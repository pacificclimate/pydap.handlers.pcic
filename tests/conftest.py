import pytest
import pycds

@pytest.fixture(scope="module")
def test_session():
    return pycds.test_session()

@pytest.fixture(scope="module")
def conn_params():
    return pycds.test_dsn
