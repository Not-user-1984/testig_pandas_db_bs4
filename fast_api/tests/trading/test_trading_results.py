import pytest
from datetime import date
from infra.sql.trading import SQLTradingRepository


@pytest.mark.asyncio
async def test_get_last_trading_dates(session, expected_trading_dates):
    trading_repository = SQLTradingRepository(session)

    dates = await trading_repository.get_last_trading_dates(limit=10)

    assert len(dates) <= 10
    assert all(isinstance(d, date) for d in dates)
    assert (
        dates == expected_trading_dates
    ), "Возвращённые даты не соответствуют ожидаемым"


@pytest.mark.asyncio
async def test_get_trading_results(session, trading_results_test_case):
    trading_repository = SQLTradingRepository(session)
    results = await trading_repository.get_trading_results(
        **trading_results_test_case["params"]
    )

    assert len(results) >= 0

    if results:
        assert trading_results_test_case["expected"](
            results
        ), "Результаты не соответствуют ожидаемым условиям"


@pytest.mark.asyncio
async def test_get_dynamics(session, dynamics_test_case):
    trading_repository = SQLTradingRepository(session)
    results = await trading_repository.get_dynamics(
        **dynamics_test_case["params"]
        )

    assert len(results) >= 0

    if results:
        assert dynamics_test_case["expected"](
            results
        ), "Результаты не соответствуют ожидаемым условиям"


@pytest.mark.asyncio
async def test_get_total_count(session):
    trading_repository = SQLTradingRepository(session)
    count = await trading_repository.get_total_count(
        oil_id="A100", delivery_type_id="F", delivery_basis_id="AN"
    )
    assert isinstance(count, int)
    assert count >= 0
