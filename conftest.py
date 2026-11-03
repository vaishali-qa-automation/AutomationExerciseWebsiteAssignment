import logging
import sys
import time
from collections.abc import Callable
from pathlib import Path

import pytest
from reportportal_client import RPLogger, RPLogHandler

from api.base_client import BaseClient
from api.users_api import UsersApi
from utilities.driver_factory import get_driver
from utilities.common_methods import get_config_section
from utilities.data_factory import new_user


logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CONFIG_FILE = Path(__file__).parent / "config" / "env_config.ini"
SUPPORTED_BROWSERS = ["chrome", "firefox"]


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        type=str.lower,
        help="Browser to run UI test on chrome | firefox",
        choices=SUPPORTED_BROWSERS,
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="Run the browser in headless mode",
    )
    parser.addini(
        "headless", type="bool", default=False, help="Run the browser in headless mode"
    )
    parser.addini(
        "browser", type="string", default=False, help="Browser type: Chrome or Firefox"
    )


@pytest.fixture
def driver(request):
    # Either this will be in pytest.ini file or provided from CLI
    browser = request.config.getoption("--browser") or request.config.getini("browser")
    headless = request.config.getoption("--headless") or request.config.getini(
        "headless"
    )
    driver = get_driver(browser, headless)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_client():
    default_section = get_config_section(CONFIG_FILE)
    base_url = default_section["base_url"]
    base_client = BaseClient(base_url)
    yield base_client
    base_client.close()


@pytest.fixture(scope="session")
def user_api(base_client):
    user_api = UsersApi(base_client)
    return user_api


@pytest.fixture
def user_data_factory() -> Callable:
    """
    Fixture that returns the imported new_user function object.
    Allows test cases to call the function directly with custom arguments.
    """
    return new_user


@pytest.fixture(scope="session", autouse=True)
def configure_global_logging(request):
    # CRITICAL: Reconfigure the global logging class for ReportPortal compatibility
    logging.setLoggerClass(RPLogger)

    # Fetch the root logger - this controls logging across ALL imported modules
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Define a clean text format for your console and files
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s::%(funcName)s::%(lineno)d::%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. Local File Handler (Tracks everything globally across POMs and tests)
    file_handler = logging.FileHandler(
        "logs/execution_flow.log", mode="w", encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    # 2. Extract the ReportPortal Service Orchestrator
    rp_plugin = request.config.pluginmanager.get_plugin("pytest-reportportal")
    rp_service = getattr(rp_plugin, "py_test_service", None)

    if rp_service:
        # ReportPortal Data Stream
        rp_handler = RPLogHandler(rp_client=rp_service)
        rp_handler.setLevel(logging.INFO)
        root_logger.addHandler(rp_handler)

        # Standard Terminal Output (Mirroring)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        root_logger.addHandler(console_handler)
    else:
        # Fallback Terminal output if offline/not running with --reportportal
        fallback_console = logging.StreamHandler(sys.stdout)
        fallback_console.setLevel(logging.INFO)
        fallback_console.setFormatter(log_format)
        root_logger.addHandler(fallback_console)

    yield

    # Clean up handlers after the test session finishes
    handlers = root_logger.handlers[:]
    for handler in handlers:
        handler.close()
        root_logger.removeHandler(handler)


# pytesthook for reporting and adding the screenshots on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """This hook captures screenshots of failed tests and routes them

    simultaneously to local disk, the console, your text file, and ReportPortal.
    """
    # Execute the test step phase
    outcome = yield
    result = outcome.get_result()  # Extract the test execution report object
    setattr(item, "rep_" + result.when, result)

    # We only care when an actual test validation step ("call") drops an assertion failure
    if result.when == "call" and result.failed:
        # Fetch your active browser instance dynamically from the current test context
        driver = item.funcargs.get("get_driver", None)

        if driver:
            # 1. Save locally to a workspace directory
            timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
            screenshot_filename = f"{item.name}_{timestamp}.png"
            screenshot_dir = Path(__file__).resolve().parent / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / screenshot_filename
            driver.save_screenshot(str(screenshot_path))

            # 2. Extract image bytes for data transport
            screenshot_bytes = driver.get_screenshot_as_png()

            # 3. Use the global logger to dispatch to ALL targets at once
            logger.error(
                f"TEST FAILURE RECORDED: Case '{item.name}' collapsed during execution. Sending screenshot asset.",
                extra={
                    "attachment": {
                        "name": f"failure_{item.name}.png",
                        "data": screenshot_bytes,
                        "mime": "image/png",
                    }
                },
            )
        else:
            # If the driver wasn't found, log a clean warning across all pipelines
            logger.warning(
                f"Automation dropped an error on '{item.name}', but 'get_driver' fixture instance was unreachable."
            )
