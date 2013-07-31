import pytest
import pycds

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_session():
    engine = create_engine(pycds.test_dsn)
    engine.echo = True
    Session = sessionmaker(bind=engine)
    return Session()

@pytest.fixture(scope="module")
def conn_params():
    return pycds.test_dsn
