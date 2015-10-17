# model.py - model classes and functions for the game
#
# Copyright 2015 Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>.
#
# This file is part of Number Tiles.
#
# Number Tiles is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Number Tiles is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Number Tiles. If not, see <http://www.gnu.org/licenses/>.
"""Model classes and functions for the number tiles game.

The basic usage of the model is as follows. A random initial game can be
created by using the :func:`random_game` function; the `size` argument
indicates the number of rows and columns in the game board::

    >>> size = 2
    >>> game = random_game(size)

A game can also be created manually from a given matrix of tiles::

    >>> tiles = [[1, 2], [3, 2]]
    >>> game = Game(tiles)
    >>> print(game)
    [1, 2]
    [3, 2]

An entry can be selected for collapsing using the
:meth:`Game.collapse_at` method. This will remove any tiles connected to
the specified entry via a path of tiles whose numbers equal that of the
selected tile::

    >>> tiles = [[1, 2], [3, 2]]
    >>> game = Game(tiles)
    >>> game.collapse_at(0, 1)
    >>> print(game)
    [1, 3]
    [None, 3]

As you can see in the above example, when collapsing, tiles are pulled
from left to right to fill any spaces that would become empty. This way,
all empty spaces only appear as a prefix in the list. To refill the
board with random new tiles, use the :meth:`Game.refill` method::

    >>> game.refill()

To test if there is any valid location for the player to collapse, use
the :meth:`Game.is_collapsible` method::

    >>> tiles = [[1, 2], [3, 2]]
    >>> game = Game(tiles)
    >>> game.is_collapsible()
    True
    >>> tiles = [[1, 2], [3, 4]]
    >>> game = Game(tiles)
    >>> game.is_collapsible()
    False

The game score, the sum of the tiles removed via the
:meth:`Game.collapse_at` method, is available from the
:attr:`Game.score` attribute::

    >>> tiles = [[1, 2], [3, 2]]
    >>> game = Game(tiles)
    >>> game.collapse_at(0, 1)
    >>> game.score
    2

"""
from itertools import chain
import random


def bounded_pareto_variate(alpha, upper_bound):
    """Repeatedly draws a random variable from the Pareto distribution
    until the variable meets the given upper bound.

    `alpha` is the parameter for the Pareto distribution.

    `upper_bound` is the upper bound which the random variable must
    meet.

    """
    result = random.paretovariate(alpha)
    while result >= upper_bound:
        result = random.paretovariate(alpha)
    return result


def float_nones(lst):
    """Returns a list containing the same elements as `lst`, but with
    any ``None`` elements floated to the left of the list.

    `lst` must be a list.

    For example::

        >>> float_nones([1, None, 2, None, 3])
        [None, None, 1, 2, 3]

    """
    right = [x for x in lst if x is not None]
    return [None] * (len(lst) - len(right)) + right


def random_game(size):
    """Returns an instance of :class:`Game` initialized with a random
    matrix of tiles.

    `size` is the number of rows and the number of columns in the game
    board.

    """
    rand = bounded_pareto_variate
    return Game([[int(rand(1, 3)) for i in range(size)] for i in range(size)])


class Game:
    """An instance of the game, maintaining a matrix of tiles.

    `tiles` must be a non-empty, square, list of lists representing a
    matrix stored in row-major order. The innermost list entries must be
    positive integers. This matrix is stored as the initial state of the
    game board.

    """

    def __init__(self, tiles):
        #: The matrix of tiles, stored as a (square) list of lists.
        self.tiles = tiles

        #: The current score of this game.
        #:
        #: The score is initially zero, and is incremented by the value
        #: of a tile for each tile removed via a call to
        #: :meth:`collapse_at`.
        self.score = 0

    def __str__(self):
        """Returns a string representation of the matrix of tiles.

        For example::

            >>> game = Game([[1, 2], [3, 4]])
            >>> print(game)
            [1, 2]
            [3, 4]

        """
        return '\n'.join(str(row) for row in self.tiles)

    def __len__(self):
        """Returns the size of the game board.

        The "size" is the number of rows and number of columns.

        For example::

            >>> game = Game([[1, 2], [3, 4]])
            >>> len(game)
            2

        """
        return len(self.tiles)

    def _bfs(self, i, j):
        """Returns an iterable over the coordinate pairs of the tiles
        that are connected to the tile at entry (`i`, `j`) by a path of
        tiles whose value matches that of the tile at (`i`, `j`).

        For example::

            >>> game = Game([[1, 1], [1, 2]])
            >>> list(game._bfs(0, 0))
            [(0, 0), (0, 1), (1, 0)]

        """
        seen = set()
        nextlevel = {(i, j)}
        while nextlevel:
            thislevel = nextlevel
            nextlevel = set()
            for k, l in thislevel:
                if (k, l) in seen:
                    continue
                yield (k, l)
                seen.add((k, l))
                # Explore each neighbor that has the same number as the
                # current tile (k, l).
                nextlevel.update((x, y) for x, y in self.neighbors(k, l)
                                 if self.tiles[k][l] == self.tiles[x][y])

    def neighbors(self, i, j):
        """Returns an iterable over coordinate pairs of the neighbors of
        entry (`i`, `j`).

        Only north, south, east, and west neighbors are considered.

        `i` and `j` must be integers at least zero and strictly less
        than the size of the game.

        For example::

            >>> game = Game([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            >>> list(game.neighbors(1, 1))
            [(0, 1), (2, 1), (1, 0), (1, 2)]

        If the entry is at the edge of the board, this only yields those
        neighbors that actually exist::

            >>> game = Game([[1, 2], [3, 4]])
            >>> list(game.neighbors(0, 0))
            [(1, 0), (0, 1)]

        """
        adds = []
        if i > 0:
            adds.append((-1, 0))
        if i < len(self.tiles) - 1:
            adds.append((+1, 0))
        if j > 0:
            adds.append((0, -1))
        if j < len(self.tiles) - 1:
            adds.append((0, +1))
        return ((i + x, j + y) for x, y in adds)

    def is_collapsible_at(self, i, j):
        """Returns ``True`` if and only if any of the neighbors of the
        tile at entry (`i`, `j`) match it.

        `i` and `j` must be integers at least zero and strictly less
        than the size of the game.

        For example::

            >>> game = Game([[1, 2], [1, 3]])
            >>> game.is_collapsible_at(0, 0)
            True
            >>> game.is_collapsible_at(0, 1)
            False

        """
        return any(self.tiles[k][l] == self.tiles[i][j]
                   for k, l in self.neighbors(i, j))

    def is_collapsible(self):
        """Returns ``True`` if and only if any of the entries on the
        board are collapsible.

        For example::

            >>> game = Game([[1, 2], [1, 3]])
            >>> game.is_collapsible()
            True
            >>> game = Game([[1, 2], [3, 4]])
            >>> game.is_collapsible()
            False

        """
        n = len(self)
        collapsible = self.is_collapsible_at
        return any(collapsible(i, j) for i in range(n) for j in range(n))

    def drop(self):
        """Collapse any empty spaces in the game board.

        For example, if a row in the game board is::

            [1, None, 2, None, 3]

        then after calling this method, that row will be::

            [None, None, 1, 2, 3]

        In other words, the empty spaces (represented by ``None``
        entries) are floated to the left.

        This method does not affect the score of the game.

        For example::

            >>> game = Game([[1, None], [2, 3]])
            >>> game.drop()
            >>> print(game)
            [None, 1]
            [2, 3]

        """
        # Float the `None`s to the left of each row while maintaining
        # the order of the remaining tiles.
        self.tiles = [float_nones(row) for row in self.tiles]

    def collapse_at(self, i, j):
        """Removes all contiguous tiles that match the tile at entry
        (`i`, `j`) and drops the tiles to fill any empty spaces in the
        board.

        `i` and `j` must be integers at least zero and strictly less
        than the size of the game.

        This method only collapses contiguous tiles and drops tiles
        into empty spaces. It does not refill the board with new
        tiles. In order to add new tiles to the newly empty spaces (if
        they exist), you must call the :meth:`refill` method.

        After removing any contiguous tiles, the value of the tile at
        entry (`i`, `j`) is incremented.

        This method additionally adds the values of any removed tiles to
        the :attr:`score` attribute.

        For example::

            >>> game = Game([[1, 1], [2, 1]])
            >>> game.collapse_at(0, 0)
            >>> print(game)
            [None, 2]
            [None, 2]

        """
        # Use list() here because the tiles will change during
        # iteration.
        for k, l in list(self._bfs(i, j)):
            # Do not remove the tile at the specified location.
            if (k, l) == (i, j):
                continue
            # Remove the connected tile and update the score.
            self.score += self.tiles[k][l]
            self.tiles[k][l] = None
        # Increment the value of the selected tile.
        self.tiles[i][j] += 1
        # Drop the tiles down through any blank spaces.
        self.drop()

    def random_tile(self):
        """Returns a random tile less than the largest number currently
        on the board.

        The value of the tile is drawn from the Pareto distribution,
        with an additional upper bound of the largest number currently
        on the board.

        """
        largest_number = max(0 if tile is None else tile
                             for tile in chain.from_iterable(self.tiles))
        return int(bounded_pareto_variate(1, largest_number))

    def refill(self):
        """Adds a random tile in each empty space on the game board.

        You should call :meth:`drop` before calling this method, but it
        is not required.

        """
        for row in self.tiles:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = self.random_tile()
