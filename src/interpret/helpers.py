from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.tm.dtm import DTM
from automata.tm.ntm import NTM
from automata.tm.mntm import MNTM

from typing import Union
import pandas as pd
import subprocess, os, platform

def system_type():
    return platform.system()
  
def definition(*args):
    target_fa = args[0]
    table = make_fa_table(target_fa)
    return table
  
def make_fa_table(target_fa) -> pd.DataFrame:
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
            [[f'[\"{input_str}\" is Accepted!]'], transition_steps.columns]
        )
        return transition_steps
    else:
        transition_steps.columns = pd.MultiIndex.from_product(
            [[f'[\"{input_str}\" is Rejected...]'], transition_steps.columns]
        )
        return transition_steps