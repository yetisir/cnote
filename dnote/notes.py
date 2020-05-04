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
        tokens = self.tokenize(note['text'], partial=True)
        for token_id in self.token_ids(tokens):
            i = self.index.update_item(
                Key={
                    'id': token_id,
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
    def token_ids(tokens):
        return [hashlib.md5(token.encode()).hexdigest() for token in tokens]

    @staticmethod
    def tokenize(text, partial=False):
        nltk.download('punkt')
        tokens = set(nltk.word_tokenize(text))
        stemmer = nltk.PorterStemmer()
        stemmed_tokens = set(stemmer.stem(token) for token in tokens)
        tokens.update(stemmed_tokens)
        if partial:
            for token in tokens.copy():
                for i in range(1, len(token) + 1):
                    ngrams = nltk.ngrams(token, i)
                    tokens.update(ngrams)

        return [''.join(token) for token in tokens]


    def find_notes(self, text):
        tokens = self.tokenize(text, partial=False)
        token_ids = self.token_ids(tokens)
        id_response = self.db.batch_get_item(
            RequestItems={
                self.index_name: {
                    'Keys': [{'id': token_id} for token_id in token_ids],
                },
            },

        )

        note_ids = set(id_response['Responses'][self.index_name][0]['note_ids'])

        note_response = self.db.batch_get_item(
            RequestItems={
                self.table.name: {
                    'Keys': [{'id': note_id} for note_id in note_ids],
                },
            },
        )

        notes = note_response['Responses'][self.table_name]
        self.show_notes(notes)


    @staticmethod
    def show_notes(notes):
        for note in notes:
            timestamp = datetime.datetime.fromtimestamp(note['timestamp'])
            print(f'{timestamp} -', note['text'])


if __name__ == '__main__':
    main()
