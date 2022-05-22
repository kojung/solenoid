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
from typing import List, Tuple, Any

import matplotlib.pyplot as plt

import numpy as np

from solenoid.units import (
    Current,
    Force,
    Power,
    Efficiency,
)
from solenoid.model import (
     force,
     current,
     power,
     efficiency,
)
from solenoid.wires import (
    awg_current_limit
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
    parser.add_argument("-a", "--awg", nargs="+", type=int, required=True,
        help="Wire AWG gauge (scalar or range)")
    parser.add_argument("-N", "--turns", nargs="+", type=float, required=True,
        help="Number of turns (scalar or range)")
    parser.add_argument("-p", "--relative_permeability", nargs="+", type=float, required=True,
        help="Relative permeability (scalar)")
    parser.add_argument("-d", "--packing_density", nargs="+", type=float, required=True,
        help="Packing density")
    parser.add_argument("--width", type=float, default=10,
        help="Figure width in inches")
    parser.add_argument("--height", type=float, default=10,
        help="Figure height in inches")
    parser.add_argument("--dpi", type=int, default=100,
        help="Figure resolution")
    return parser.parse_args()

# pylint: disable=too-many-locals
def compute_force(args, range_param) -> Tuple[Any, List[Force]]:
    """return force vs. range parameter"""
    range_name, _, (range_start, range_end) = range_param
    x = np.linspace(range_start, range_end, 30)
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

# pylint: disable=too-many-locals
def compute_current(args, range_param) -> Tuple[Any, List[Current]]:
    """return current vs. range parameter"""
    range_name, _, (range_start, range_end) = range_param
    x = np.linspace(range_start, range_end, 30)
    y = []
    for val in x:
        voltage               = val if range_name == "Voltage"               else args.voltage[0]
        length                = val if range_name == "Length"                else args.length[0]
        radius                = val if range_name == "Radius"                else args.radius[0]
        awg                   = val if range_name == "Awg"                   else args.awg[0]
        turns                 = val if range_name == "Turns"                 else args.turns[0]
        packing_density       = val if range_name == "Packing Density"       else args.packing_density[0]
        c = current(
            v=voltage,
            awg=awg,
            r_o=radius,
            l=length,
            N=turns,
            d=packing_density,
        )
        y.append(c)
    return (x, y)

# pylint: disable=too-many-locals
def compute_power(args, range_param) -> Tuple[Any, List[Power]]:
    """return power vs. range parameter"""
    range_name, _, (range_start, range_end) = range_param
    x = np.linspace(range_start, range_end, 30)
    y = []
    for val in x:
        voltage               = val if range_name == "Voltage"               else args.voltage[0]
        length                = val if range_name == "Length"                else args.length[0]
        radius                = val if range_name == "Radius"                else args.radius[0]
        awg                   = val if range_name == "Awg"                   else args.awg[0]
        turns                 = val if range_name == "Turns"                 else args.turns[0]
        packing_density       = val if range_name == "Packing Density"       else args.packing_density[0]
        p = power(
            v=voltage,
            awg=awg,
            r_o=radius,
            l=length,
            N=turns,
            d=packing_density,
        )
        y.append(p)
    return (x, y)

# pylint: disable=too-many-locals
def compute_efficiency(args, range_param) -> Tuple[Any, List[Efficiency]]:
    """return efficiency vs. range parameter"""
    range_name, _, (range_start, range_end) = range_param
    x = np.linspace(range_start, range_end, 30)
    y = []
    for val in x:
        voltage               = val if range_name == "Voltage"               else args.voltage[0]
        length                = val if range_name == "Length"                else args.length[0]
        radius                = val if range_name == "Radius"                else args.radius[0]
        awg                   = val if range_name == "Awg"                   else args.awg[0]
        turns                 = val if range_name == "Turns"                 else args.turns[0]
        packing_density       = val if range_name == "Packing Density"       else args.packing_density[0]
        relative_permeability = val if range_name == "Relative Permeability" else args.relative_permeability[0]
        e = efficiency(
            v=voltage,
            mu_r=relative_permeability,
            awg=awg,
            r_o=radius,
            l=length,
            N=turns,
            d=packing_density,
        )
        y.append(e)
    return (x, y)

# pylint: disable=too-many-statements
def main():
    """main program"""
    args = parse_args()

    # make sure exactly 1 parameter is specified as range, while the rest are scalars
    params = [
        ("Voltage",               "[V]", args.voltage),
        ("Length",                "[m]", args.length),
        ("Radius",                "[m]", args.radius),
        ("Awg",                   "[AWG]", args.awg),
        ("Turns",                 "[#]", args.turns),
        ("Relative Permeability", "",    args.relative_permeability),
        ("Packing Density",       "",    args.packing_density),
    ]
    range_param = (None, "", 0)
    textbox = []
    for name, unit, param in params:
        if len(param) > 1:
            # make sure exactly 1 parameter is a ranged parameter
            if range_param == (None, "", 0):
                range_param = (name, unit, param)
            else:
                # pylint: disable=unsubscriptable-object
                raise ValueError(f"Both parameters '{name}' and '{range_param[0]}' specified as range")
        else:
            # collect non-ranged parameters
            textbox.append(f"{name} = {param[0]} {unit}")

    assert range_param != (None, "", 0), "At least one parameter should be a range"

    range_name, _, (range_start, range_end) = range_param
    domain = np.linspace(range_start, range_end, 30)

    # current limit depends on wire gauge only
    if range_name == "Awg":
        # variable current limit
        current_limit = np.array(map(awg_current_limit, domain))
    else:
        # fixed current limit
        current_limit = np.array([awg_current_limit(args.awg[0])] * len(domain))

    # power limit depends on voltage and wire gauge
    if range_name == "Voltage":
        # fixed current limit, variable voltage
        power_limit = current_limit * domain
    else:
        # variable current limit, fixed voltage
        power_limit = current_limit * args.voltage[0]

    fig = plt.figure(figsize=(args.width, args.height), dpi=args.dpi)

    ax  = fig.add_subplot(511)  # legend
    ax1 = fig.add_subplot(512)
    ax2 = fig.add_subplot(513)
    ax3 = fig.add_subplot(514)
    ax4 = fig.add_subplot(515)

    # Turn off axis lines and ticks of the legend
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0, 0, "\n".join(textbox), transform=ax.transAxes, bbox=props)
    ax.set_title(f"Solenoid properties vs. {range_param[0]}")

    # force
    x, y = compute_force(args, range_param)
    ax1.plot(x,y)
    ax1.set_ylabel("Force [N]")

    # current
    x, y = compute_current(args, range_param)
    ax2.plot(x,y)
    ax2.plot(x, current_limit, '--', color='red')
    ax2.set_ylabel("Current [A]")

    # power
    x, y = compute_power(args, range_param)
    power_limit = current_limit * args.voltage[0]
    ax3.plot(x,y)
    ax3.plot(x, power_limit, '--', color='red')
    ax3.set_ylabel("Power [W]")

    # efficiency
    x, y = compute_efficiency(args, range_param)
    ax4.plot(x,y)
    ax4.set_ylabel("Efficiency [N/W]")
    ax4.set_xlabel(f"{range_param[0]} {range_param[1]}")

    # all done
    plt.show()

if __name__ == "__main__":
    main()
