from datetime import datetime, timezone
import socket
import getpass
from unittest import mock

import pytest
from botocore import stub

from dnote import aws, utils

TEST_TIMESTAMP = datetime(2020, 12, 25, 17, 5, 55, tzinfo=timezone.utc)
TEST_HOST = 'host'
TEST_USER = 'user'


@pytest.fixture(autouse=True)
def dynamodb_stub():
    with stub.Stubber(aws.dynamodb.meta.client) as stubber:
        yield stubber
#        stubber.assert_no_pending_responses()


@pytest.fixture
def datetime_now(monkeypatch):
    monkeypatch.setattr(
        utils, 'now', lambda: TEST_TIMESTAMP)


@pytest.fixture
def host(monkeypatch):
    monkeypatch.setattr(
        socket, 'gethostname', lambda: TEST_HOST)


@pytest.fixture
def user(monkeypatch):
    monkeypatch.setattr(
        getpass, 'getuser', lambda: TEST_USER)
