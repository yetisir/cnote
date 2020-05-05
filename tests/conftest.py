import pytest
from botocore import stub

from dnote import aws


@pytest.fixture(autouse=True)
def dynamodb_stub():
    with stub.Stubber(aws.dynamodb.meta.client) as stubber:
        yield stubber
#        stubber.assert_no_pending_responses()
