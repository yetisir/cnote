from botocore import stub

from cnote import notes, aws


def test_note_table_exists():
    with stub.Stubber(aws.dynamodb.meta.client) as stubber:
        collection = notes.NoteCollection(create_tables=False)

        stubber.add_response(
            'list_tables', {'TableNames': ['cnote', 'cnote_index']})

        assert collection.exists is True
        stubber.assert_no_pending_responses()


def test_index_table_exists():
    with stub.Stubber(aws.dynamodb.meta.client) as stubber:
        collection = notes.NoteCollection(create_tables=False)

        stubber.add_response(
            'list_tables', {'TableNames': ['cnote', 'cnote_index']})

        assert collection.exists is True
        stubber.assert_no_pending_responses()
