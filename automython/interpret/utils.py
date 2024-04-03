from typing import (
    Iterable,
    Literal,
    Tuple,
    TypeVar,
    Union,
)
from collections import defaultdict
from itertools import tee, zip_longest
import os
import pathlib
import uuid
import random
# Optional imports for use with visual functionality
try:
    import pygraphviz as pgv
except ImportError:
    _visual_imports = False
else:
    _visual_imports = True

LayoutMethod = Literal["neato", "dot", "twopi", "circo", "fdp", "nop"]
DTMSymbolT = str
T = TypeVar("T")


def create_unique_random_id() -> str:
    # To be able to set the random seed, took code from:
    # https://nathanielknight.ca/articles/consistent_random_uuids_in_python.html
    return str(
        uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)
    )
    
def pairwise(iterable: Iterable[T], final_none: bool = False) -> Iterable[Tuple[T, T]]:
    """Based on https://docs.python.org/3/library/itertools.html#itertools.pairwise"""
    a, b = tee(iterable)
    next(b, None)

    if final_none:
        return zip_longest(a, b)

    return zip(a, b)
  
def create_graph(
    horizontal: bool = True,
    reverse_orientation: bool = False,
    fig_size: Union[Tuple[float, float], Tuple[float], None] = None,
    state_separation: float = 0.5,
) -> pgv.AGraph:
    """Creates and returns a graph object
    Args:
        - horizontal (bool, optional): Direction of node layout. Defaults
            to True.
        - reverse_orientation (bool, optional): Reverse direction of node
            layout. Defaults to False.
        - fig_size (tuple, optional): Figure size. Defaults to None.
        - state_separation (float, optional): Node distance. Defaults to 0.5.
    Returns:
        AGraph with the given configuration.
    """
    
    if not _visual_imports:
        raise ImportError(
            "Missing visualization packages; "
            "please install coloraide and pygraphviz."
        )
    
    # Defining the graph.
    graph = pgv.AGraph(strict=False, directed=True)

    if fig_size is not None:
        graph.graph_attr.update(size=", ".join(map(str, fig_size)))

    graph.graph_attr.update(ranksep=str(state_separation))

    if horizontal:
        rankdir = "RL" if reverse_orientation else "LR"
    else:
        rankdir = "BT" if reverse_orientation else "TB"

    graph.graph_attr.update(rankdir=rankdir)

    return graph

def save_graph(
    graph: pgv.AGraph,
    path: Union[str, os.PathLike],
) -> None:
    """Write `graph` to file given by `path`. PNG, SVG, etc.
    Returns the same graph."""

    save_path_final: pathlib.Path = pathlib.Path(path)

    format = save_path_final.suffix.split(".")[1] if save_path_final.suffix else None

    graph.draw(
        path=save_path_final,
        format=format,
    )
