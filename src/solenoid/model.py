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
Model of a Solenoid
Based on:
A Detailed Explanation of Solenoid Force.
Paul H. Schimpf.
Int. J. on Recent Trends in Engineering and Technology, Vol. 8, No. 2, Jan 2013
"""

from typing import NewType
import math

# Type aliases for typecheck
Area                = NewType('Area',                float)
DecayFactor         = NewType('DecayFactor',         float)
Force               = NewType('Force',               float)
Length              = NewType('Length',              float)
Permeability        = NewType('Permeability',        float)
Radius              = NewType('Radius',              float)
RelPermeability     = NewType('RelPermeability',     float)
ResistancePerLength = NewType('ResistancePerLength', float)
Voltage             = NewType('Voltage',             float)
WindingFactor       = NewType('WindingFactor',       float)
WireGauge           = NewType('WireGauge',           int)
Turns               = NewType('Turns',               int)

# constants
MU : Permeability = Permeability(4 * math.pi * 1e-7)

def wire_area(awg: WireGauge) -> Area:
    """Determine wire cross section area in m^2"""
    # WIP
    return Area(awg)

def packing_density() -> float:
    """Return wire packing density"""
    return 0.7

def winding_factor(awg: WireGauge, r_o: Radius, l: Length, N: Turns) -> float:
    """Compute winding factor"""
    numerator   = r_o ** 2
    beta        = wire_area(awg) / (2 * packing_density() * l)
    denominator = (beta * N + r_o) ** 2
    return numerator / denominator

def decay_factor(mu_r: RelPermeability) -> float:
    """Compute decay factor"""
    return math.log(mu_r)

def res_per_length(awg: WireGauge) -> ResistancePerLength:
    """Compute wire resistance per length in ohms/m"""
    # WIP
    return ResistancePerLength(awg)

def force(
    v: Voltage,
    mu_r: RelPermeability,
    awg: WireGauge,
    r_o: Radius,
    l: Length,
    N: Turns) -> Force:
    """Compute force inside a solenoid in Newtons"""
    wf          = winding_factor(awg, r_o, l, N)
    alpha       = decay_factor(mu_r)
    gamma       = res_per_length(awg)
    numerator   = -(v ** 2) * mu_r * MU * wf * alpha
    denominator = (8 * math.pi * (gamma ** 2) * (l ** 2))
    return Force(numerator / denominator)
