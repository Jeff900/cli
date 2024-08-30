"""This module aims to provide a shell for python applications, which can be
configured per application. The shell on itself listen to input, creates a
dictionary with commands and arguments and passes it to the application.
"""

import re
import json


__version__ = '0.0.3'


class Settings:
    """Gets settings from cli.json. See README file for explanation per
    setting. Sets settings to a dictionary.
    """

    def __init__(self, path='./cli.json'):
        self.path = path
        self.data = self.read_json()

    def read_json(self):
        """Reads json data.
        """
        with open(self.path, 'r') as f:
            data = json.load(f)
        return data

    def print_settings(self):
        """For testing purposes and checking settings.
        """
        if self.data:
            for key, value in self.data.items():
                print(key, '-', value)
        else:
            print('Can\'t find self.data')


class Args:
    """This class handles arguments given with the prompt handled by the Prompt
    class.
    """

    def __init__(self, settings, args):
        self.args = args
        self.pos_args = []
        self.kw_args = {}

    def init_args(self):
        """Loop over al args, get positional first, then handle flags.
        """
        pos_arg = True
        for arg in self.args:
            if arg.startswith(settings.data['multi_char_arg']):
                # assume double-dashed arg
                pos_arg = False
            elif arg.startswith(settings.data['single_char_arg']):
                # assume single-dashed arg
                pos_arg = False
            elif pos_arg is True:
                # assume positional arg
                self.pos_args.append(arg)


class Prompt:
    """Prompt class handles the input. It extracts all parts from the actual
    command up to the flags with its arguments.
    """

    def __init__(self, settings):
        self.prefix = settings.data['prefix']
        self.args = Args()

    def clean_prompt(self, i):
        """Clean prompt from trailing and duplicate spaces.
        Returns String"""
        c = " ".join(re.split("\s+", i, flags=re.UNICODE)).strip()
        return c

    def parse_prompt(self, input_cleaned):
        """Split cleaned input on spaces.
        Returns a List."""
        return input_cleaned.split(' ')

    def parse_arguments(self, input_parsed):
        """Loops over all items in parsed prompt but ignores first. On flag
        (double dash `--`) it will create a Dict key. Following non-flag items
        will be added as values. Until a new flag is found etc.
        Returns Dictionary
        """
        args = {}
        for arg in input_parsed[1:]:
            if arg.startswith('--'):
                current_arg = arg
                args[arg] = []
            else:
                args[current_arg].append(arg)
        return args

    def run(self, settings):
        """Runs main program until stop command is entered.
        """
        while True:
            i = input(self.prefix)
            if i.lower().strip() in settings.data['quit_commands']:
                break
            else:
                input_cleaned = self.clean_prompt(i)
                input_parsed = self.parse_prompt(input_cleaned)
                command = input_parsed[0]
                args = self.parse_arguments(settings, input_parsed)
                print(args)
                # func(self)

if __name__ == '__main__':
    try:
        settings = Settings()
    except Exception as exc:
        print(exc)

    prompt = Prompt(settings)
    prompt.run(settings)
