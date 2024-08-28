import re


__version__ = '0.0.2'


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
        while True:
            i = input(self.prefix)
            if i.lower().strip() in ['exit', 'quit', 'stop', 'q']:
                break
            else:
                input_cleaned = self.clean_prompt(i)
                input_parsed = self.parse_prompt(input_cleaned)
                args = self.parse_arguments(input_parsed)
                func(self)
