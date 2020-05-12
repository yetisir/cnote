import sys
import termios
import re

import click

from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    aliases = ['n']
    description = 'Add a note to the dNote database'

    def run(self, options):
        collection = notes.NoteCollection()
        collection.init_tables()

        body = options.body if options.body else launch_editor()

        collection.add_note(
            body, name=options.name, tags=options.tags)

    def build_parser(self, parser):
        parser.add_argument('--body', '-b')
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
            search_fields, exact=options.exact, quiet=options.quiet)

    def build_parser(self, parser):
        parser.add_argument('--id', '-i')
        parser.add_argument('--range', '-r', nargs='+')
        parser.add_argument('--name', '-n', nargs='+')
        parser.add_argument('--body', '-b', nargs='+')
        parser.add_argument('--tags', '-t', nargs='+')
        parser.add_argument('--host', '-o', nargs='+')
        parser.add_argument('--exact', '-e', action='store_true')
        parser.add_argument('--quiet', '-q', action='store_true')


class RemoveNoteEntryPoint(common.EntryPoint):
    name = 'remove'
    aliases = ['r', 'rm']
    description = 'Removes notes from the dNote database'

    def run(self, options):
        piped_input = sys.stdin.read() if not sys.stdin.isatty() else ''
        ids = []

        if piped_input:
            ids.extend(piped_input.split())
        if options.ids:
            ids.extend(options.ids)

        ids = [id for id in ids if re.match(r'([a-fA-F\d]{32})', id)]

        collection = notes.NoteCollection()
        collection.init_tables()
        collection.delete_notes(ids)

    def build_parser(self, parser):
        parser.add_argument('--ids', '-i', nargs='+')


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

    stty_attrs = termios.tcgetattr(sys.stdout)

    note = sys.stdin.read() if not sys.stdin.isatty() else ''
    note = click.edit(note, require_save=False)

    termios.tcsetattr(sys.stdout, termios.TCSAFLUSH, stty_attrs)
    return note
