"""This module aims to provide a shell for python applications, which can be
configured per application. The shell on itself listen to input, creates a
dictionary with commands and arguments and passes it to the application.
"""

import re, json


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


class Prompt:
    """Prompt class handles the input. It extracts all parts from the actual
    command up to the flags with its arguments.
    """

    def __init__(self, prefix='> '):
        self.prefix = prefix
        # self.input_cleaned = Prompt.clean_prompt(i)
        # self.input_parsed = self.parse_prompt()
        # self.command = self.input_parsed[0]
        # self.parse_arguments()

    def clean_prompt(self, i):
        """Clean prompt from trailing and duplicate spaces.
        Returns String"""
        c = " ".join(re.split("\s+", i, flags=re.UNICODE)).strip()
        self.input_cleaned = c

    def parse_prompt(self, input_cleaned):
        """Split cleaned input on spaces.
        Returns a List."""
        self.input_parsed = self.input_cleaned.split(' ')

    def parse_arguments(self, input_parsed):
        """Loops over all items in parsed prompt but ignores first. On flag
        (double dash `--`) it will create a Dict key. Following non-flag items
        will be added as values. Until a new flag is found etc.
        Returns Dictionary
        """
        self.args = dict()
        for arg in self.input_parsed[1:]:
            if arg.startswith('--'):
                current_arg = arg
                self.args[arg] = []
            else:
                self.args[current_arg].append(arg)
        self.args

    def run(self, func):
        """Runs main program until stop command is entered.
        """
        try:
            settings = Settings()
        except:
            pass
        while True:
            i = input(self.prefix)
            if i.lower().strip() in settings.data['quit_commands']:
                break
            else:
                input_cleaned = self.clean_prompt(i)
                input_parsed = self.parse_prompt(input_cleaned)
                args = self.parse_arguments(input_parsed)
                func(self)
