import hashlib
import socket
import getpass
from datetime import datetime

import nltk
from dynaconf import settings

from . import aws, index, common, utils


class Text:
    def __init__(self, raw):
        self.raw = raw.strip()

    @property
    def tokens(self):
        raw_tokens = set(nltk.word_tokenize(self.raw.lower()))
        stemmer = nltk.LancasterStemmer()
        stemmed_tokens = set(stemmer.stem(token) for token in raw_tokens)
        tokens = [''.join(token) for token in stemmed_tokens]

        return {self.token_id(token): token for token in tokens}

    @staticmethod
    def token_id(token):
        return hashlib.md5(token.encode()).hexdigest()


class Note:
    def __init__(self, body, name=None, tags=None, **kwargs):
        self.name = name.strip() if name else f'{getpass.getuser()}-note'
        self.body = body.strip()
        self.timestamp = self._get_timestamp()
        self.host = socket.gethostname()
        self.tags = [tag.strip() for tag in tags] if tags else []
        self.id = self._get_id()
        self.name = self.name if name else f'{self.name}-{self.id[:8]}'

    @classmethod
    def from_dict(cls, attributes):
        note_instance = cls(**attributes)
        for attribute, value in attributes.items():
            setattr(note_instance, attribute, value)

        return note_instance

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp)

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

    def show(self, quiet=False, max_lines=10):
        if quiet:
            print(self.id)
            return

        print(f'{self.id} ({self.name}) [{self.host}@{self.datetime}]')
        lines = self.body.split('\n')
        for line in lines[:max_lines]:
            print(f'\t{line}')

        if max_lines and len(lines) > max_lines:
            missing_lines = len(lines) - max_lines
            print(f'[Truncated {missing_lines} lines] ...\n')

    def _get_id(self):
        note_hash = hashlib.md5()
        note_hash.update(self.name.encode())
        note_hash.update(self.body.encode())
        note_hash.update(self.host.encode())
        note_hash.update(str(self.timestamp).encode())
        for tag in self.tags:
            note_hash.update(tag.encode())

        return note_hash.hexdigest()

    @staticmethod
    def _get_timestamp():
        return int(utils.now().timestamp())


class NoteCollection(common.DynamoDBTable):
    # table_name = settings.DYNAMODB_NOTETABLE
    table_name = 'dnote'

    def __init__(self, create_tables=True):
        super().__init__()
        self.index = index.NoteIndex()

        if create_tables:
            self._initialize_tables()

    def add_note(self, body=None, name=None, tags=None):

        note = Note(body, name=name, tags=tags)
        self.table.put_item(Item=note.to_dict())
        self.index.add_note(note)
        note.show()

    def update_note(self, note, body=None, name=None, tags=None):

        body = body if body else note.body
        name = name if name else note.name
        tags = tags if tags else note.tags
        self.add_note(body=body, name=name, tags=tags)
        self.delete_notes([note.id])

    def delete_notes(self, ids):
        with self.table.batch_writer() as batch:
            for id in ids:
                batch.delete_item(Key={'id': id})
        # TODO: remove old note index references
        # self.index.delete_note(id)

    def show_notes(self, notes=None, ids=None, max_lines=10, quiet=False):
        if notes is None:
            notes = []
        if ids is not None:
            notes.extend(self.get_notes(ids))
        for note in notes:
            note.show(max_lines=max_lines, quiet=quiet)

    def search_notes(
            self, search_fields, datetime_range=None, exact=False,
            quiet=False):
        # search the index for the terms provided
        notes = self._token_search(search_fields)

        # refine to exact matches if requested
        if exact:
            notes = self._exact_search(search_fields, notes=notes)

        # refine to datetime range if specified
        notes = [
            note for note in notes
            if datetime_range[0] < note.datetime < datetime_range[1]]

        # sort notes by timestamp
        notes.sort(key=lambda note: note.timestamp)

        # display matching notes
        self.show_notes(notes=notes, quiet=quiet)

    def get_notes(self, ids=None, datetime_range=(None, None)):
        if ids is None:
            notes = self.table.scan()['Items']
        elif not len(ids):
            notes = []
        else:
            notes = aws.dynamodb.batch_get_item(
                RequestItems={
                    self.table.name: {
                        'Keys': [{'id': note_id} for note_id in ids],
                    },
                },
            )['Responses'][self.table_name]

        return [Note.from_dict(note) for note in notes]

    def _initialize_tables(self):
        if not self.exists:
            self.create_table()

        if not self.index.exists:
            self.index.create_table()

    def _exact_search(self, search_fields, notes=None):
        if notes is None:
            notes = self._token_search(search_fields)
        exact_match_notes = []
        for note in notes:
            if self._search_fields_in_note(search_fields, note):
                exact_match_notes.append(note)
        return exact_match_notes

    @staticmethod
    def _search_fields_in_note(field_searches, note):
        for field, search_terms in field_searches.items():
            for search_term in search_terms:
                if search_term not in getattr(note, field):
                    return False
        return True

    def _token_search(self, search_fields):
        token_notes = []
        for field, search in search_fields.items():

            tokens = Text(' '.join(search)).tokens
            responses = self.index.query_token_ids(tokens)

            for response in responses:
                token_note_ids = response.get(
                    index.NoteIndex.get_field_name(field))
                if token_note_ids:
                    token_notes.append(set(token_note_ids))

        note_ids = (
            None if not token_notes else list(set.intersection(*token_notes)))

        return self.get_notes(ids=note_ids)
