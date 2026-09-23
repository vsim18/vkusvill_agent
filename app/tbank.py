from dataclasses import dataclass


@dataclass(frozen=True)
class SelectedProduct:
    name: str
    quantity: float | None = None
    unit: str | None = None
    search_query: str = ""


@dataclass(frozen=True)
class TBankSearchItem:
    product_name: str
    quantity: float | None
    unit: str | None
    search_query: str


@dataclass(frozen=True)
class TBankSearchResult:
    items: list[TBankSearchItem]
    bulk_query: str


def normalize_search_query(search_query: str) -> str:
    return " ".join(search_query.strip().lower().split())


def build_tbank_queries(products: list[SelectedProduct]) -> list[str]:
    queries: list[str] = []
    seen: set[str] = set()

    for product in products:
        query = normalize_search_query(product.search_query)
        if not query or query in seen:
            continue
        seen.add(query)
        queries.append(query)

    return queries


def build_tbank_bulk_query(products: list[SelectedProduct]) -> str:
    return "; ".join(build_tbank_queries(products))


def build_tbank_search_result(products: list[SelectedProduct]) -> TBankSearchResult:
    return TBankSearchResult(
        items=[
            TBankSearchItem(
                product_name=product.name,
                quantity=product.quantity,
                unit=product.unit,
                search_query=normalize_search_query(product.search_query),
            )
            for product in products
            if normalize_search_query(product.search_query)
        ],
        bulk_query=build_tbank_bulk_query(products),
    )
