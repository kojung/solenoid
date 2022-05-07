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
Based on [1]:
A Detailed Explanation of Solenoid Force.
Paul H. Schimpf.
Int. J. on Recent Trends in Engineering and Technology, Vol. 8, No. 2, Jan 2013
"""

import math
from unittest import TestCase

from solenoid.wires import (
    awg_area,
    awg_resistance_per_length,
    awg_resistance,
)
from solenoid.units import (
    Current,
    DecayFactor,
    Efficiency,
    Force,
    Length,
    Permeability,
    Power,
    Radius,
    RelativePermeability,
    Resistance,
    Turns,
    Voltage,
    WindingFactor,
    WireGauge,
    PackingDensity,
)

def average_radius(awg:WireGauge, r_o:Radius, l:Length, N:Turns, d:PackingDensity) -> Radius:
    """
    Average solenoid radius, taking wire gauge into account

    :param awg: Wire gauge
    :param r_o: Solenoid nominal radius in meters
    :param l:   Solenoid length in meters
    :param N:   Number of turns
    :param d:   Packing density
    :return:    Average solenoid radius

    r_a    = beta * N + r_o
    beta   = a / lambda * l
    a      = wire cross section
    lambda = packing density
    l      = solenoid length
    """
    beta = awg_area(awg) / (d * l)
    return Radius(beta * N + r_o)

def _winding_factor(
    awg:WireGauge, r_o:Radius, l:Length, N:Turns, d:PackingDensity) -> WindingFactor:
    """
    Compute winding factor

    :param awg: Wire gauge
    :param r_o: Solenoid nominal radius in meters
    :param l:   Solenoid length in meters
    :param N:   Number of turns
    :param d:   Packing density
    :return:    Winding factor

    wf = r_o^2 / r_a^2
    """
    numerator   = r_o ** 2
    denominator = average_radius(awg, r_o, l, N, d) ** 2
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
    N:Turns,
    d:PackingDensity) -> Force:
    """
    Compute force inside a solenoid in Newtons

    :param v:    Voltage
    :param mu_r: Relative permeability of armature
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :param d:    Packing density
    :return:     Solenoid force when armature is fully inside solenoid in Newtons
    """
    mu : Permeability = Permeability(4 * math.pi * 1e-7)  # permeability of space/air
    wf                = _winding_factor(awg, r_o, l, N, d)
    alpha             = _decay_factor(mu_r)
    gamma             = awg_resistance_per_length(awg)
    numerator         = -(v ** 2) * mu_r * mu * wf * alpha
    denominator       = (8 * math.pi * (gamma ** 2) * (l ** 2))
    return Force(numerator / denominator)

def resistance(
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns,
    d:PackingDensity) -> Resistance:
    """
    Compute solenoid resistnace

    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :param d:    Wire packing density
    :return:     Solenoid resistance in ohms
    """
    r_a          = average_radius(awg, r_o, l, N, d)
    total_length = Length(2 * r_a * math.pi * N)
    return awg_resistance(awg, total_length)

def current(
    v:Voltage,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns,
    d:PackingDensity) -> Current:
    """
    Compute solenoid current at DC in Amps

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :param d:    Wire packing density
    :return:     Solenoid current in Amps
    """
    res = resistance(awg, r_o, l, N, d)
    return Current(v/res)

def power(
    v:Voltage,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns,
    d:PackingDensity) -> Power:
    """
    Compute solenoid power

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :param d:    Wire packing density
    :return:     Solenoid power in Watts

    power = V^2 / R at DC
    """
    i = current(v, awg, r_o, l, N, d)
    return Power(v * i)

def efficiency(
    v:Voltage,
    mu_r:RelativePermeability,
    awg:WireGauge,
    r_o:Radius,
    l:Length,
    N:Turns,
    d:PackingDensity) -> Efficiency:
    """
    Compute solenoid efficiency.

    :param v:    Solenoid voltage
    :param awg:  Wire gauge
    :param r_o:  Solenoid nominal radius in meters
    :param l:    Solenoid length in meters
    :param N:    Number of turns
    :param d:    Wire packing density
    :return:     Solenoid efficiency in Newton/Watt

    Efficiency is defined as force/power in Newton/Watt
    """
    newton = force(v, mu_r, awg, r_o, l, N, d)
    watt   = power(v, awg, r_o, l, N, d)
    return Efficiency(newton/watt)

class TestModel(TestCase):
    """Unit tests"""
    def test_average_radius(self) -> None:
        """Test awg_radius"""
        # Figure 6a of [1]
        d   = PackingDensity(0.48) # reverse-engineered value
        l   = Length(27 / 1000)    # 27mm
        r_o = Radius(2.3 / 1000)   # 2.3mm
        awg = WireGauge(30)
        N   = Turns(572)
        r_a = average_radius(awg, r_o, l, N, d)
        self.assertAlmostEqual(r_a, 4.5 / 1000, places=4)

    def test_resistance(self):
        """Test awg_radius"""
        # Figure 6a of [1]
        d   = PackingDensity(0.48) # reverse-engineered value
        l   = Length(27 / 1000)   # 27mm
        r_o = Radius(2.3 / 1000)  # 2.3mm
        awg = WireGauge(30)
        N   = Turns(572)
        self.assertAlmostEqual(resistance(awg, r_o, l, N, d), 5.3, delta=0.1)
