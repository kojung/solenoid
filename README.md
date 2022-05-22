# Solenoid Calculator

## Introduction

This calculator plots Force [N], Current [A], Power [W] , Efficiency [N/W] as a function of one of the following parameters:

- Voltage
- Length
- Inner Radius
- Wire Gauge
- Turns
- Relative permeability
- Packing density

## Usage

```
$ python solenoid/calculator.py

$ python solenoid/calculator.py -h
usage: calculator.py [-h]
    -v VOLTAGE [VOLTAGE ...] 
    -l LENGTH [LENGTH ...]
    -r RADIUS [RADIUS ...]
    -a AWG [AWG ...]
    -N TURNS [TURNS ...]
    -p RELATIVE_PERMEABILITY [RELATIVE_PERMEABILITY ...]
    -d PACKING_DENSITY [PACKING_DENSITY ...]
    [--width WIDTH]
    [--height HEIGHT]
    [--dpi DPI]

Solenoid Calculator

Plot Force, Power, Efficiency as a function of ONE of the following parameters:

- Voltage
- Length
- Inner Radius
- Wire Gauge
- Turns
- Relative permeability
- Packing density

Scalar parameters are specified as a single number.
Range parameters are specified as a start/end tuple.

optional arguments:
  -h, --help            show this help message and exit
  -v VOLTAGE [VOLTAGE ...], --voltage VOLTAGE [VOLTAGE ...]
                        Solenoid voltage (scalar or range)
  -l LENGTH [LENGTH ...], --length LENGTH [LENGTH ...]
                        Solenoid length (scalar or range)
  -r RADIUS [RADIUS ...], --radius RADIUS [RADIUS ...]
                        Solenoid inner radius (scalar or range)
  -a AWG [AWG ...], --awg AWG [AWG ...]
                        Wire gauge in AWG (scalar or range)
  -N TURNS [TURNS ...], --turns TURNS [TURNS ...]
                        Number of turns (scalar or range)
  -p RELATIVE_PERMEABILITY [RELATIVE_PERMEABILITY ...], --relative_permeability RELATIVE_PERMEABILITY [RELATIVE_PERMEABILITY ...]
                        Relative permeability (scalar)
  -d PACKING_DENSITY [PACKING_DENSITY ...], --packing_density PACKING_DENSITY [PACKING_DENSITY ...]
                        Packing density
  --width WIDTH         Figure width in inches
  --height HEIGHT       Figure height in inches
  --dpi DPI             Figure resolution
```

