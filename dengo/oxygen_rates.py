"""
Author: Devin Silvia <devin.silvia@gmail.com>
Affiliation: UC Boulder
Homepage: http://yt.enzotools.org/
License:
  Copyright (C) 2012 Matthew Turk.  All Rights Reserved.

  This file is part of the dengo package.

  This file is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from reaction_classes import Species, chianti_rate

for i in range(9):
    ion_state = i + 1
    s = Species("o_%s" % ion_state, 16, i)
    if ion_state != 9:
        # we need to do this to make sure the 'ion_state + 1' species
        # exists when chianti_rate is called
        splusone = Species("o_%s" % (ion_state+1), 16, i+1)
    chianti_rate(s)
