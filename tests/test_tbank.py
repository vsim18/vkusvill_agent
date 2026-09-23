from app.tbank import (
    SelectedProduct,
    build_tbank_bulk_query,
    build_tbank_queries,
    build_tbank_search_result,
)


def test_build_tbank_queries_returns_empty_list_for_empty_products() -> None:
    assert build_tbank_queries([]) == []


def test_build_tbank_bulk_query_returns_empty_string_for_empty_products() -> None:
    assert build_tbank_bulk_query([]) == ""


def test_build_tbank_queries_supports_one_product() -> None:
    products = [SelectedProduct(name="Бекон", quantity=200, unit="g", search_query="бекон")]

    assert build_tbank_queries(products) == ["бекон"]
    assert build_tbank_bulk_query(products) == "бекон"


def test_build_tbank_bulk_query_supports_multiple_products() -> None:
    products = [
        SelectedProduct(name="Спагетти", quantity=400, unit="g", search_query="спагетти"),
        SelectedProduct(name="Бекон", quantity=200, unit="g", search_query="бекон"),
    ]

    assert build_tbank_bulk_query(products) == "спагетти; бекон"


def test_build_tbank_queries_deduplicates_queries_preserving_order() -> None:
    products = [
        SelectedProduct(name="Яйца 10 шт", quantity=1, unit="pack", search_query="яйца"),
        SelectedProduct(name="Яйца 20 шт", quantity=2, unit="pack", search_query="  ЯЙЦА  "),
        SelectedProduct(name="Молоко", quantity=1, unit="l", search_query="молоко"),
    ]

    assert build_tbank_queries(products) == ["яйца", "молоко"]


def test_build_tbank_search_result_preserves_quantity_and_unit() -> None:
    products = [
        SelectedProduct(name="Бекон", quantity=200, unit="g", search_query="бекон"),
    ]

    result = build_tbank_search_result(products)

    assert result.items[0].product_name == "Бекон"
    assert result.items[0].quantity == 200
    assert result.items[0].unit == "g"
    assert result.items[0].search_query == "бекон"


def test_build_tbank_queries_preserves_product_characteristics() -> None:
    products = [
        SelectedProduct(
            name="Сливки 20%",
            quantity=200,
            unit="ml",
            search_query="сливки 20%",
        ),
        SelectedProduct(
            name="Творог 5%",
            quantity=400,
            unit="g",
            search_query="творог 5%",
        ),
        SelectedProduct(
            name="Молоко безлактозное",
            quantity=1,
            unit="l",
            search_query="молоко безлактозное",
        ),
    ]

    assert build_tbank_queries(products) == [
        "сливки 20%",
        "творог 5%",
        "молоко безлактозное",
    ]


def test_build_tbank_search_result_uses_deduplicated_bulk_query() -> None:
    products = [
        SelectedProduct(name="Яйца 10 шт", quantity=1, unit="pack", search_query="яйца"),
        SelectedProduct(name="Яйца 20 шт", quantity=2, unit="pack", search_query="яйца"),
    ]

    result = build_tbank_search_result(products)

    assert len(result.items) == 2
    assert result.bulk_query == "яйца"
