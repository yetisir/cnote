import tempfile
import subprocess
import datetime

import boto3


class NoteTable:
    def __init__(self, endpoint=None, table_name='dnote'):
        self.db = boto3.resource('dynamodb', endpoint_url=endpoint)
        self.table = self.db.Table(table_name)
        self.table_name = table_name

        self.create_table()

    def add_note(self, text):
        if not text:
            text = self.edit_note()

        timestamp = datetime.datetime.now().timestamp()
        id = hash((text, timestamp))
        note = {
            'id': int(id),
            'text': text,
            'timestamp': int(timestamp),
        }

        self.table.put_item(Item=note)

    @staticmethod
    def edit_note():
        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            subprocess.call(['vim', '+startinsert', tf.name])
            tf.seek(0)
            return tf.read()

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


    def find_notes(self):
        print(self.table.scan())


def main():
    table = NoteTable(endpoint='http://localhost:8000')
    table.add_note('this is a new note!')
    table.add_note('this is a note!')
    table.add_note('this is another note!')

    table.push_notes()


if __name__ == '__main__':
    main()
