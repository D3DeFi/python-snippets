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
    """Attaches argument to a __dict__ attribute within a specific function or method."""
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func
    return _decorator

# Example command with methods decored
# docstring of a class will be used as a subcommand help
class ListActions(object):
    """list sub-command help."""

    def router(self, args):
        self.list_items(args.pretty or None)

    @args('--pretty', action='store_true', help='display pretty output')
    def list_items(self, pretty):
        if pretty:
            for item in ITEMS:
                print(item)
        else:
            print(ITEMS)

# Example command with methods decored
# docstring of a class will be used as a subcommand help
class ShowActions(object):
    """show sub-command help."""

    # specify arguments only once
    @args('--name', type=str, metavar='<name>', help='name of a displayed item')
    def router(self, args):
        if 'type' in args.__dict__ and args.__dict__['type'] == True:
            self.show_item_type(args.name)
        else:
            self.show_item(args.name)

    def show_item(self, name):
        print(ITEMS.get(name, None) or 'Key not found!')

    @args('--type', action='store_true', help='display type of a shown item')
    def show_item_type(self, name):
        print(type(ITEMS.get(name, None)) or 'Key not found!')

# definition in which commands to parse arguments
CATEGORIES = {
    'show': ShowActions,
    'list': ListActions
}

def get_argument_parser(description=None):
    """Iterates over function's or method's __dict__['args'] variable to load arguments into arg parser."""
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
    for category in CATEGORIES:
        obj = CATEGORIES[category]()

        # use docstring as a help and define subcommand in argument parser
        desc = getattr(obj, '__doc__', None)
        sub_parser = subparsers.add_parser(category, help=desc)

        # get all class public methods
        category_methods = [getattr(obj, m) for m in dir(obj) if callable(getattr(obj, m)) and not m.startswith('_')]
        # iterate over callable methods and load defined arguments
        arguments = dict()
        for method in category_methods:
            for args, kwargs in getattr(method, 'args', []):
                # if argument does not have 'dest' parameter, it's name will be used instead
                dest = kwargs.get('dest', None) or args[0].lstrip('-')
                if dest not in arguments:
                    sub_parser.add_argument(*args, **kwargs)

                # make sure only first argument is used if two or more are found with the same name
                arguments.setdefault(dest, [args, kwargs])

    return parser


if __name__ == '__main__':
    parser = get_argument_parser(description='Example parser')
    args = parser.parse_args()

    # load appriopiate category, argparse will handle correct output for us
    # TODO: create better logic for matching methods/functions with arguments
    category = CATEGORIES[args.subcommand]()
    category.router(args)
