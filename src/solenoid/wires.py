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
AWG Copper Wire properties
"""
import math

from solenoid.units import (
    Area,
    Length,
    Radius,
    Resistance,
    ResistancePerLength,
    Temperature,
    WireGauge,
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
    temp:Temperature=Temperature(293)) -> ResistancePerLength:
    """
    :param awg:       Wire AWG
    :param temp:      Temperature [K]
    :return:          Resistance per unit length for copper at given temperature [Ohm/m]
    """
    # Reference: http://www.endmemo.com/physics/resistt.php
    reference_temp      = 293      # 20C
    resistivity         = 1.68e-8  # [ohm . m]
    alpha               = 0.0039   # thermal coefficient [1/K]
    delta_t             = temp - reference_temp
    resistivity_at_temp = resistivity * (1 + alpha * delta_t)
    area                = awg_area(awg)

    return ResistancePerLength(resistivity_at_temp / area)

def awg_resistance(
    awg:WireGauge,
    length:Length=Length(1),
    temp:Temperature=Temperature(293)) -> Resistance:
    """Wire resistance for given length"""
    return Resistance(awg_resistance_per_length(awg, temp) * length)
