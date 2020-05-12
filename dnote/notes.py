import hashlib
import socket
import getpass
from datetime import datetime

import nltk
import dateparser

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
        return datetime.fromtimestamp(self.timestamp)

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

    def show(self, quiet=False):
        if quiet:
            print(self.id)
            return
        print(f'{self.id} ({self.name}) [{self.host}@{self.datetime}]')
        for line in self.body.split('\n'):
            print(f'\t{line}')

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
    table_name = 'dnote'  # TODO: get from config

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
        if not note.body:
            return
        self.table.put_item(Item=note.to_dict())
        self.index.add_note(note)
        note.show()

    def get_note_from_id(self, id):
        response = self.table.get_item(Key={'id': id})
        return Note.from_dict(response)

    def get_notes_from_ids(self, ids, datetime_range=(None, None)):
        notes = aws.dynamodb.batch_get_item(
            RequestItems={
                self.table.name: {
                    'Keys': [{'id': note_id} for note_id in ids],
                },
            },
        )['Responses'][self.table_name]

        return [Note.from_dict(note) for note in notes]

    def delete_notes(self, ids):
        with self.table.batch_writer() as batch:
            for id in ids:
                batch.delete_item(Key={'id': id})

    def get_notes_from_scan(self):
        notes = self.table.scan()['Items']
        return [Note.from_dict(note) for note in notes]

    @staticmethod
    def show_notes(notes, quiet=False):
        for note in notes:
            note.show(quiet=quiet)

    def text_search(self, field_searches, datetime_range=None, exact=False, quiet=False):
        field_searches = {
            field: searches for field, searches in field_searches.items()
            if searches}

        datetime_range = self._validate_range(datetime_range)
        print(datetime_range)
        notes = self.get_matching_search_notes(field_searches)

        if exact:
            notes = self._exact_match_notes(notes, field_searches)

        notes = [note for note in notes if datetime_range[0] < note.datetime < datetime_range[1]]

        if not notes:
            return
        notes.sort(key=lambda note: note.timestamp)
        self.show_notes(notes, quiet=quiet)

    def _validate_range(self, datetime_range):
        now = datetime.utcnow()
        if not datetime_range:
            return (datetime.fromtimestamp(0), now)
        dates = [dateparser.parse(date, settings={'TO_TIMEZONE': 'UTC'}) for date in datetime_range]
        if None in dates:
            raise ValueError('Unable to parse date range')

        if len(dates) == 1:
            end = dates[0]
            start = now
        elif len(dates) == 2:
            end = max(dates)
            start = min(dates)

        return (start, end)


    def get_matching_search_notes(self, field_searches):
        if not field_searches:
            return self.get_notes_from_scan()

        search_map = self._create_search_map(field_searches)

        note_id_sets = []

        for field_search_map in search_map.values():
            for note_ids in field_search_map.values():
                note_id_sets.append(note_ids)

        if not note_id_sets:
            return []

        all_note_ids = set.intersection(*note_id_sets)

        if not all_note_ids:
            return []

        return self.get_notes_from_ids(all_note_ids)

    def _exact_match_notes(self, notes, field_searches):
        exact_match_notes = []
        for note in notes:
            if self._all_in_note(field_searches, note):
                exact_match_notes.append(note)
        return exact_match_notes

    @staticmethod
    def _all_in_note(field_searches, note):
        for field, search_terms in field_searches.items():
            for search_term in search_terms:
                if search_term not in getattr(note, field):
                    return False
        return True

    def _create_search_map(self, fields):
        search_map = {}
        for field, search in fields.items():

            tokens = Text(' '.join(search)).tokens
            responses = self.index.query_token_ids(tokens)

            field_search_map = {}
            for response in responses:
                token_note_ids = response.get(
                    index.NoteIndex.get_field_name(field))
                if not token_note_ids:
                    continue
                field_search_map[tokens[response['id']]] = set(token_note_ids)

            search_map[field] = field_search_map

        return search_map
