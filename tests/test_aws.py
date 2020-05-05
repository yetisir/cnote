import pytest
from botocore import stub
from dnote import notes


@pytest.fixture(autouse=True)
def test_create_table():
    table = notes.NoteTable()
    with stub.Stubber(table.db.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
