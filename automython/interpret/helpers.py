from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.tm.dtm import DTM
from automata.tm.ntm import NTM
from automata.tm.mntm import MNTM
import interpret.tm_helpers as tm_helpers

import random
import copy
from forbiddenfruit import curse
from typing import Union
import pandas as pd
import subprocess, os, platform

def dict_deepcopy(self) -> dict:
    return copy.deepcopy(dict(self))

curse(dict, "deepcopy", dict_deepcopy)


def system_type():
    return platform.system()
  
def definition(*args):
    target_fa = args[0]
    table = None
    if isinstance(target_fa, DFA):
        table = make_dfa_table(target_fa)
    elif isinstance(target_fa, NFA):
        table = make_nfa_table(target_fa)
    elif isinstance(target_fa, tm_helpers.VisualDTM):
        table = make_dtm_table(target_fa)
    return table

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py
def make_dfa_table(target_fa) -> pd.DataFrame:
    initial_state = target_fa.initial_state
    final_states = target_fa.final_states

    table = {}

    for from_state, to_state, symbol in target_fa.iter_transitions():
        # Prepare nice string for from_state
        if isinstance(from_state, frozenset):
            from_state_str = str(set(from_state))
        else:
            from_state_str = str(from_state)

        if from_state in final_states:
            from_state_str = "*" + from_state_str
        if from_state == initial_state:
            from_state_str = "→" + from_state_str

        # Prepare nice string for to_state
        if isinstance(to_state, frozenset):
            to_state_str = str(set(to_state))
        else:
            to_state_str = str(to_state)

        if to_state in final_states:
            to_state_str = "*" + to_state_str

        # Prepare nice symbol
        if symbol == "":
            symbol = "λ"

        from_state_dict = table.setdefault(from_state_str, dict())
        from_state_dict.setdefault(symbol, set()).add(to_state_str)

    # Reformat table for singleton sets
    for symbol_dict in table.values():
        for symbol in symbol_dict:
            if len(symbol_dict[symbol]) == 1:
                symbol_dict[symbol] = symbol_dict[symbol].pop()


    df = pd.DataFrame.from_dict(table).fillna("∅").T
    return df.reindex(sorted(df.columns), axis=1)

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py
def make_nfa_table(target_fa) -> pd.DataFrame:
        """
        Generates a transition table of the given VisualNFA.

        Returns:
            DataFrame: A transition table of the VisualNFA.
        """

        final_states = "".join(target_fa.final_states)

        transitions = _nfa_add_lambda(all_transitions=target_fa.transitions)

        table: dict = {}
        for state, transition in sorted(transitions.items()):
            if state == target_fa.initial_state and state in final_states:
                state = "→*" + state
            elif state == target_fa.initial_state:
                state = "→" + state
            elif state in final_states:
                state = "*" + state
            row: dict = {}
            for input_symbol, next_states in transition.items():
                # Prepare nice symbol
                if input_symbol == "":
                    input_symbol = "λ"
                cell: list = []
                for next_state in sorted(next_states):
                    if next_state in final_states:
                        cell.append("*" + next_state)
                    else:
                        cell.append(next_state)
                if len(cell) == 1:
                    cell = cell.pop()
                else:
                    cell = "{" + ",".join(cell) + "}"
                row[input_symbol] = cell
            table[state] = row

        table = pd.DataFrame.from_dict(table).fillna("∅").T
        table = table.reindex(sorted(table.columns), axis=1)
        return table
    
def make_dtm_table(target_fa) -> pd.DataFrame:
    initial_state = target_fa.dtm.initial_state
    final_states = target_fa.dtm.final_states

    table = {}

    for from_state, (to_state, write_symbol, direction), read_symbol in target_fa.iter_transitions():
        # Prepare nice string for from_state
        if isinstance(from_state, frozenset):
            from_state_str = str(set(from_state))
        else:
            from_state_str = str(from_state)

        if from_state in final_states:
            from_state_str = "*" + from_state_str
        if from_state == initial_state:
            from_state_str = "→" + from_state_str

        # Prepare nice string for to_state
        if isinstance(to_state, frozenset):
            to_state_str = str(set(to_state))
        else:
            to_state_str = str(to_state)

        if to_state in final_states:
            to_state_str = "*" + to_state_str

        # Prepare nice symbol
        if read_symbol == "":
            read_symbol = "λ"
        if write_symbol == "":
            write_symbol = "λ"

        from_state_dict = table.setdefault(from_state_str, dict())
        from_state_dict.setdefault(to_state_str, set()).add(read_symbol + "/" + write_symbol + "," + direction)

    # Reformat table for singleton sets
    for symbol_dict in table.values():
        for symbol in symbol_dict:
            if len(symbol_dict[symbol]) == 1:
                symbol_dict[symbol] = symbol_dict[symbol].pop()

    df = pd.DataFrame.from_dict(table).fillna("∅").T
    return df.reindex(sorted(df.columns), axis=1)

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py
def _nfa_add_lambda(all_transitions: dict) -> dict:
        """
        Replacing '' key name for empty string (lambda/epsilon) transitions.

        Args:
            all_transitions (dict): The NFA's transitions with '' for lambda transitions.
            input_symbols (str): The NFA's input symbols/alphabet.

        Returns:
            dict: Transitions with λ for lambda transitions
        """
        all_transitions = all_transitions.deepcopy()
        # Replacing '' key name for empty string (lambda/epsilon) transitions.
        for transitions in all_transitions.values():
            transitions = transitions.deepcopy()
            for state, transition in list(transitions.items()):
                if state == "":
                    transitions["λ"] = transition
                    del transitions[""]
        return all_transitions
 
def make_DFA(states, input_symbols, transitions, initial_state, final_states, allow_partial=False): 
    return DFA(
      states=states,
      input_symbols=input_symbols,
      transitions=transitions,
      initial_state=initial_state,
      final_states=final_states,
      allow_partial=allow_partial
    )
    
def make_NFA(states, input_symbols, transitions, initial_state, final_states):
    return NFA(
       states=states,
       input_symbols=input_symbols,
       transitions=transitions,
       initial_state=initial_state,
       final_states=final_states 
    )
    
def make_DTM(states, input_symbols, tape_symbols, transitions, initial_state, blank_symbol, final_states):
    dtm = DTM(
        states=states,
        input_symbols=input_symbols,
        tape_symbols=tape_symbols,
        transitions=transitions,
        initial_state=initial_state,
        blank_symbol=blank_symbol,
        final_states=final_states 
    )
    dtm = tm_helpers.VisualDTM(dtm)
    return dtm
    
def open(filename): 
    if str(filename).lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        try:
            if platform.system() == 'Darwin':       # macOS
                subprocess.check_call(('open', filename), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            elif platform.system() == 'Windows':    # Windows
                os.startfile(os.path.normpath(filename))
            else:                                   # linux variants
                subprocess.check_call(('xdg-open', filename), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) 
            return ("Opening " + str(filename) + "...")
        except Exception as ex:
            message = 'The file ' + os.path.normpath(filename) + ' does not exist.'
            return message
    else:
        return 'The file ' + os.path.normpath(filename) + ' is not an accepted file type to open.'
   
def save(*args):
  target_fa = args[0]
  path = args[1]
  if len(args) > 2:
    input_string = args[2]
    if len(args) > 3:
      horizontal = args[3]
      return target_fa.show_diagram(input_str=input_string, path=path, horizontal=horizontal)
    else:
      return target_fa.show_diagram(input_str=input_string, path=path)
  else:
      return target_fa.show_diagram(path=path)
  
def test(*args):
    target_fa = args[0]
    input_string = args[1]
    #(transition_steps, accepted) = target_fa._get_input_path(input_string)
    if isinstance(target_fa, DFA):
        taken_steps = \
            _make_dfa_transition_walkthrough(target_fa, input_string)
        return (taken_steps, 'ipython_display')
    elif isinstance(target_fa, NFA):
        taken_steps = \
            _make_nfa_transition_walkthrough(target_fa, input_string)
        return (taken_steps, 'ipython_display')
    elif isinstance(target_fa, tm_helpers.VisualDTM):
        taken_steps = \
            _make_dtm_transition_walkthrough(target_fa, input_string)
        return (taken_steps, 'ipython_display')
        
    #return_string = 'Steps taken:'
    #for i in transition_steps:
    #  return_string += "\n->" + " From " + str(i[0]) + " to " + str(i[1]) + " on " + str(i[2])
    #return_string += '\n'
    #if (accepted):
    #    return_string += '\nAccepted word!'
    #else:
    #    return_string += '\nRejected word...'
    #    
    #return return_string 

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/dfa.py
def _make_dfa_transition_walkthrough(target_fa, input_str: str, return_result=False) -> Union[bool, list, list]:
        """
        Checks if string of input symbols results in final state.

        Args:
            input_str (str): The input string to run on the DFA.
            return_result (bool, optional): Returns results to the show_diagram method. Defaults to False.

        Raises:
            TypeError: To let the user know a string has to be entered.

        Returns:
            Union[bool, list, list]: If the last state is the final state, transition pairs, and steps taken.
        """
        if not isinstance(input_str, str):
            raise TypeError(f"input_str should be a string. {input_str} is {type(input_str)}, not a string.")

        current_state = target_fa.initial_state
        transitions_taken = [current_state]
        symbol_sequence: list = []
        status: bool = True

        for symbol in input_str:
            symbol_sequence.append(symbol)
            if symbol in target_fa.transitions[current_state]:
                current_state = target_fa.transitions[current_state][symbol]
            transitions_taken.append(current_state)

        if transitions_taken[-1] not in target_fa.final_states:
            status = False
        else:
            status = True

        taken_transitions_pairs = [
            (a, b, c)
            for a, b, c in zip(
                transitions_taken, transitions_taken[1:], symbol_sequence
            )
        ]
        taken_steps = _get_dfa_transition_steps(
            target_fa=target_fa,
            initial_state=target_fa.initial_state,
            final_states=target_fa.final_states,
            input_str=input_str,
            transitions_taken=transitions_taken,
            status=status,
        )
        if return_result:
            return status, taken_transitions_pairs, taken_steps
        else:
            return taken_steps  # .to_string(index=False)
        
#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/dfa.py
def _get_dfa_transition_steps(target_fa, initial_state, final_states, input_str: str, transitions_taken: list, status: bool) -> pd.DataFrame:
    initial_state = target_fa.initial_state
    final_states = target_fa.final_states
    
    current_states = transitions_taken.copy()
    for i, state in enumerate(current_states):
        if (
            state == initial_state and state in
            final_states
        ):
            current_states[i] = "→*" + state
        elif state == initial_state:
            current_states[i] = "→" + state
        elif state in final_states:
            current_states[i] = "*" + state

    new_states = current_states.copy()
    del current_states[-1]
    del new_states[0]
    inputs = [str(x) for x in input_str]

    transition_steps: dict = {
        "Current state:": current_states,
        "Input symbol:": inputs,
        "New state:": new_states,
    }

    transition_steps = pd.DataFrame.from_dict(
        transition_steps
    )
    transition_steps.index += 1
    transition_steps = pd.DataFrame.from_dict(
        transition_steps
    ).rename_axis("Step:", axis=1)
    if status:
        transition_steps.columns = pd.MultiIndex.from_product(
            [[f'[DFA on \"{input_str}\" is Accepted!]'], transition_steps.columns]
        )
        return transition_steps
    else:
        transition_steps.columns = pd.MultiIndex.from_product(
            [[f'[DFA on \"{input_str}\" is Rejected...]'], transition_steps.columns]
        )
        return transition_steps

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py    
def _make_nfa_transition_walkthrough(target_fa, input_str: str, return_result=False) -> Union[bool, list, pd.DataFrame]:  # pragma: no cover. Too many possibilities.
        """
        Checks if string of input symbols results in final state.

        Args:
            input_str (str): The input string to run on the NFA.
            return_result (bool, optional): Returns results to the show_diagram method. Defaults to False.

        Raises:
            TypeError: To let the user know a string has to be entered.

        Returns:
            Union[bool, list, list]: If the last state is the final state, transition pairs, and steps taken.
        """

        if not isinstance(input_str, str):
            raise TypeError(
                f"input_str should be a string. "
                f"{input_str} is {type(input_str)}, not a string."
            )
            
        status = target_fa.accepts_input(input_str)
            
        status, taken_transitions_pairs = _nfa_pathfinder(
            target_fa, input_str=input_str, status=status
        )
        if not isinstance(status, bool):
            if return_result:
                return status, [], pd.DataFrame, input_str
            else:
                return status
        current_states = target_fa.initial_state
        transitions_taken = [current_states]

        for transition in range(len(taken_transitions_pairs)):
            transitions_taken.append(taken_transitions_pairs[transition][1])

        taken_steps, inputs = _get_nfa_transition_steps(
            initial_state=target_fa.initial_state,
            final_states=target_fa.final_states,
            input_str=input_str,
            transitions_taken=transitions_taken,
            status=status,
        )
        if return_result:
            return status, taken_transitions_pairs, taken_steps, inputs
        else:
            return taken_steps

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py    
def _get_nfa_transition_steps(initial_state, final_states, input_str: str, transitions_taken: list, status: bool) -> pd.DataFrame:  # pragma: no cover. Too many possibilities.
        """
        Generates a table of taken transitions based on the input string and it's result.

        Args:
            initial_state (str): The NFA's initial state.
            final_states (set): The NFA's final states.
            input_str (str): The input string to run on the NFA.
            transitions_taken (list): Transitions taken from the input string.
            status (bool): The result of the input string.

        Returns:
            DataFrame: Table of taken transitions based on the input string and it's result.
        """
        current_states = transitions_taken.copy()
        for i, state in enumerate(current_states):

            if state == "" or state == {}:
                current_states[i] = "∅"

            elif state == initial_state and state in final_states:
                current_states[i] = "→*" + state
            elif state == initial_state:
                current_states[i] = "→" + state
            elif state in final_states:
                current_states[i] = "*" + state

        new_states = current_states.copy()
        del current_states[-1]
        del new_states[0]
        inputs = [str(x) for x in input_str]
        inputs = inputs[: len(current_states)]

        transition_steps: dict = {
            "Current state:": current_states,
            "Input symbol:": inputs,
            "New state:": new_states,
        }

        transition_steps = pd.DataFrame.from_dict(transition_steps)
        transition_steps.index += 1
        transition_steps = pd.DataFrame.from_dict(
            transition_steps
        ).rename_axis("Step:", axis=1)
        if status:
            transition_steps.columns = pd.MultiIndex.from_product(
                [[f'[NFA on \"{input_str}\" is Accepted!]'], transition_steps.columns]
            )
            return transition_steps, inputs
        else:
            transition_steps.columns = pd.MultiIndex.from_product(
                [[f'[NFA on \"{input_str}\" is Rejected...]'], transition_steps.columns]
            )
            return transition_steps, inputs
        
#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py        
def _nfa_pathfinder(target_fa, input_str: str, status: bool = False, counter: int = 0, main_counter: int = 0) -> Union[bool, list]:  # pragma: no cover. Too many possibilities.
        """
        Searches for a appropriate path to return to input_check.

        Args:
            input_str (str): Input symbols
            status (bool, optional): If a path is found. Defaults to False.
            counter (int, optional): To keep track of recursion limit in __pathsearcher. Defaults to 0.
            main_counter (int, optional): To keep track of recursion limit in _pathfinder. Defaults to 0.

        Returns:
            Union[bool, list]: If a path is found, and a list of transition tuples.
        """

        counter += 1
        nfa = target_fa.copy()
        recursion_limit = 50
        result = _nfa_pathsearcher(nfa, input_str, status)

        if result:
            return status, result
        else:
            main_counter += 1
            if main_counter <= recursion_limit:
                return _nfa_pathfinder(
                    input_str, status, counter, main_counter=main_counter
                )
            else:
                status = (
                    "[NO VALID PATH FOUND]\n"
                    "Try to eliminate lambda transitions and try again.\n"
                    "Example: nfa_lambda_removed = nfa.eliminate_lambda()"
                )
                return status, []

#https://github.com/lewiuberg/visual-automata/blob/master/visual_automata/fa/nfa.py
def _nfa_pathsearcher(nfa, input_str: str, status: bool = False, counter: int = 0) -> list:  # pragma: no cover. Too many possibilities.
        """
        Searches for a appropriate path to return to _pathfinder.

        Args:
            nfa (VisualNFA): A VisualNFA object.
            input_str (str): Input symbols.
            status (bool, optional): If a path is found. Defaults to False.
            counter (int, optional): To keep track of recursion limit. Defaults to 0.

        Returns:
            list: a list of transition tuples.
        """

        recursion_limit = 20000
        counter += 1
        current_state = {(nfa.initial_state)}
        path = []
        for symbol in input_str:
            next_curr = nfa._get_next_current_states(current_state, symbol)
            if next_curr == set():
                if not status:
                    state = {}
                    path.append(("".join(current_state), state, symbol))
                    return path
                else:
                    break
            else:
                state = random.choice(list(next_curr))
            path.append(("".join(current_state), state, symbol))
            current_state = {(state)}

        # Accepted path opptained.
        if (
            status
            and len(input_str) == (len(path))
            and path[-1][1] in nfa.final_states
        ):
            return path
        # Rejected path opptained.
        elif not status and len(input_str) == (len(path)):
            return path
        # No path obtained. Try again.
        else:
            if counter <= recursion_limit:
                return _nfa_pathsearcher(nfa, input_str, status, counter)
            else:
                return False
            
def _make_dtm_transition_walkthrough(target_fa, input_str: str, return_result=False) -> Union[bool, list, list]:
        """
        Checks if string of input symbols results in final state.

        Args:
            input_str (str): The input string to run on the DFA.
            return_result (bool, optional): Returns results to the show_diagram method. Defaults to False.

        Raises:
            TypeError: To let the user know a string has to be entered.

        Returns:
            Union[bool, list, list]: If the last state is the final state, transition pairs, and steps taken.
        """
        if not isinstance(input_str, str):
            raise TypeError(f"input_str should be a string. {input_str} is {type(input_str)}, not a string.")

        current_state = target_fa.dtm.initial_state
        transitions_taken = []
        symbol_sequence: list = []
        status: bool = True

        transitions_path, status = target_fa.get_input_path(input_str=input_str)
        
        for transition_index, configuration_pair in enumerate(
                transitions_path, start=1
            ):
            
            prev_configuration = configuration_pair[0]
            configuration = configuration_pair[1]
            
            from_state = prev_configuration.state
            to_state = configuration.state
            
            if configuration.tape.current_position > prev_configuration.tape.current_position:
                direction = 'R'
            elif configuration.tape.current_position < prev_configuration.tape.current_position:
                direction = 'L'
            else:
                direction = 'N'
                
            if direction == 'R':
                write_symbol = configuration.tape.tape[configuration.tape.current_position - 1]
                read_symbol = prev_configuration.tape.tape[configuration.tape.current_position - 1]
            elif direction == 'L':
                write_symbol = configuration.tape.tape[configuration.tape.current_position + 1]
                read_symbol = prev_configuration.tape.tape[configuration.tape.current_position + 1]
            else: 
                write_symbol = configuration.tape.tape[configuration.tape.current_position]
                read_symbol = prev_configuration.tape.tape[configuration.tape.current_position]
            
            transition = target_fa.get_edge_name(read_symbol) + "/" + target_fa.get_edge_name(write_symbol) + "," + direction
            transitions_taken.append((from_state, to_state, transition))

        taken_steps = _get_dtm_transition_steps(
            target_fa=target_fa.dtm,
            initial_state=target_fa.dtm.initial_state,
            final_states=target_fa.dtm.final_states,
            input_str=input_str,
            transitions_taken=transitions_taken,
            status=status,
        )
        if return_result:
            return status, taken_steps
        else:
            return taken_steps  # .to_string(index=False)
        
def _get_dtm_transition_steps(target_fa, initial_state, final_states, input_str: str, transitions_taken: list, status: bool) -> pd.DataFrame:
    initial_state = target_fa.initial_state
    final_states = target_fa.final_states
    
    current_states = transitions_taken.copy()
    for i, state in enumerate(current_states):
        if (
            state[0] == initial_state and state[0] in
            final_states
        ):
            current_states[i] = "→*" + state[0]
        elif state[0] == initial_state:
            current_states[i] = "→" + state[0]
        elif state[0] in final_states:
            current_states[i] = "*" + state[0]
        else:
            current_states[i] = state[0]
    current_states.insert(0, "")

    new_states = transitions_taken.copy()
    for i, state in enumerate(new_states):
        if (
            state[1] == initial_state and state[1] in
            final_states
        ):
            new_states[i] = "→*" + state[1]
        elif state[1] == initial_state:
            new_states[i] = "→" + state[1]
        elif state[1] in final_states:
            new_states[i] = "*" + state[1]
        else:
            new_states[i] = state[1]
    new_states.insert(0, current_states[1])
            
    #del current_states[-1]
    #del new_states[0]
    actions = [str(x[2]) for x in transitions_taken]
    actions.insert(0,"$/$/R")

    transition_steps: dict = {
        "Current state:": current_states,
        "Read/Write/Move:": actions,
        "New state:": new_states,
    }

    transition_steps = pd.DataFrame.from_dict(
        transition_steps
    )
    transition_steps.index += 1
    transition_steps = pd.DataFrame.from_dict(
        transition_steps
    ).rename_axis("Step:", axis=1)
    if status:
        transition_steps.columns = pd.MultiIndex.from_product(
            [[f'[DTM on \"{input_str}\" is Accepted!]'], transition_steps.columns]
        )
        return transition_steps
    else:
        transition_steps.columns = pd.MultiIndex.from_product(
            [[f'[DTM on \"{input_str}\" is Rejected...]'], transition_steps.columns]
        )
        return transition_steps
