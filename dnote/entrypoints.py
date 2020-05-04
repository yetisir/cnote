from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    description = 'Add a note to the dNote database'

    def run(self, options):
        table = notes.NoteTable()
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
        parser.add_argument('search')


class ConfigEntryPoint(common.EntryPoint):
    name = 'config'
    description = 'Config settings for dNote'

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
