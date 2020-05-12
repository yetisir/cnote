import sys
import termios
import re

import click

from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
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
    description = 'Search for notes in the dNote database'

    def run(self, options):
        if options.range and len(options.range) > 2:
            raise ValueError('Number of range arguments exceeds 2')

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
            search_fields, exact=options.exact, quiet=options.quiet,
            datetime_range=options.range)

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
    name = 'rm'
    description = 'Removes notes from the dNote database'

    def run(self, options):
        ids = get_input_ids(options.ids)
        collection = notes.NoteCollection()
        collection.init_tables()
        collection.delete_notes(ids)

    def build_parser(self, parser):
        parser.add_argument('--ids', '-i', nargs='+')


class EditNoteEntryPoint(common.EntryPoint):
    name = 'edit'
    description = 'Updates a note from the dNote database'

    def run(self, options):
        ids = get_input_ids(options.ids)
        if len(ids) >= 1:
            raise ValueError('More than one id specified')
        collection = notes.NoteCollection()
        collection.init_tables()

        # TODO: update table

    def build_parser(self, parser):
        parser.add_argument('--id', '-i', required=True)
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')
        parser.add_argument('--open', '-o', action='store_true')


class ShowNoteEntryPoint(common.EntryPoint):
    name = 'show'
    description = 'Displays a full note from the dNote database'

    def run(self, options):
        pass

    def build_parser(self, parser):
        parser.add_argument('--id', '-i', required=True)


class ConfigEntryPoint(common.EntryPoint):
    name = 'config'
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


def get_input_ids(ids):
    piped_input = sys.stdin.read() if not sys.stdin.isatty() else ''
    ids = ids if ids else []

    regex = r'([a-fA-F\d]{32})'

    ids = [id for id in ids if re.match(regex, id)]
    for line in piped_input.split('\n'):
        if line.startswith('\t'):
            continue

        match = re.match(regex, line)
        if match:
            ids.append(match.group())

    return ids
