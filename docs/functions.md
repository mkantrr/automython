# Functions

## `save(path[optional], input_string[optional], horizontal[optional])`

The `save()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.save()`.

When executed, this function will, by default, save the automata object's graph to a file named after the variable name, i.e. `fa.png`.

- If the `path` parameter is specified, which is a string, the function will save the automata object's graph to that path/file name.
- If the `input_string` parameter is specified, which is a string containing the input symbols from the automata's object, the function will save the automata object's graph with a gradient of transitions taken through the input_string as a test string. The transitions gradient in the saved file will be green if the string is accepted, or red if the string is rejected. This is, in essence, the visual representation of [`test()`](#`test(input_string)`) 
- If the `horizontal` parameter is specified, which is a boolean, the function will save the automata object's graph in horizontal dimensions if `True` or vertical dimensions if `False`.

## `definition()`

The `definition()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.definition()`.

When executed, this function will return a string representation of the transition table-like structure of the automata object. You can use something like `print(fa.definition())` to print it to standard out.

- The → symbol denotes the initial state.
- The * symbol denotes an accepting state.

## `test(input_string)`

The `test()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.test("1010")`.

When executed, this function will return a string representation of the transition steps took through the automata. It returns this as a table-like structure, and also returns whether or not the input string is accepted or rejected by the automata. This is, in essense, the textual representation of [`definition()`](#`definition()`)

- The `input_string` argument must be a string.
- The → symbol denotes the initial state.
- The * symbol denotes an accepting state.

## `open(path[optional])`

When executed, this function will, by default, open a file called `M.png` in the same directory as when `automython` command that was run.

- If the function is executed in the same way as `save()`, i.e. `fa.open()`, the default file it will open will be the variable it is called on (`fa.png`).
- If the `path` parameter is specified, which is a string, the function will open the specified file in the OS native viewer. If the path is specified **and** the function is called on a variable, the variable it is called on is obsolete, and the path parameter takes precedence.

## `print(args[optional])`

The `print()` function is intended to be used as a standalone function, similar to how it is used in Python. If the function is called on a variable, the variable is obsolete. If the function is assigned to a variable, the variable will store `None`.

- If the `args` parameter is passed, this can be a variable, function call, expression, or "native" type, the string representation of whatever is passed in is printed straight through Python's `print()` function.
- If `args` is not passed, it will run the equivalent of `print('')` in Python.