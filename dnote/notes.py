import tempfile
import subprocess
import datetime
import hashlib
import sys
import socket
import os

import nltk

from . import aws, index, common


class Text:
    def __init__(self, raw):
        self.raw = raw.strip()

    @property
    def tokens(self):
        tokens = set(nltk.word_tokenize(self.raw.lower()))
        stemmer = nltk.PorterStemmer()
        stemmed_tokens = set(stemmer.stem(token) for token in tokens)
        tokens.update(stemmed_tokens)

        tokens = [''.join(token) for token in tokens]

        return {self.token_id(token): token for token in tokens}

    @staticmethod
    def token_id(token):
        return hashlib.md5(token.encode()).hexdigest()


class Note:
    def __init__(self, name, text, tags=None, **kwargs):
        self.name = name
        self.text = text.strip()
        self.timestamp = self._get_timestamp()
        self.host = socket.gethostname()
        self.tags = tags if tags else []
        self.id = self._get_id()

    @classmethod
    def from_dict(cls, attributes):
        note_instance = cls(**attributes)
        for attribute, value in attributes.items():
            setattr(note_instance, attribute, value)

        return note_instance

    @property
    def datetime(self):
        return datetime.datetime.fromtimestamp(self.timestamp)

    @property
    def tokens(self):
        return {
            'text': Text(self.text).tokens,
            'name': Text(self.name).tokens,
            'tags': Text(' '.join(self.tags)).tokens,
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'text': self.text,
            'timestamp': self.timestamp,
            'host': self.host,
            'tags': self.tags,
        }

    def show(self):
        print(f'{self.name} | {self.datetime} | {self.host}')
        print('\t' + self.text.replace('\n', '\n\t'))

    def _get_timestamp(self):
        return int(datetime.datetime.now().timestamp())

    def _get_id(self):
        hash_list = [
            self.name,
            self.text,
            self.timestamp,
            self.host,
            tuple(self.tags),
        ]

        return hashlib.md5(str(hash_list).encode()).hexdigest()


class NoteCollection(common.DynamoDBTable):
    table_name='dnote'  #TODO: get from config

    def __init__(self):
        super().__init__(self)
        self.index = index.NoteIndex()

    def init_tables(self):
        if not self.exists:
            self.create_table()
        
        if not self.index.exists:
            self.index.create_table()

    def add_note(self, name, text, tags=None):
        note = Note(name, text, tags)
        self.table.put_item(Item=note.to_dict())
        self.index.add_note(note)
        note.show()

    def get_note_from_id(self, id):
        response = self.table.get_item(Key={'id': id})
        return Note.from_dict(response)
            
    @staticmethod
    def show_notes(notes):
        for note in notes:
            note.show()

    def search_notes(self, text, field):
        text = Text(text)
        self.index.query_token_ids(text.tokens.keys())

        print(id_response)
    # def find_notes(self, text):
    #     pass

    #     text = self.parse_text(text)
    #     tokens = self.tokenize(text)
    #     token_ids = self.token_ids(tokens)
    #     id_response = aws.dynamodb.batch_get_item(
    #         RequestItems={
    #             self.index_name: {
    #                 'Keys': [{'id': token_id} for token_id in token_ids],
    #             },
    #         },

    #     )['Responses'][self.index_name]

    #     if not id_response:
    #         return

    #     note_ids = set(id_response[0]['note_ids'])

    #     notes = aws.dynamodb.batch_get_item(
    #         RequestItems={
    #             self.table.name: {
    #                 'Keys': [{'id': note_id} for note_id in note_ids],
    #             },
    #         },
    #     )['Responses'][self.table_name]

    #     if not quiet:
    #         self.show_notes(notes)

    #     return notes