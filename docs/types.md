# Types

## Integer

Integers in Automython act the same as `int`s in Python.

## String

Strings in Automython act the same as `str`s in Python. You can use both `'` or `"` symbols to enclose them, just like Python.

## Boolean

Booleans in Automython act the same as `bool`s in Python.

## Dictionary

Dictioniaries in Automython act the same as `dict`s in Python. The only difference in the more limited support types for what you can assign to keys to only Automython's "native" types, and no other Python types that are not included.

## Set

Sets in Automython act the same as `set`s in Python. The only difference is the more limited support types for what you can assign to keys to only Automython's "native" types, and no other Python types that are not included.

## Tuple

Tuples in Automython act the same as `tuple`s in Python. The only difference is the more limited support, as you cannot perform most of the Python tuple functions and slick scripting you can here. They are built for a specific purpose, and it is moreso to be integrated with the computational theory concepts below.

## DFA
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

## NFA
**Non-deterministic Finite Automaton**:

The NFA object in Automython must resemble this syntax:
```python
NFA(states, input_symbols, transitions, initial_state, final_states)
```
It must **also** be assigned to a variable; it cannot be treated as an expression, i.e.:
```python
nfa = NFA(states, input_symbols, transitions, initial_state, final_states)
```

- The `states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `input_symbols` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `transitions` argument is a Dictionary. This can be either a Dictionary in the argument, or a variable that stores a Dictionary. The values of each key maps to an input symbol as a key to a Set of states.
- The `initial_state` argument is a String. This can be either a String in the argument, or a variable that stores a String.
- The `final_states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.

## DTM
**Deterministic Turing Machine**:

The DFA object in Automython must resemble this syntax:
```python
DTM(states, input_symbols, tape_symbols, transitions, initial_state, blank_symbol, final_states)
```
It must **also** be assigned to a variable; it cannot be treated as an expression, i.e.:
```python
dtm = DTM(states, input_symbols, tape_symbols, transitions, initial_state, blank_symbol, final_states)
```

- The `states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.
- The `input_symbols` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set. These symbols are all Strings, and are the only symbols that can exist on the tape before the Turing machine begins its run.
- The `tape_symbols` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set. These symbols are all Strings that are able to be read and written on the tape.
- The `transitions` argument is a Dictionary. This can be either a Dictionary in the argument, or a variable that stores a Dictionary. The values of each key maps to an input symbol as a key to a Tuple of strings denoting the new state, write symbol, and direction to move on the tape.
- The `initial_state` argument is a String. This can be either a String in the argument, or a variable that stores a String.
- The `blank_symbol` argument is a String. This can be either a String in the argument, or a variable that stores a String. This is the symbol on the tape that fills theoretical space on the tape where the input is not.
- The `final_states` argument is a Set. This can be either a Set in the argument, or a variable that stores a Set.