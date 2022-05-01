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
AWG Wire properties
"""
import math

from solenoid.units import (
    WireGauge,
    Radius,
    Area,
    ResistancePerLength,
    Temperature,
)

def awg_radius(awg:WireGauge) -> Radius:
    """
    Convert AWG (American Wire Gauge) to radius

    :param awg: Wire AWG
    :return:    Wire diameter in m

    diameter [mm] = 0.127 * 92 ^ ((36-AWG)/39)

    Reference: http://www.reuk.co.uk/AWG-to-Square-mm-Wire-Size-Converter.htm
    """
    diameter_mm = 0.127 * (92 ** ((36 - awg) / 39))
    diameter_m  = diameter_mm / 1000
    return Radius(diameter_m / 2)

def awg_area(awg:WireGauge) -> Area:
    """
    :param awg: AWG number
    :return:    Wire cross sectional area in m^2
    """
    return Area(math.pi * (awg_radius(awg) ** 2))

def awg_resistance_per_length(
    awg:WireGauge,
    material:str="copper",
    temp:Temperature=Temperature(293)) -> ResistancePerLength:
    """
    :param awg:       Wire AWG
    :param material:  Wire material
    :param temp:      Temperature [K]
    :return:          Resistance per unit length for the selected material at given temperature [Ohm/m]

    Reference: http://www.endmemo.com/physics/resistt.php
    """
    coefficients = {
        # material: (resistivity [ohm.m] at 293K, thermal coefficient [1/K])
        "silver"     : (1.59e-8, 0.0038),
        "copper"     : (1.68e-8, 0.0039),
        "gold"       : (2.44e-8, 0.0034),
        "aluminium"  : (2.82e-8, 0.0039),
        "tungsten"   : (5.60e-8, 0.0045),
        "zinc"       : (5.90e-8, 0.0037),
        "nickel"     : (6.99e-8, 0.006),
        "iron"       : (1.0e-7,  0.005),
        "platinum"   : (1.06e-7, 0.00392),
        "tin"        : (1.09e-7, 0.0045),
        "lead"       : (2.2e-7,  0.0039),
        "manganin"   : (4.82e-7, 0.000002),
        "constantan" : (4.9e-7,  0.000008),
        "mercury"    : (9.8e-7,  0.0009),
        "nichrome"   : (1.10e-6, 0.0004),
        "carbon"     : (3.5e-5, -0.0005),
        "germanium"  : (4.6e-1, -0.048),
        "silicon"    : (6.40e2, -0.075),
    }

    reference_temp      = 293  # 20C
    resistivity, alpha  = coefficients[material]
    delta_t             = temp - reference_temp
    resistivity_at_temp = resistivity * (1 + alpha * delta_t)
    area                = awg_area(awg)

    return ResistancePerLength(resistivity_at_temp / area)
