#!/usr/bin/env python3

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
Solenoid calculator
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np

from solenoid.model import (
     force,
#     current,
#     resistance,
#     power,
#     efficiency,
)

def parse_args():
    """Parse command line args"""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description="""\
Solenoid Calculator

Plot Force, Power, Efficiency as a function of ONE of the following parameters:

- Voltage
- Length
- Radius
- AWG
- Turns
- Relative permeability
- Packing density

Scalar parameters are specified as a single number.
Range parameters are specified as a start/end tuple.
""")
    parser.add_argument("-v", "--voltage", nargs="+", type=float, required=True,
        help="Solenoid voltage (scalar or range)")
    parser.add_argument("-l", "--length", nargs="+", type=float, required=True,
        help="Solenoid length (scalar or range)")
    parser.add_argument("-r", "--radius", nargs="+", type=float, required=True,
        help="Solenoid inner radius (scalar or range)")
    parser.add_argument("-a", "--awg", nargs="+", type=float, required=True,
        help="Wire AWG gauge (scalar or range)")
    parser.add_argument("-N", "--turns", nargs="+", type=float, required=True,
        help="Number of turns (scalar or range)")
    parser.add_argument("-p", "--relative_permeability", nargs="+", type=float, required=True,
        help="Relative permeability (scalar)")
    parser.add_argument("-d", "--packing_density", nargs="+", type=float, required=True,
        help="Packing density")
    return parser.parse_args()

# pylint: disable=too-many-locals
def compute_force(args, range_param):
    """return force vs. range parameter"""
    range_name, _, (range_start, range_end) = range_param
    x = np.linspace(range_start, range_end, 30)
    print(f"Computing 'force' vs '{range_name}' from '{range_start}' to '{range_end}'")
    y = []
    for val in x:
        voltage               = val if range_name == "Voltage"               else args.voltage[0]
        length                = val if range_name == "Length"                else args.length[0]
        radius                = val if range_name == "Radius"                else args.radius[0]
        awg                   = val if range_name == "Awg"                   else args.awg[0]
        turns                 = val if range_name == "Turns"                 else args.turns[0]
        relative_permeability = val if range_name == "Relative Permeability" else args.relative_permeability[0]
        packing_density       = val if range_name == "Packing Density"       else args.packing_density[0]
        f = force(
            v=voltage,
            mu_r=relative_permeability,
            awg=awg,
            r_o=radius,
            l=length,
            N=turns,
            d=packing_density,
        )
        y.append(f)
    return (x, y)

def main():
    """main program"""
    args = parse_args()

    # make sure exactly 1 parameter is specified as range, while the rest are scalars
    params = [
        ("Voltage",               "[V]", args.voltage),
        ("Length",                "[m]", args.length),
        ("Radius",                "[m]", args.radius),
        ("Awg",                   "[#]", args.awg),
        ("Turns",                 "[#]", args.turns),
        ("Relative Permeability", "",    args.relative_permeability),
        ("Packing Density",       "",    args.packing_density),
    ]
    range_param = (None, "", 0)
    for name, unit, param in params:
        if len(param) > 1:
            if range_param == (None, "", 0):
                range_param = (name, unit, param)
            else:
                # pylint: disable=unsubscriptable-object
                raise ValueError(f"Both parameters '{name}' and '{range_param[0]}' specified as range")
    assert range_param != (None, "", 0), "At least one parameter should be a range"

    x, y = compute_force(args, range_param)

    _, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_ylabel("Force [N]")
    ax.set_xlabel(f"{range_param[0]} {range_param[1]}")
    plt.show()

    print("end")

if __name__ == "__main__":
    main()
