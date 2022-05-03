# Solenoid
# Copyright (C) 2022 Jung Ko <kojung@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Type aliases for different units. Used for typechecking.
"""

from typing import NewType

# Type aliases for typecheck
# All types are assumed to be in SI units
Area                 = NewType('Area',                 float)
DecayFactor          = NewType('DecayFactor',          float)
Force                = NewType('Force',                float)
Length               = NewType('Length',               float)
Permeability         = NewType('Permeability',         float)
Radius               = NewType('Radius',               float)
RelativePermeability = NewType('RelativePermeability', float)
Resistance           = NewType('Resistance',           float)
ResistancePerLength  = NewType('ResistancePerLength',  float)
Voltage              = NewType('Voltage',              float)
WindingFactor        = NewType('WindingFactor',        float)
WireGauge            = NewType('WireGauge',            int)
Turns                = NewType('Turns',                int)
Temperature          = NewType('Temperature',          float)
Power                = NewType('Power',                float)
Efficiency           = NewType('Efficiency',           float)
Current              = NewType('Current',              float)
PackingDensity       = NewType('PackingDensity',       float)
