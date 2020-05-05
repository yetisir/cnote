from . import aws, common

class NoteIndex(common.DynamoDBTable):
    table_name = 'dnote_index'  # TODO: move to config

    def __init__(self):
        super().__init__(self)

    def add_note(self, note):
        for field, tokens in note.tokens.items():
            for token_id in tokens.keys():
                self.update_index(note.id, token_id, field)

    def update_index(self, note_id, token_id, field):
        self.table.update_item(
            Key={
                'id': token_id,
            },
            UpdateExpression=(
                f'SET note_ids_in_{field} = list_append('
                f'   if_not_exists(note_ids_in_{field}, :empty_list),'
                f'   :note_id) '
            ),
            ExpressionAttributeValues={
                ':note_id': [note_id],
                ':empty_list': [],
            },
        )

    def query_token_ids(self, token_ids):
        return aws.dynamodb.batch_get_item(
            RequestItems={
                self.table_name: {
                    'Keys': [{'id': token_id} for token_id in token_ids],
                },
            },            
        )