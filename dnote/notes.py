import tempfile
import subprocess
import datetime
import hashlib

import boto3
import nltk


class NoteTable:
    def __init__(self, endpoint='http://localhost:8000', table_name='dnote'):
        self.table_name = table_name
        self.index_name = f'{table_name}_index'

        self.db = boto3.resource('dynamodb', endpoint_url=endpoint)

        self.create_table(self.table_name)
        self.table = self.db.Table(self.table_name)

        self.create_table(self.index_name)
        self.index = self.db.Table(self.index_name)

    def add_note(self, text):
        if not text:
            text = self.edit_note()

        timestamp = datetime.datetime.now().timestamp()
        id = hashlib.md5(str((text, timestamp)).encode()).hexdigest()
        note = {
            'id': id,
            'text': text,
            'timestamp': int(timestamp),
        }

        self.table.put_item(Item=note)

        self.index_note(note)

    @staticmethod
    def edit_note():
        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            subprocess.call(['vim', '+startinsert', tf.name])
            tf.seek(0)
            return tf.read()

    def create_table(self, table_name):
        if table_name in self.db.meta.client.list_tables()['TableNames']:
            return
        self.db.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S',
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

    def index_note(self, note):
        tokens = self.tokenize(note['text'])
        for token in sorted(tokens):
            id = hashlib.md5(token.encode()).hexdigest()

            i = self.index.update_item(
                Key={
                    'id': id,
                },
                UpdateExpression=(
                    'SET note_ids = list_append('
                    '   if_not_exists(note_ids, :empty_list),'
                    '   :note_id)'
                ),
                ExpressionAttributeValues={
                    ':note_id': [note['id']],
                    ':empty_list': [],
                },
                ReturnValues='UPDATED_NEW', #temp
            )

    @staticmethod
    def tokenize(text):
        nltk.download('punkt')
        tokens = nltk.word_tokenize(text)
        stemmer = nltk.PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        partial_tokens = []
        for token in list(set(tokens + stemmed_tokens)):
            for i in range(1, len(token) + 1):
                ngrams = nltk.ngrams(token, i)
                partial_tokens.extend(ngrams)

        return set(''.join(token) for token in partial_tokens)


    def find_notes(self):
        print(self.table.scan())


if __name__ == '__main__':
    main()
