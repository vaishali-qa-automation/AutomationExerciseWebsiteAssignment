from api.base_client import BaseClient


class ProductsEndpoints:
    PRODUCTS_LIST = "/api/productsList"
    BRANDS_LIST = "/api/brandsList"
    SEARCH_PRODUCT = "/api/searchProduct"


class ProductsApi:
    def __init__(self, client: BaseClient):
        self._client = client

    def list_products(self):
        return self._client.get(ProductsEndpoints.PRODUCTS_LIST)

    def search_product(self, product: str):
        return self._client.post(
            ProductsEndpoints.SEARCH_PRODUCT,
            data={"search_product": product},
        )

    def list_brands(self):
        return self._client.get(ProductsEndpoints.BRANDS_LIST)


