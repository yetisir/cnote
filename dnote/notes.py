import tempfile
import subprocess
import datetime
import hashlib
import sys

import boto3
import nltk

from . import utils


class NoteTable:
    def __init__(self, endpoint='http://localhost:8000', table_name='dnote'):
        self.table_name = table_name
        self.index_name = f'{table_name}_index'

        self.db = boto3.resource('dynamodb', endpoint_url=endpoint)

        self.create_table(self.table_name)
        self.table = self.db.Table(self.table_name)

        self.create_table(self.index_name)
        self.index = self.db.Table(self.index_name)

    def parse_text(self, text):
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        if not text:
            text = self.edit_text()
        if not text:
            exit()

        return text.strip()

    def add_note(self, text):
        timestamp = datetime.datetime.now().timestamp()
        note = {
            'id': hashlib.md5(str((text, timestamp)).encode()).hexdigest(),
            'text': self.parse_text(text),
            'timestamp': int(timestamp),
        }

        self.table.put_item(Item=note)
        self.index_note(note)

    @staticmethod
    def edit_text():
        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            subprocess.call(['vim', '+startinsert', tf.name])
            tf.seek(0)
            return tf.read().decode()

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
        for token_id in self.token_ids(tokens):
            self.index.update_item(
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
            )

    @staticmethod
    def token_ids(tokens):
        return [hashlib.md5(token.encode()).hexdigest() for token in tokens]

    @staticmethod
    def tokenize(text):
        nltk.download('punkt', quiet=True)
        tokens = set(nltk.word_tokenize(text))
        stemmer = nltk.PorterStemmer()
        stemmed_tokens = set(stemmer.stem(token) for token in tokens)
        tokens.update(stemmed_tokens)

        return [''.join(token) for token in tokens]

    def find_notes(self, text):
        text = self.parse_text(text)
        tokens = self.tokenize(text)
        token_ids = self.token_ids(tokens)
        id_response = self.db.batch_get_item(
            RequestItems={
                self.index_name: {
                    'Keys': [{'id': token_id} for token_id in token_ids],
                },
            },

        )['Responses'][self.index_name]

        if not id_response:
            return

        note_ids = set(id_response[0]['note_ids'])

        notes = self.db.batch_get_item(
            RequestItems={
                self.table.name: {
                    'Keys': [{'id': note_id} for note_id in note_ids],
                },
            },
        )['Responses'][self.table_name]

        self.show_notes(notes)

    @staticmethod
    def show_notes(notes):
        for note in notes:
            timestamp = datetime.datetime.fromtimestamp(note['timestamp'])
            print(f'{timestamp} -', note['text'])
