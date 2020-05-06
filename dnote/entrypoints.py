import os
import sys
import tempfile
import subprocess
import fileinput

from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    description = 'Add a note to the dNote database'

    def run(self, options):
        collection = notes.NoteCollection()
        collection.init_tables()
        body = self._launch_editor()
        if body:
            collection.add_note(
                body, name=options.name, tags=options.tags)

    def build_parser(self, parser):
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')
        parser.add_argument('--file', '-f')

    @staticmethod
    def _launch_editor():
        editor = os.environ.get('EDITOR', 'vim')
        args = [editor]
        note = sys.stdin.read() if not sys.stdin.isatty() else ''

        if editor == 'vim':
            args.append('+startinsert')

        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(note.encode())
            temp_file.flush()
            args.append(temp_file.name)
            subprocess.call(args)
            temp_file.seek(0)
            return temp_file.read().decode()

class FindNotesEntryPoint(common.EntryPoint):
    name = 'find'
    description = 'Search for notes in the dNote database'

    def run(self, options):
        collection = notes.NoteCollection()
        collection.init_tables()
        search_fields = {
            'name': options.name,
            'body': options.body,
            'tags': options.tags,
            'host': options.host,
        }

        # collection.date_search(options.range)
        collection.text_search(
            search_fields, exact=options.exact)

    def build_parser(self, parser):
        parser.add_argument('--id', '-i')
        parser.add_argument('--name', '-n')
        parser.add_argument('--body', '-b')
        parser.add_argument('--tags', '-t')
        parser.add_argument('--host', '-o')
        parser.add_argument('--range', '-r')
        parser.add_argument('--exact', '-e', action='store_true')


class ConfigEntryPoint(common.EntryPoint):
    name = 'config'
    description = 'Config settings for dNote'

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
