#!/usr/bin/env python

from typing import ClassVar, Self
from dataclasses import dataclass
import argparse

from resistors.resistors import parse_workbook, find_dividers

@dataclass
class NumericRange:
    min: int | float | None
    max: int | float | None

    def __contains__(self, v: int | float):
        return (self.min is None or v >= self.min) and (self.max is None or v <= self.max)

    def parse(v: str):
        limits = [ float(v) if v else None for v in v.split("..") ]
        return NumericRange(limits[0] if len(limits) > 0 else None, limits[1] if len(limits) > 1 else None)
    
    ALL: ClassVar[Self]

NumericRange.ALL = NumericRange(None, None)

class Args(argparse.Namespace):
    voltage: float
    type: list[str]
    power: NumericRange
    resistance: NumericRange
    accuracy: NumericRange
    current: NumericRange
    epsilon: float
    shipment: list[str]
    r1_or_factor: float
    r2: float | None

    @property
    def factor(self):
        return self.r2 / (self.r1_or_factor + self.r2) if self.r2 is not None else self.r1_or_factor

    def parse() -> "Args":
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--voltage", help="reference voltage", type=float, default=5)
        parser.add_argument("-t", "--type", nargs="+", default=[], help="type filter")
        parser.add_argument("-p", "--power", type=NumericRange.parse, default=NumericRange.ALL, help="power filter")
        parser.add_argument("-r", "--resistance", type=NumericRange.parse, default=NumericRange.ALL, help="resistance filter")
        parser.add_argument("-a", "--accuracy", type=NumericRange.parse, default=NumericRange.ALL, help="accuracy filter")
        parser.add_argument("-c", "--current", type=NumericRange.parse, default=NumericRange.ALL, help="current filter")
        parser.add_argument("-e", "--epsilon", type=float, default=0.05, help="absolute tolerance between coefficients")
        parser.add_argument("-s", "--shipment", nargs="+", default=[], help="parcel or shipment name, where to find this resistor")
        parser.add_argument("r1_or_factor", type=float, help="r1 resistance or voltage divider factor (r2/(r1+r2))")
        parser.add_argument("r2", type=float, help="r2 resistance", nargs="?")
        result = Args()
        parser.parse_args(namespace=result)
        return result
    
args: Args = Args.parse()

resistors = [ 
    resistor 
    for resistor in parse_workbook("known_resistors.xlsx") 
    if all(getattr(resistor,name) in getattr(args,name) for name in ["type","power","accuracy","resistance"]) 
]

print(f"searching for factor={args.factor:.5f} v_tev={args.voltage*args.factor:.5f} abs_tol={args.epsilon}")

found_dividers = find_dividers(resistors, args.voltage, args.factor, args.epsilon)
for index, result in enumerate(found_dividers):
    print(f"""======== {index}
Error: {result.error:.5f}
Factor: {result.factor:.5f} 
R total: {result.r_total:.5f}
Current: {result.current:.5f} 
V tev: {result.v_tev:.5f} 
R tev: {result.r_tev:.5f}
R1: {result.r1} 
R2: {result.r2}
""")