from . import common, utils


class AddEntryPoint(common.EntryPoint):
    name = 'add'
    description = ''

    def run(self, options):
        pass

    def build_parser(self, parser):
        pass


class SearchEntryPoint(common.EntryPoint):
    name = 'add'
    description = ''

    def run(self, options):
        pass

    def build_parser(self, parser):
        parser.add_argument(
            'action', default='resume', const='resume', nargs='?',
            choices=self.actions.keys())


def initialize():
    return {cls.name: cls() for cls in common.EntryPoint.__subclasses__()}
