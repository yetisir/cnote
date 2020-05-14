from . import aws, common


class NoteIndex(common.DynamoDBTable):
    #table_name = settings.DYNAMODB_NOTETABLE
    table_name = 'dnote_index'

    def __init__(self):
        super().__init__(self)

    def add_note(self, note):
        for field, tokens in note.tokens.items():
            for token_id in tokens.keys():
                self.update_index(note.id, token_id, field)

    @staticmethod
    def get_field_name(field):
        return f'note_ids_in_{field}'

    def update_index(self, note_id, token_id, field):
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
        if not token_ids:
            return []

        return aws.dynamodb.batch_get_item(
            RequestItems={
                self.table_name: {
                    'Keys': [{'id': token_id} for token_id in token_ids],
                },
            },
        )['Responses'][self.table_name]
