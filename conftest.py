import pytest

def pytest_addoption(parser):
    parser.addoption("--p", help="Type Password")
    parser.addoption("--u", help="Type Username")

@pytest.fixture
def p(request):
    return request.config.getoption("--p")

@pytest.fixture
def u(request):
    return request.config.getoption("--u")


