import logging

logger = logging.getLogger(__name__)

class TestProductsApi:

    def test_list_products(self, product_api):
        response = product_api.list_products()
        json_data = response.json()
        assert json_data["responseCode"] == 200
        assert isinstance(json_data["products"][0]["id"], int)