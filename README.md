# Automython

*Copyright 2024 Matthew Kanter*  
*Released under the MIT license*

[![build](https://github.com/mkantrr/automython/actions/workflows/build.yml/badge.svg)](https://github.com/mkantrr/automythonactions/workflows/build.yml)

## `https://pypi.org/project/automython`

The **Automython** interpreter is a simple programming language that interprets its source code to Python as its target code to help understand and visualize automata theory.

This project originially started out as my senior Capstone project at UMW I would complete to graduate with University Honors. It originally started out as a proposal to create a whole new programming language, writing a compiler that translates my designed syntax into machine code to run a finite automata (either a deterministic finite automata (DFA) or non-deterministic (NFA), or if time permitted since it was only a one semester project a Turing machine) and output to the user a graph visualization of the inputted 5-tuple automata, whether an optional input word was accepted or rejected by the automata, and a table of transition functions/steps.

It slowly evolved as I worked closely with my fantastic professor, [**Dr. Andrew Marshall**](https://www.marshallandrew.net/) into creating an interpreter to Python to make use of pre-existing visualization libraries ([automata-lib](https://github.com/caleb531/automata), [visual-automata](https://github.com/lewiuberg/visual-automata)) and the small scope of the operations this language would have to perform. After all, what's the point of creating a whole new programming language that only performs one basic function when you could instead create a programming language that translates to a more widely used and broader use case programming language to make use of already written higher level logic? Point proven, nobody wants to write assembly. *shudders*

Thank you to [**Leonardo Giordani**](https://www.thedigitalcatonline.com/pages/about.html) for his TDD work on a simple calculator interpreter in Python that was heavily adapted for this package.

This package requires Python 3.8 or newer.

## Prerequisites

```sh
pip install 'automata-lib[visual]'
pip install pandas
pip install ipython
```

## Installing

You can install the latest version of Automython via `pip`:

```sh
pip install automython
```

## Usage

Automython can be used in two ways, similar to Python. It can be used as a command line interface or by passing in it's own readable `.theory` file type to read.

### CLI
Automython can be used similarly to how `python` can be on the command line. Simply run to bring up the interface:

```sh
automython
```
Refer to the next section for specifics on syntax.

### File Syntax
To use this package once installed, you need to have a file with the extension `.theory` to run it on.
This `.theory` file has very simiilar syntax definitions to Python, however with some limitations as the scope is not quite that large.

All types in the `.theory` file operate the same as Python. The "native" types (supported types that are converted to Python) for Automython are:

- [`Integer`](#Integer)
- [`String`](#String)
- [`Boolean`](#Boolean)
- [`Dictionary`](#Dictionary)
- [`Set`](#Set)

Computational theory objects that are supported are:

- [`DFA`](#DFA) (i.e. `DFA(states, input_symbols, transitions, initial_state, final_states, allow_partial[optional]: bool`)
- [`NFA`](#NFA) (i.e. `NFA(states, input_symbols, transitions, initial_state, final_states)`)
The parameters within these calls can be substituted for any native types supported.

[Variables](#Variable) exist. Variables are defined such that `x = {'s1', 's2'}` assigns that set to the `x` variable.

Function calls exist too. Function calls return a value, usually only a string. You can assign a variable to these function_calls.
The available functions to use are:

- [`save()`](<#`save(path[optional], input_string[optional], horizontal[optional])`>)
- [`definition()`](#`definition()`)
- [`test()`](#`test(input_string)`)
- [`open()`](#`open(path[optional])`)
- [`print()`](#`print(args[optional])`)

Each function can be wrapped in `print()` to display the value returned from each function.

### Types

#### Integer

Integers in Automython act the same as `int`s in Python.

#### String

Strings in Automython act the same as `string`s in Python. You can use both `'` or `"` symbols to enclose them, just like Python.

#### Boolean

Booleans in Automython act the same as `bool`s in Python.

#### Dictionary

Dictioniaries in Automython act the same as `dict`s in Python. The only difference in the more limited support types for what you can assign to keys to only Automython's "native" types, and no other Python types that are not included.

#### Set

Sets in Automython act the same as `set`s in Python. The only difference in the more limited support types for what you can assign to keys to only Automython's "native" types, and no other Python types that are not included.

#### DFA
**Deterministic Finite Automaton**:

The DFA object in Automython must resemble this syntax:
```python
DFA(states, input_symbols, transitions, initial_state, final_states, allow_partial[optional]: bool)
```
It must **also** be assigned to a variable; it cannot be treated as an expression, i.e.:
```python
dfa = DFA(states, input_symbols, transitions, initial_state, final_states, allow_partial[optional]: bool)
```

- The `states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `input_symbols` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `transitions` argument is a Dictionary. This can be either a Dictionary in the argument, or a variable that stores a Dictionary. The values of each key maps to an input symbol as a key to a String denoting the state.
- The `initial_state` argument is a String. This can be either a String in the argument, or a variable that stores a String.
- The `final_states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `allow_partial` argument is optional, and is a Boolean. The default value is `False` if it is not specified, but if it is specified, it allows the DFA to be validated as a partial DFA. 

#### NFA
**Non-deterministic Finite Automaton**:

The NFA object in Automython must resemble this syntax:
```python
NFA(states, input_symbols, transitions, initial_state, final_states)
```
It must **also** be assigned to a variable; it cannot be treated as an expression, i.e.:
```python
nfa = NFA(states, input_symbols, transitions, initial_state, final_states, allow_partial[optional]: bool)
```

- The `states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `input_symbols` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `transitions` argument is a Dictionary. This can be either a Dictionary in the argument, or a variable that stores a Dictionary. The values of each key maps to an input symbol as a key to a Set of states.
- The `initial_state` argument is a String. This can be either a String in the argument, or a variable that stores a String.
- The `final_states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.

### Functions

#### `save(path[optional], input_string[optional], horizontal[optional])`

The `save()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.save()`.

When executed, this function will, by default, save the automata object's graph to a file named after the variable name, i.e. `fa.png`.

- If the `path` parameter is specified, which is a string, the function will save the automata object's graph to that path/file name.
- If the `input_string` parameter is specified, which is a string containing the input symbols from the automata's object, the function will save the automata object's graph with a gradient of transitions taken through the input_string as a test string. The transitions gradient in the saved file will be green if the string is accepted, or red if the string is rejected. This is, in essence, the visual representation of [`test()`](#`test(input_string)`) 
- If the `horizontal` parameter is specified, which is a boolean, the function will save the automata object's graph in horizontal dimensions if `True` or vertical dimensions if `False`.

#### `definition()`

The `definition()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.definition()`.

When executed, this function will return a string representation of the transition table-like structure of the automata object. You can use something like `print(fa.definition())` to print it to standard out.

- The → symbol denotes the initial state.
- The * symbol denotes an accepting state.

#### `test(input_string)`

The `test()` function can only be used when calling it on an automata variable already assigned, i.e. `fa.test("1010")`.

When executed, this function will return a string representation of the transition steps took through the automata. It returns this as a table-like structure, and also returns whether or not the input string is accepted or rejected by the automata. This is, in essense, the textual representation of [`definition()`](#`definition()`)

- The `input_string` argument must be a string.
- The → symbol denotes the initial state.
- The * symbol denotes an accepting state.

#### `open(path[optional])`

When executed, this function will, by default, open a file called `M.png` in the same directory as when `automython` command that was run.

- If the function is executed in the same way as `save()`, i.e. `fa.open()`, the default file it will open will be the variable it is called on (`fa.png`).
- If the `path` parameter is specified, which is a string, the function will open the specified file in the OS native viewer. If the path is specified **and** the function is called on a variable, the variable it is called on is obsolete, and the path parameter takes precedence.

#### `print(args[optional])`

The `print()` function is intended to be used as a standalone function, similar to how it is used in Python. If the function is called on a variable, the variable is obsolete. If the function is assigned to a variable, the variable will store `None`.

- If the `args` parameter is passed, this can be a variable, function call, expression, or "native" type, the string representation of whatever is passed in is printed straight through Python's `print()` function.
- If `args` is not passed, it will run the equivalent of `print('')` in Python.
