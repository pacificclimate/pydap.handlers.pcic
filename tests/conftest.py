import pytest
import pycds

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_session():
    engine = create_engine('sqlite+pysqlite:///{0}'.format(pycds.test_dsn))
    engine.echo = True
    Session = sessionmaker(bind=engine)
    return Session()

@pytest.fixture(scope="module")
def conn_params():
    return 'sqlite+pysqlite:///{0}'.format(pycds.test_dsn)
