from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    description = 'Add a note to the dNote database'

    def run(self, options):
        table = notes.NoteTable()
        table.add_note(options.note)

    def build_parser(self, parser):
        parser.add_argument('note', nargs='?', type=str)


class FindNotesEntryPoint(common.EntryPoint):
    name = 'find'
    description = 'Search for notes in the dNote database'

    def run(self, options):
        table = notes.NoteTable()
        table.find_notes()

    def build_parser(self, parser):
        pass


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
