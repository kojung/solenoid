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
from typing import Optional

from icecream import ic

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

# disable debugging by default
ic.disable()

def check_values(
    v:Optional[Voltage]=None,
    mu_r:Optional[RelativePermeability]=None,
    awg:Optional[WireGauge]=None,
    r_o:Optional[Radius]=None,
    l:Optional[Length]=None,
    N:Optional[Turns]=None,
    d:Optional[PackingDensity]=None) -> None:
    """Check values ranges"""
    if awg:
        assert 40 >= awg >= 0, f"Wire gauge must be between 0 .. 40, got {awg}"
    if v:
        assert v > 0, f"Voltage must be > 0, got {v}"
    if d:
        assert d > 0, f"Packing density must be > 0, got {d}"
    if l:
        assert l > 0, f"Length must be > 0, got {l}"
    if mu_r:
        assert mu_r > 1, f"Relative permeability must be > 1, got {mu_r}"
    if N:
        assert N > 0, f"Number of turns must be > 0, got {N}"
    if r_o:
        assert r_o > 0, f"Internal radius must be > 0, got {r_o}"

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
    check_values(awg=awg, r_o=r_o, l=l, N=N, d=d)
    beta = awg_area(awg) / (2 * d * l)
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
    check_values(awg=awg, r_o=r_o, l=l, N=N, d=d)
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
    check_values(mu_r=mu_r)
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
    check_values(v=v, mu_r=mu_r, awg=awg, r_o=r_o, l=l, N=N, d=d)
    # ic.enable()
    mu : Permeability = ic(Permeability(4 * math.pi * 1e-7))  # permeability of space/air
    wf                = ic(_winding_factor(awg, r_o, l, N, d))
    alpha             = ic(_decay_factor(mu_r))
    gamma             = ic(awg_resistance_per_length(awg))
    numerator         = ic(-(v ** 2) * mu_r * mu * wf * alpha)
    denominator       = ic(-(8 * math.pi * (gamma ** 2) * (l ** 2)))
    newtons           = ic(numerator / denominator)
    ic.disable()
    return Force(newtons)

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
    check_values(awg=awg, r_o=r_o, l=l, N=N, d=d)
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
    check_values(v=v, awg=awg, r_o=r_o, l=l, N=N, d=d)
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
    check_values(v=v, awg=awg, r_o=r_o, l=l, N=N, d=d)
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
    check_values(v=v, awg=awg, r_o=r_o, l=l, N=N, d=d)
    newton = force(v, mu_r, awg, r_o, l, N, d)
    watt   = power(v, awg, r_o, l, N, d)
    return Efficiency(newton/watt)

class TestModel(TestCase):
    """Unit tests"""
    def test_average_radius(self) -> None:
        """Test awg_radius"""
        # Figure 6a of [1]
        d   = PackingDensity(0.25) # reverse-engineered value
        l   = Length(27 / 1000)    # 27mm
        r_o = Radius(2.3 / 1000)   # 2.3mm
        awg = WireGauge(30)
        N   = Turns(572)
        r_a = average_radius(awg, r_o, l, N, d)
        self.assertAlmostEqual(r_a, 4.4 / 1000, delta=0.0001)

    def test_resistance(self) -> None:
        """Test awg_radius"""
        # Figure 6a of [1]
        d   = PackingDensity(0.25) # reverse-engineered value
        l   = Length(27 / 1000)    # 27mm
        r_o = Radius(2.3 / 1000)   # 2.3mm
        awg = WireGauge(30)
        N   = Turns(572)
        self.assertAlmostEqual(resistance(awg, r_o, l, N, d), 5.3, delta=0.05)

    def test_force(self) -> None:
        """Test solenoid force"""
        # Figure 6a of [1]
        v    = Voltage(4.3)               # reverse-engineered value
        mu_r = RelativePermeability(375)  # from Paul's email
        d    = PackingDensity(0.25)       # reverse-engineered value
        l    = Length(27 / 1000)          # 27mm
        r_o  = Radius(2.3 / 1000)         # 2.3mm
        awg  = WireGauge(30)
        N    = Turns(572)
        self.assertAlmostEqual(force(v, mu_r, awg, r_o, l, N, d), 6.8, delta=0.1)

    def test_power(self) -> None:
        """Test solenoid power"""
        # Figure 6a of [1]
        v    = Voltage(4.3)               # reverse-engineered value
        d    = PackingDensity(0.25)       # reverse-engineered value
        l    = Length(27 / 1000)          # 27mm
        r_o  = Radius(2.3 / 1000)         # 2.3mm
        awg  = WireGauge(30)
        N    = Turns(572)
        self.assertAlmostEqual(power(v, awg, r_o, l, N, d), 4, delta=0.51)
