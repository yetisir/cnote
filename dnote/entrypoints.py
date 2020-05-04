import tempfile
import subprocess

from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    description = 'Add a note to the dNote database'

    def run(self, options):
        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            subprocess.call(['vim', '+startinsert', tf.name])
            tf.seek(0)
            note = tf.read()

        table = notes.noteTable()
        table.add_note(note)

    def build_parser(self, parser):
        pass


class SearchNotesEntryPoint(common.EntryPoint):
    name = 'search'
    description = 'Search for notes in the dNote database'

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
