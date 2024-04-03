import interpret.utils as utils
import coloraide
from automata.tm.dtm import DTM, DTMStateT, DTMPathResultT
from automata.tm.configuration import TMConfiguration
from automata.tm.tape import TMTape
import automata.base.exceptions as exceptions
from typing import (
    Any,
    List,
    Tuple,
    Union,
    Optional,
    Generator,
)
from collections import defaultdict
import os

class VisualDTM:
    def __init__(self, dtm):
        self.dtm = dtm
        
    def __repr__(self):
        return str(self.dtm)
    
    def __str__(self):
        return str(self.dtm)
    
    def get_state_name(self, state_data: Any) -> str:
        """
        Get a string representation of a state. This is used for displaying and
        uses `str` for any unsupported python data types.
        """
        if isinstance(state_data, str):
            if state_data == "":
                return "λ"

            return state_data

        elif isinstance(state_data, (frozenset, tuple)):
            inner = ", ".join(
                self.get_state_name(sub_data) for sub_data in state_data
            )
            if isinstance(state_data, frozenset):
                if state_data:
                    return "{" + inner + "}"
                else:
                    return "∅"

            elif isinstance(state_data, tuple):
                return "(" + inner + ")"

        return str(state_data)

    def get_edge_name(self, symbol: str) -> str:
            return "ε" if symbol == "" else str(symbol)

    def get_input_path(
            self, input_str: str
        ) -> Tuple[List[Tuple[DTMStateT, DTMStateT, utils.DTMSymbolT]], bool]:
            """
            Calculate the path taken by input.

            Parameters
            ------
            input_str : str
                The input string to run on the DFA.

            Returns
            ------
            Tuple[List[Tuple[DFAStateT, DFAStateT, DFASymbolT], bool]]
                A list of all transitions taken in each step and a boolean
                indicating whether the DFA accepted the input.

            """

            state_history = list(self.read_input_stepwise(input_str, ignore_rejection=True))
            state_history.pop()


            path = []
            for state_pair in zip(utils.pairwise(state_history)):
                path.append(state_pair[0])

            last_state = state_history[-1].state if state_history else self.dtm.initial_state
            accepted = last_state in self.dtm.final_states

            return path, accepted
        
    def _get_transition(
        self, state: DTMStateT, tape_symbol: str
    ) -> Optional[DTMPathResultT]:
        """Get the transiton tuple for the given state and tape symbol."""
        if state in self.dtm.transitions and tape_symbol in self.dtm.transitions[state]:
            return self.dtm.transitions[state][tape_symbol]
        else:
            return None

    def _has_accepted(self, configuration: TMConfiguration) -> bool:
        """Check whether the given config indicates accepted input."""
        return configuration.state in self.dtm.final_states
    
    def _has_rejected(self, configuration: TMConfiguration) -> bool:
        return not configuration.state

    def _get_next_configuration(self, old_config: TMConfiguration, ignore_rejection) -> TMConfiguration:
        """Advance to the next configuration."""
        next_transition = self._get_transition(
            old_config.state, old_config.tape.read_symbol()
        )

        if next_transition is None:
            if ignore_rejection == False:
                raise exceptions.RejectionException(
                    "The machine entered a non-final configuration for which no "
                    "transition is defined ({}, {})".format(
                        old_config.state, old_config.tape.read_symbol()
                    )
                )
            else:
                return TMConfiguration("", TMTape("", self.dtm.blank_symbol, -1))
        tape = old_config.tape
        (new_state, new_tape_symbol, direction) = next_transition
        tape = tape.write_symbol(new_tape_symbol)
        tape = tape.move(direction)
        return TMConfiguration(new_state, tape)

    def read_input_stepwise(
        self, input_str: str, ignore_rejection: bool = False
    ) -> Generator[TMConfiguration, None, None]:
        """
        Return a generator that yields the configuration of this DTM at each
        step while reading input.

        Parameters
        ----------
        input_str : str
            The input string to read.

        Yields
        ------
        Generator[TMConfiguration, None, None]
            A generator that yields the current configuration of
            the DTM after each step of reading input.
        """
        current_configuration = TMConfiguration(
            self.dtm.initial_state, TMTape(input_str, blank_symbol=self.dtm.blank_symbol)
        )
        yield current_configuration

        # The initial state cannot be a final state for a DTM, so the first
        # iteration is always guaranteed to run (as it should)
        while not self._has_rejected(current_configuration) or self._has_accepted(current_configuration):
            current_configuration = self._get_next_configuration(current_configuration, ignore_rejection)
            yield current_configuration

    def iter_transitions(
            self,
        ) -> Generator[Tuple[DTMStateT, DTMStateT, str], None, None]:
            """
            Iterate over all transitions in the DFA. Each transition is a tuple
            of the form (from_state, to_state, symbol).

            Returns
            ------
            Generator[Tuple[DFAStateT, DFAStateT, str], None, None]
                The desired generator over the DFA transitions.
            """
            return (
                (from_, to_, symbol)
                for from_, lookup in self.dtm.transitions.items()
                for symbol, to_ in lookup.items()
            )

    def show_diagram(
        self,
        input_str: Optional[str] = None,
        path: Union[str, os.PathLike, None] = None,
        *,
        layout_method: utils.LayoutMethod = "dot",
        horizontal: bool = True,
        reverse_orientation: bool = False,
        fig_size: Union[Tuple[float, float], Tuple[float], None] = None,
        font_size: float = 14.0,
        arrow_size: float = 0.85,
        state_separation: float = 0.5,
    ):

        # Defining the graph.
        graph = utils.create_graph(
            horizontal, reverse_orientation, fig_size, state_separation
        )

        font_size_str = str(font_size)
        arrow_size_str = str(arrow_size)

        # create unique id to avoid colliding with other states
        null_node = utils.create_unique_random_id()

        graph.add_node(
            null_node,
            label="",
            tooltip=".",
            shape="point",
            fontsize=font_size_str,
        )
        initial_node = self.get_state_name(self.dtm.initial_state)
        graph.add_edge(
            null_node,
            initial_node,
            label="$/$,R",
            tooltip="->" + initial_node,
            arrowsize=arrow_size_str,
        )

        nonfinal_states = map(self.get_state_name, self.dtm.states - self.dtm.final_states)
        final_states = map(self.get_state_name, self.dtm.final_states)
        graph.add_nodes_from(nonfinal_states, shape="circle", fontsize=font_size_str)
        graph.add_nodes_from(final_states, shape="doublecircle", fontsize=font_size_str)

        is_edge_drawn = defaultdict(lambda: False)
        if input_str is not None:
            #try:
            input_path, is_accepted = self.get_input_path(input_str=input_str)
            #except Exception as ex:
            #    template = "An exception of type {0} occurred:\n{1!r}"
            #    message = template.format(type(ex).__name__, ex.args[0])
            #    print(message)
            #    return None

            start_color = coloraide.Color("#ff0")
            end_color = (
                coloraide.Color("#0f0") if is_accepted else coloraide.Color("#f00")
            )
            interpolation = coloraide.Color.interpolate(
                [start_color, end_color], space="srgb"
            )

            # find all transitions in the finite state machine with traversal.
            for transition_index, configuration_pair in enumerate(
                input_path, start=1
            ):

                prev_configuration = configuration_pair[0]
                configuration = configuration_pair[1]
                color = interpolation(transition_index / len(input_path))

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

                label = self.get_edge_name(read_symbol) + "/" + self.get_edge_name(write_symbol) + "," + direction

                is_edge_drawn[from_state, to_state, read_symbol] = True
                graph.add_edge(
                    self.get_state_name(from_state),
                    self.get_state_name(to_state),
                    label=f"<{label} <b>[<i>#{transition_index}</i>]</b>>",
                    arrowsize=arrow_size_str,
                    fontsize=font_size_str,
                    color=color.to_string(hex=True),
                    penwidth="1.5",
                )
                prev_configuration = configuration
            # Create a subgraph for the tape
            subgraph = graph.add_subgraph(name='cluster_tape', label='Initial Tape', pos='0,0!', rank='same')

            # Create the tape visualization inside the subgraph
            tape_label = f'{{ ' + '$ | ' + '|'.join(list(input_str)) + f' | {self.dtm.blank_symbol}' + ' | ...' + '}}'
            subgraph.add_node('tape', shape='record', label=f'{tape_label}', fontsize=font_size_str)
        else: 
            # Create a subgraph for the tape
            subgraph = graph.add_subgraph(name='cluster_tape', label='Tape Symbols', pos='0,0!', rank='same')

            # Create the tape visualization inside the subgraph
            tape_label = f'{{ ' + '|'.join(self.dtm.tape_symbols) + ' }}'
            subgraph.add_node('tape', shape='record', label=f'{tape_label}', fontsize=font_size_str)

        edge_labels = defaultdict(list)
        for from_state, config, symbol in self.iter_transitions():
            if is_edge_drawn[from_state, config[0], symbol]:
                continue

            from_node = self.get_state_name(from_state)
            to_node = self.get_state_name(config[0])
            label = self.get_edge_name(symbol) + "/" + self.get_edge_name(config[1]) + "," + config[2]
            edge_labels[from_node, to_node].append(label)

        for (from_node, to_node), labels in edge_labels.items():
            graph.add_edge(
                from_node,
                to_node,
                label=",".join(sorted(labels)),
                arrowsize=arrow_size_str,
                fontsize=font_size_str,
            )

        # Set layout
        graph.layout(prog=layout_method)

        # Write diagram to file
        if path is not None:
            utils.save_graph(graph, path)

        return graph