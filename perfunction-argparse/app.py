#!/usr/bin/env python

import argparse

# Example database
ITEMS = {
    'a': 'test1',
    'b': 'test2',
    'c': 'test3',
    'd': 'test4'
}

# decorator for argument definitions
def args(*args, **kwargs):
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func
    return _decorator

# Example command with methods decored
# docstring of a class will be used as a subcommand help
class ListActions(object):
    """list sub-command help."""

    @args('--pretty', action='store_true', help='display pretty output')
    def list_items(self, pretty):
        if pretty:
            for item in ITEMS:
                print(item)

# Example command with methods decored
# docstring of a class will be used as a subcommand help
class ShowActions(object):
    """show sub-command help."""

    @args('--name', type=str, metavar='<name>', help='name of a displayed item')
    def show_item(self, name):
        print(ITEMS.get(key, None) or 'Key not found!')

    @args('--name', type=str, metavar='<name>', help='name of a displayed item')
    @args('--type', action='store_true', help='display type of a shown item')
    def show_item_type(self, name, type):
        print(type(ITEMS.get(key, None)) or 'Key not found!')

# definition in which commands to parse arguments
CATEGORIES = {
    'show': ShowActions,
    'list': ListActions
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    for category in CATEGORIES:
        obj = CATEGORIES[category]()
        # use docstring as a help and define subcommand in argument parser
        desc = getattr(obj, '__doc__', None)
        sub_parser = subparsers.add_parser(category, help=desc)

        # get all class public methods
        category_methods = [getattr(obj, m) for m in dir(m) if callable(getattr(obj, m)) and not m.startswith('_')]
        # iterate over callable methods and load defined arguments
        for args, kwargs in [getattr(func, 'args', []) for func in category_methods]:
            pass

    args = parser.parse_args()
