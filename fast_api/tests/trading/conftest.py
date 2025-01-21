import pytest
from .test_data import test_cases, test_cases_trading_results, expected_dates


@pytest.fixture(params=test_cases)
def dynamics_test_case(request):
    return request.param


@pytest.fixture(params=test_cases_trading_results)
def trading_results_test_case(request):
    return request.param

@pytest.fixture
def expected_trading_dates():
    return expected_dates