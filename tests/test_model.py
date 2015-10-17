# test_model.py - unit tests for the model module
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
"""Unit tests for the :mod:`numbertiles.model` module."""
from itertools import chain

from nose.tools import eq_
from nose.tools import ok_

from numbertiles import Game


class TestGame:
    """Unit tests for the :class:`numbertiles.Game` class."""

    def test_collapse_at_no_drop(self):
        """Tests for a collapse that does not cause any tiles to drop.

        """
        game = Game([[1, 2], [1, 3]])
        game.collapse_at(0, 0)
        eq_(game.tiles, [[2, 2], [None, 3]])

    def test_collapse_at_drop(self):
        """Tests for a collapse that causes tiles to drop."""
        game = Game([[2, 1], [3, 1]])
        game.collapse_at(0, 1)
        eq_(game.tiles, [[2, 2], [None, 3]])

    def test_collapse_at_score(self):
        """Tests that collapsing a tile causes the game score to
        increase.

        """
        game = Game([[2, 1], [2, 1]])
        game.collapse_at(0, 0)
        eq_(game.score, 2)
        game.collapse_at(0, 1)
        eq_(game.score, 3)

    def test_refill_not_none(self):
        """Tests that refilling the game board replaces tiles in all the
        empty spaces.

        """
        game = Game([[None, 2], [None, None]])
        game.refill()
        ok_(all(tile is not None for tile in chain.from_iterable(game.tiles)))

    def test_refill_bounded(self):
        """Tests that the refilled the values of the tiles are bounded
        above by the largest entry in the game board.

        """
        # Create a 10 x 10 game board with a single tile of value 10.
        size = 10
        tiles = [[None] * size] * size
        tiles[0][0] = 10
        game = Game(tiles)
        # Refill the game board with random tiles.
        game.refill()
        ok_(all(tile <= 10 for tile in chain.from_iterable(game.tiles)))
