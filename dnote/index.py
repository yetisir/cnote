from . import aws, common
from .config import settings


class NoteIndex(common.DynamoDBTable):
    """Class to help interface with DynamoDB index table.

    Attributes:
        table_name (str): table name
    """
    table_name = settings.dynamodb_index_table

    def __init__(self):
        super().__init__(self)

    def add_note(self, note):
        """Adds a note to the index table.

        Args:
            note (dnote.notes.Note): Note to be added to the index
        """

        for field, tokens in note.tokens.items():
            for token_id in tokens.keys():
                self.update_index(note.id, token_id, field)

    @staticmethod
    def get_field_name(field):
        """Returns DynamoDB field name. Here a field refers to the component
        of the note (i.e. body, name, tags, or host)

        Args:
            field (str): field type

        Returns:
            str: field name
        """

        return f'note_ids_in_{field}'

    def update_index(self, note_id, token_id, field):
        """updates the DynamoDB index given a new index entry

        Args:
            note_id (str): Note id.
            token_id (str): Token id.
            field (str): Component of the note (i.e. body, name, tags,
                or host).
        """

        field_name = self.get_field_name(field)
        self.table.update_item(
            Key={
                'id': token_id,
            },
            UpdateExpression=(
                f'SET {field_name} = list_append('
                f'   if_not_exists({field_name}, :empty_list),'
                f'   :note_id) '
            ),
            ExpressionAttributeValues={
                ':note_id': [note_id],
                ':empty_list': [],
            },
        )

    def query_token_ids(self, token_ids):
        """Search database for specific token ids.

        Args:
            token_ids (list fo str): List of token ids.

        Returns:
            list of dict: List of notes (as dicts) associated with the
                specified token_id.
        """

        if not token_ids:
            return []

        return aws.dynamodb.batch_get_item(
            RequestItems={
                self.table_name: {
                    'Keys': [{'id': token_id} for token_id in token_ids],
                },
            },
        )['Responses'][self.table_name]
