import datetime
import hashlib

import boto3


class NoteTable:
    def __init__(self, endpoint=None, table_name='dnote'):
        self.db = boto3.resource('dynamodb', endpoint_url=endpoint)
        self.table = self.db.Table(table_name)
        self.table_name = table_name

        self.create_table()

    def add_note(self, text):
        timestamp = datetime.datetime.now().timestamp()
        id = hash((text, timestamp))
        note = {
            'id': int(id),
            'text': text,
            'timestamp': int(timestamp),
        }


        self.table.put_item(Item=note)

    def create_table(self):
        if self.table_name in self.db.meta.client.list_tables()['TableNames']:
            return
        self.db.create_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH',
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            },
        )


def main():
    table = NoteTable(endpoint='http://localhost:8000')
    table.add_note('this is a new note!')
    table.add_note('this is a note!')
    table.add_note('this is another note!')

    table.push_notes()

if __name__ == '__main__':
    main()

