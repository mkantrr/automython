# Automython

*Copyright 2024 Matthew Kanter*  
*Released under the MIT license*

[![build](https://github.com/mkantrr/automython/actions/workflows/build.yml/badge.svg)](https://github.com/mkantrr/automythonactions/workflows/build.yml)

The **Automython** interpreter is a simple programming language that interprets its source code to Python as its target code to help understand and visualize automata theory.

This project originially started out as my senior capstone project at umw i would complete to graduate with university honors. it originally started out as a proposal to create a whole new programming language, writing a compiler that translates my designed syntax into machine code to run a finite automata (either a deterministic finite automata (DFA) or non-deterministic (NFA), or if time permitted since it was only a one semester project a Turing machine) and output to the user a graph visualization of the inputted 5-tuple automata, whether an optional input word was accepted or rejected by the automata, and a table of transition functions/steps.

It slowly evolved as I worked closely with my fantastic professor, [**Dr. Andrew Marshall**](https://www.marshallandrew.net/) into creating an interpreter to Python to make use of pre-existing visualization libraries ([automata-lib](https://github.com/caleb531/automata), [visual-automata](https://github.com/lewiuberg/visual-automata)) and the small scope of the operations this language would have to perform. After all, what's the point of creating a whole new programming language that only performs one basic function when you could instead create a programming language that translates to a more widely used and broader use case programming language to make use of already written higher level logic? Point proven, nobody wants to write assembly. *shudders*

Thank you to [**Leonardo Giordani**](https://www.thedigitalcatonline.com/pages/about.html) for his TDD work in a simple calculator interpreter in Python that was heavily adapted for this package.

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

- [`Integer`](./types.md#Integer)
- [`String`](./types.md#String)
- [`Boolean`](./types.md#Boolean)
- [`Dictionary`](./types.md#Dictionary)
- [`Set`](./types.md#Set)

Computational theory objects that are supported are:
- [`DFA`](./types.md#DFA) (i.e. `DFA(states, input_symbols, transitions, initial_state, final_states, allow_partial[optional]: bool`)
- [`NFA`](./types.md#NFA) (i.e. `NFA(states, input_symbols, transitions, initial_state, final_states)`)
The parameters within these calls can be substituted for any native types supported.

[Variables](./types.md#Variable) exist. Variables are defined such that `x = {'s1', 's2'}` assigns that set to the `x` variable.

Function calls exist too. Function calls return a value, usually only a string. You can assign a variable to these function_calls.
The available functions to use are:

- [`save()`](<./functions.md#`save(path[optional], input_string[optional], horizontal[optional])`>)
- [`definition()`](./functions.md#`definition()`)
- [`test()`](./functions.md#`test(input_string)`)
- [`open()`](./functions.md#`open(path[optional])`)
- [`print()`](./functions.md#`print(args[optional])`)

Each function can be wrapped in `print()` to display the value returned from each function.
