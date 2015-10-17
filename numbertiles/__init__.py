# __init__.py - Python package indicator file
#
# Copyright 2015 Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>.
#
# This file is part of Tiles.
#
# Tiles is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Tiles is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tiles. If not, see <http://www.gnu.org/licenses/>.
"""Code for the tiles game.

Names available from this package are part of the public API for
Tiles. For more advanced usage, you can access the model, view, or
controller directly from the corresponding modules in this directory.

"""
from .model import Game
from .model import random_game
