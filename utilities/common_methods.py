import configparser
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_config_section(
    config_file: str | Path,
    section: str = "DEFAULT",
) -> configparser.SectionProxy:
    """
    Read an INI file and return one section.

    Args:
        config_file: path to the INI file
        section: section name (defaults to DEFAULT)

    Returns:
        SectionProxy: dict-like view of the section. All values are strings;
        use .getint() / .getboolean() for typed values.

    Raises:
        FileNotFoundError: file missing or unreadable
        ValueError: section not present in the file
    """
    config_path = Path(config_file)

    parser = configparser.ConfigParser()
    if not parser.read(config_path, encoding="utf-8"):
        raise FileNotFoundError(
            f"Config file not found or unreadable: {config_path.resolve()}"
        )

    if section not in parser:
        raise ValueError(
            f"Section '{section}' not found in {config_path.name}. "
            f"Available: {parser.sections()}"
        )

    logger.debug(f"Loaded section '{section}' from {config_path}")
    return parser[section]
