from . import common, notes


class NewNoteEntryPoint(common.EntryPoint):
    name = 'new'
    description = 'Add a note to the dNote database'

    def run(self, options):
        body = self._validate_body(options.body)

        collection = notes.NoteCollection()
        collection.add_note(
            body=body, name=options.name, tags=options.tags)

    def build_parser(self, parser):
        parser.add_argument('--body', '-b')
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')


class FindNotesEntryPoint(common.EntryPoint):
    name = 'find'
    description = 'Search for notes in the dNote database'

    def run(self, options):
        datetime_range = self._validate_range(options.range)
        search_fields = self._validate_search_fields({
            'name': options.name,
            'body': options.body,
            'tags': options.tags,
            'host': options.host,
        })

        collection = notes.NoteCollection()
        collection.search_notes(
            search_fields=search_fields, datetime_range=datetime_range,
            exact=options.exact, quiet=options.quiet)

    def build_parser(self, parser):
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
        ids = self._validate_ids(options.ids)

        collection = notes.NoteCollection()
        collection.delete_notes(ids)

    def build_parser(self, parser):
        parser.add_argument('--ids', '-i', nargs='+')


class EditNoteEntryPoint(common.EntryPoint):
    name = 'edit'
    description = 'Updates a note from the dNote database'

    def run(self, options):
        ids = self._validate_ids(options.id)
        if len(ids) > 1:
            raise ValueError('More than one id specified ...')
        if not len(ids):
            return

        collection = notes.NoteCollection()
        note = collection.get_notes(ids)[0]
        if not note:
            raise ValueError('Specified note does not exist ...')

        body = self._validate_body(options.body, prompt=note.body)
        collection.update_note(
            note=note, body=body, name=options.name, tags=options.tags)

    def build_parser(self, parser):
        parser.add_argument('--id', '-i')
        parser.add_argument('--body', '-b')
        parser.add_argument('--name', '-n')
        parser.add_argument('--tags', '-t', nargs='+')


class ShowNoteEntryPoint(common.EntryPoint):
    name = 'show'
    description = 'Displays a full note from the dNote database'

    def run(self, options):
        ids = self._validate_ids(options.ids)
        collection = notes.NoteCollection()
        collection.show_notes(ids=ids)

    def build_parser(self, parser):
        parser.add_argument('--ids', '-i', nargs='+')
        parser.add_argument('--max', '-m', type=int)


class UndoEntryPoint(common.EntryPoint):
    name = 'undo'
    description = 'Undoes the previous dNote edit or new command'

    def run(self, options):
        raise NotImplementedError

    def build_parser(self, parser):
        pass


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
