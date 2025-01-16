import pytest
from datetime import date
from infra.sql.trading import SQLTradingRepository


@pytest.mark.asyncio
async def test_get_last_trading_dates(session):
    trading_repository = SQLTradingRepository(session)
    dates = await trading_repository.get_last_trading_dates(limit=5)
    assert len(dates) <= 5
    assert all(isinstance(d, date) for d in dates)


@pytest.mark.asyncio
async def test_get_trading_results(session):
    trading_repository = SQLTradingRepository(session)
    results = await trading_repository.get_trading_results(
        oil_id="A100", delivery_type_id="F", delivery_basis_id="ANK", skip=0, limit=10
    )
    assert len(results) >= 0
    if results:
        assert results[0].oil_id == "A100"
        assert results[0].delivery_type_id == "F"
        assert results[0].delivery_basis_id == "ANK"


@pytest.mark.asyncio
async def test_get_dynamics(session):
    trading_repository = SQLTradingRepository(session)
    results = await trading_repository.get_dynamics(
        oil_id="A100",
        # delivery_type_id="F",
        # delivery_basis_id="ANK",
        # start_date=date(2023, 1, 1),
        # end_date=date(2023, 12, 31),
        # skip=0,
        # limit=10,
    )
    assert len(results) > 0, "Метод вернул пустой список, хотя это недопустимо"

    assert results[0].oil_id == "A100"
    assert results[0].delivery_type_id == "F"
    assert results[0].delivery_basis_id == "ANK"
    assert results[0].date >= date(2024, 1, 1)
    assert results[0].date <= date(2024, 12, 31)


@pytest.mark.asyncio
async def test_get_dynamics_delivery_type_id(session):
    trading_repository = SQLTradingRepository(session)
    results = await trading_repository.get_dynamics(

        delivery_type_id="F",

    )
    assert len(results) > 0, "Метод вернул пустой список, хотя это недопустимо"

    assert results[0].oil_id == "A100"
    assert results[0].delivery_type_id == "F"
    assert results[0].delivery_basis_id == "ANK"
    assert results[0].date >= date(2024, 1, 1)
    assert results[0].date <= date(2024, 12, 31)


@pytest.mark.asyncio
async def test_get_total_count(session):
    trading_repository = SQLTradingRepository(session)
    count = await trading_repository.get_total_count(
        oil_id="A100", delivery_type_id="F", delivery_basis_id="AN"
    )
    assert isinstance(count, int)
    assert count >= 0
