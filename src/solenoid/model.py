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

import math

from solenoid.wires import (
    awg_area,
    awg_resistance_per_length,
    awg_resistance,
)
from solenoid.units import (
    Current,
    DecayFactor,
    Force,
    Length,
    Permeability,
    Power,
    Radius,
    RelativePermeability,
    Turns,
    Voltage,
    WindingFactor,
    WireGauge,
    Efficiency,
)

def _packing_density() -> float:
    """
    Wire packing density

    For lattice, packing density <= pi / sqrt(12) = 0.907
    For lattice, packing density <= pi / 4 = 0.785

    Assume packing density of 0.7
    """
    return 0.7

def _average_radius(awg:WireGauge, r_o:Radius, l:Length, N:Turns) -> Radius:
    """
    Average solenoid radius, taking wire gauge into account

    :param awg: Wire gauge
    :param r_o: Solenoid nominal radius in meters
    :param l:   Solenoid length in meters
    :param N:   Number of turns
    :return:    Average solenoid radius

    r_a    = beta * N + r_0
    beta   = a / (2 * lambda * l)
    a      = wire cross section
    lambda = packing density
    l      = solenoid length
    """
    beta = awg_area(awg) / (2 * _packing_density() * l)
    return Radius(beta * N + r_o)

def _winding_factor(awg:WireGauge, r_o:Radius, l:Length, N:Turns) -> WindingFactor:
    """
    Compute winding factor

    :param awg: Wire gauge
    :param r_o: Solenoid nominal radius in meters
    :param l:   Solenoid length in meters
    :param N:   Number of turns
    :return:    Winding factor

    wf = r_o^2 / r_a^2
    """
    numerator   = r_o ** 2
    denominator = _average_radius(awg, r_o, l, N) ** 2
    return WindingFactor(numerator / denominator)

def _decay_factor(mu_r:RelativePermeability) -> DecayFactor:
    """
    Compute decay factor

    :param mu_r: Relative permeability of armature

    Model solenoid force along the axis as an exponential decaying
    function. The decay factor expresses how fast the solenoid force
    becomes 0 as the armature exits the solenoid.
    """
    return DecayFactor(math.log(mu_r))

def force(
    v:Voltage,
    mu_r:RelativePermeability,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns) -> Force:
    """
    Compute force inside a solenoid in Newtons

    :param v:    Voltage
    :param mu_r: Relative permeability of armature
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :return:     Solenoid force when armature is fully inside solenoid in Newtons
    """
    mu : Permeability = Permeability(4 * math.pi * 1e-7)  # permeability of space/air
    wf                = _winding_factor(awg, r_o, l, N)
    alpha             = _decay_factor(mu_r)
    gamma             = awg_resistance_per_length(awg)
    numerator         = -(v ** 2) * mu_r * mu * wf * alpha
    denominator       = (8 * math.pi * (gamma ** 2) * (l ** 2))
    return Force(numerator / denominator)

def current(
    v:Voltage,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns) -> Current:
    """
    Compute solenoid current at DC in Amps

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :return:     Solenoid current in Amps
    """
    r_a          = _average_radius(awg, r_o, l, N)
    total_length = Length(2 * r_a * math.pi * N)
    resistance   = awg_resistance(awg, total_length)
    return Current(v/resistance)

def power(
    v:Voltage,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns) -> Power:
    """
    Compute solenoid power

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :return:     Solenoid power in Watts

    power = V^2 / R at DC
    """
    i = current(v, awg, r_o, l, N)
    return Power(v * i)

def efficiency(
    v:Voltage,
    mu_r:RelativePermeability,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns) -> Efficiency:
    """
    Compute solenoid efficiency.

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :return:     Solenoid efficiency in Newton/Watt

    Efficiency is defined as force/power in Newton/Watt
    """
    newton = force(v, mu_r, awg, r_o, l, N)
    watt   = power(v, awg, r_o, l, N)
    return Efficiency(newton/watt)
