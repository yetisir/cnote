import os
import sys
import tempfile
import subprocess

from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    aliases = ['n']
    description = 'Add a note to the dNote database'

    def run(self, options):
        collection = notes.NoteCollection()
        collection.init_tables()
        body = launch_editor()
        if body:
            collection.add_note(
                body, name=options.name, tags=options.tags)

    def build_parser(self, parser):
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')
        parser.add_argument('--file', '-f')


class FindNotesEntryPoint(common.EntryPoint):
    name = 'find'
    aliases = ['f']
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


class RemoveNoteEntryPoint(common.EntryPoint):
    name = 'remove'
    aliases = ['r', 'rm']
    description = 'Removes a note from the dNote database'

    def run(self, options):
        pass

    def build_parser(self, parser):
        parser.add_argument('--id', '-i', nargs='+', required=True)


class EditNoteEntryPoint(common.EntryPoint):
    name = 'edit'
    aliases = ['e']
    description = 'Updates a note from the dNote database'

    def run(self, options):
        pass

    def build_parser(self, parser):
        parser.add_argument('--id', '-i', required=True)
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')
        parser.add_argument('--open', '-o', action='store_true')


class ShowNoteEntryPoint(common.EntryPoint):
    name = 'show'
    aliases = ['s']
    description = 'Displays a full note from the dNote database'

    def run(self, options):
        pass

    def build_parser(self, parser):
        parser.add_argument('--id', '-i', required=True)


class ConfigEntryPoint(common.EntryPoint):
    name = 'config'
    aliases = ['c', 'conf']
    description = 'Config settings for dNote'

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


def initialize():
    entry_points = {}
    for cls in common.EntryPoint.__subclasses__():
        entry_points[cls.name] = cls()
        for alias in cls.aliases:
            entry_points[alias] = cls()
    return entry_points


def launch_editor():
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
