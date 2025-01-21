from datetime import date

test_cases = [
    {
        "params": {"oil_id": "A100"},
        "expected": lambda results: all(result.oil_id == "A100" for result in results),
    },
    {
        "params": {"delivery_type_id": "F"},
        "expected": lambda results: all(
            result.delivery_type_id == "F" for result in results
        ),
    },
    {
        "params": {"delivery_basis_id": "ANK"},
        "expected": lambda results: all(
            result.delivery_basis_id == "ANK" for result in results
        ),
    },
    {
        "params": {"start_date": date(2023, 1, 1)},
        "expected": lambda results: all(
            result.date >= date(2023, 1, 1) for result in results
        ),
    },
    {
        "params": {"end_date": date(2023, 12, 31)},
        "expected": lambda results: all(
            result.date <= date(2023, 12, 31) for result in results
        ),
    },
    {
        "params": {"skip": 0, "limit": 10},
        "expected": lambda results: len(results) <= 10,
    },
    {
        "params": {
            "oil_id": "A100",
            "delivery_type_id": "F",
            "delivery_basis_id": "ANK",
            "start_date": date(2023, 1, 1),
            "end_date": date(2023, 12, 31),
            "skip": 0,
            "limit": 10,
        },
        "expected": lambda results: (
            all(result.oil_id == "A100" for result in results)
            and all(result.delivery_type_id == "F" for result in results)
            and all(result.delivery_basis_id == "ANK" for result in results)
            and all(result.date >= date(2023, 1, 1) for result in results)
            and all(result.date <= date(2023, 12, 31) for result in results)
            and len(results) <= 10
        ),
    },
]
test_cases_trading_results = [
    {
        "params": {"oil_id": "A100"},
        "expected": lambda results: (
            len(results) >= 0
            and (not results or all(result.oil_id == "A100" for result in results))
        ),
    },
    {
        "params": {"delivery_type_id": "F"},
        "expected": lambda results: (
            len(results) >= 0
            and (
                not results or all(result.delivery_type_id == "F" for result in results)
            )
        ),
    },
    {
        "params": {"delivery_basis_id": "ANK"},
        "expected": lambda results: (
            len(results) >= 0
            and (
                not results
                or all(result.delivery_basis_id == "ANK" for result in results)
            )
        ),
    },
    {
        "params": {"skip": 0, "limit": 10},
        "expected": lambda results: len(results) <= 10,
    },
    {
        "params": {
            "oil_id": "A100",
            "delivery_type_id": "F",
            "delivery_basis_id": "ANK",
            "skip": 0,
            "limit": 10,
        },
        "expected": lambda results: (
            len(results) >= 0
            and (
                not results
                or (
                    all(result.oil_id == "A100" for result in results)
                    and all(result.delivery_type_id == "F" for result in results)
                    and all(result.delivery_basis_id == "ANK" for result in results)
                    and len(results) <= 10
                )
            )
        ),
    },
]

expected_dates = [
    date(2024, 12, 24),
    date(2024, 12, 10),
    date(2024, 11, 26),
    date(2024, 11, 12),
    date(2024, 10, 29),
    date(2024, 10, 15),
    date(2024, 10, 1),
    date(2024, 9, 17),
    date(2024, 9, 3),
    date(2024, 8, 20),
]
