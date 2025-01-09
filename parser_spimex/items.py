
from scrapy import Item, Field


class ParsedDataItem(Item):
    """
    Класс для хранения структурированных данных, извлеченных из XLS-файлов.
    """
    id = Field()
    exchange_product_id = Field()
    exchange_product_name = Field()
    oil_id = Field()
    delivery_basis_id = Field()
    delivery_basis_name = Field()
    delivery_type_id = Field()
    volume = Field()
    total = Field()
    count = Field()
    date = Field()
