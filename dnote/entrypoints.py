from . import common, notes
from .config import config


class AddNoteEntryPoint(common.EntryPoint):
    name = 'add'
    description = 'Create a new note to the dNote database'

    def run(self, options):
        table = notes.NoteTable(endpoint=config.dynamodb_endpoint)
        table.add_note(options.note)

    def build_parser(self, parser):
        parser.add_argument('note', nargs='?')


class FindNotesEntryPoint(common.EntryPoint):
    name = 'find'
    description = 'Search for notes in the dNote database'

    def run(self, options):
        table = notes.NoteTable()
        table.find_notes(options.search)

    def build_parser(self, parser):
        parser.add_argument('search', nargs='?')


class ConfigEntryPoint(common.EntryPoint):
    name = 'config'
    description = 'Config settings for dNote'

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
