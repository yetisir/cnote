import tempfile
import subprocess
import datetime
import hashlib
import sys
import socket
import os
import getpass 

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
    def __init__(self, body, name, tags=None, **kwargs):
        self.name = name if name else f'{getpass.getuser()}\'s Note'
        self.body = body.strip()
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
            'body': Text(self.body).tokens,
            'name': Text(self.name).tokens,
            'host': Text(self.host).tokens,
            'tags': Text(' '.join(self.tags)).tokens,
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'body': self.body,
            'timestamp': self.timestamp,
            'host': self.host,
            'tags': self.tags,
        }

    def show(self):
        print(f'"{self.name}" [{self.host}@{self.datetime}]')
        for line in self.body.split('\n'):
            print(f'\t{line}')

    def _get_timestamp(self):
        return int(datetime.datetime.now().timestamp())

    def _get_id(self):
        hash_list = [
            self.name,
            self.body,
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

    def add_note(self, body, name=None, tags=None):
        note = Note(body, name=name, tags=tags)
        self.table.put_item(Item=note.to_dict())
        self.index.add_note(note)
        note.show()

    def get_note_from_id(self, id):
        response = self.table.get_item(Key={'id': id})
        return Note.from_dict(response)

    def get_notes_from_ids(self, ids):
        notes = aws.dynamodb.batch_get_item(
            RequestItems={
                self.table.name: {
                    'Keys': [{'id': note_id} for note_id in ids],
                },
            },
        )['Responses'][self.table_name]

        return [Note.from_dict(note) for note in notes]
            
    @staticmethod
    def show_notes(notes):
        for note in notes:
            note.show()

    def text_search(self, field_searches, exact=False):
        field_searches = {
            field: searches for field, searches in field_searches.items()
            if searches}
        search_map = self._create_search_map(field_searches)

        note_id_sets = []

        for field_search_map in search_map.values():
            for note_ids in field_search_map.values():
                note_id_sets.append(note_ids)

        all_note_ids = set.intersection(*note_id_sets)

        if not all_note_ids:
            return

        notes = self.get_notes_from_ids(all_note_ids)

        if exact:
            notes = self._exact_match_notes(notes, field_searches)

        if not notes:
            return

        notes.sort(key=lambda note: note.timestamp)
        self.show_notes(notes)

    @staticmethod
    def _exact_match_notes(notes, field_searches):
            exact_match_notes = []
            for note in notes:
                for field, search in field_searches.items():
                    if search in getattr(note, field):
                        exact_match_notes.append(note)
            return exact_match_notes

    def _create_search_map(self, fields):
        search_map = {}
        for field, search in fields.items():

            tokens = Text(search).tokens
            responses = self.index.query_token_ids(tokens)

            field_search_map = {}
            for response in responses:
                token_note_ids = response.get(index.NoteIndex.get_field_name(field))
                if not token_note_ids:
                    continue
                field_search_map[tokens[response['id']]] = set(token_note_ids)

            search_map[field] = field_search_map

        return search_map