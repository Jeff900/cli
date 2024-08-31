# cli
Python module to handle user input from the command line in a REPL like fashion.

# Usage

# Settings file
* quit_commands - Default: ['exit', 'quit', 'stop', 'q']. You can add any single word string pattern as quit command, as long as it doesn't collide with application commands. Defaults can be overwritten. Exit commands are case insensitive.
* prefix - Default: '> '. prefix sets the first characters shown in shell. They are ignored when reading input. Set as empty string if no prefix is desired.
* single_char_arg - Default: '-'
* multi_char_arg - Default: '--'