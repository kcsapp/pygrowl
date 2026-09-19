"""
Generate data and a population-synthesis analysis plot for that data all in one!

This script runs the COMPAS command locally, either using the binary if available or the docker
image otherwise, and generates the selected plot from the data defined in the
[onboarding notebook](https://github.com/FloorBroekgaarden/GROWL-catalog-public/blob/main/onboarding_growl/introduction_to_population_synthesis.ipynb).
"""

import logging
import os
import sys
from argparse import ArgumentParser
from datetime import datetime, timezone

import growl.io as gio
import growl.plot as gplt
from growl.config import CompasOptions
from growl.constants import StateColumn
from growl.run import run_compas

logging.basicConfig(level=logging.INFO)

OUTPUT_PREFIX = "BSE_Detailed_Output"
STANDARD_COLUMNS = [
    "Time",
    "dT",
    "Mass(1)",
    "Mass(2)",
    "Mass_He_Core(1)",
    "Mass_He_Core(2)",
    "Mass_CO_Core(1)",
    "Mass_CO_Core(2)",
    "Radius(1)",
    "Radius(2)",
    "RocheLobe(1)",
    "RocheLobe(2)",
    "SemiMajorAxis",
    "Eccentricity",
    "Stellar_Type(1)",
    "Stellar_Type(2)",
    "Luminosity(1)",
    "Luminosity(2)",
    "Teff(1)",
    "Teff(2)",
    "MT_History",
    "Unbound",
]
EVENT_COLUMNS: list[StateColumn] = [
    "stellar_type_1",
    "stellar_type_2",
    "mt_history",
]

FIXED_ARGS = [
    "--mode",
    "--detailed-output",
    "--logfile-detailed-output",
]


def main():
    parser = ArgumentParser(
        description=(
            "Generate and plot binary system evolution with COMPAS. Additional arguments are "
            "passed as COMPAS parameters and settings."
        )
    )
    parser.add_argument(
        "--input",
        default="data/input",
        help="Input path where COMPAS will find config files",
    )
    parser.add_argument(
        "--output",
        default="data/logs",
        help="Output path where COMPAS results will be stored",
    )
    parser.add_argument(
        "--rundir",
        default=None,
        help="If specified, generate plots from this directory instead of generating a new output",
    )
    parser.add_argument(
        "--run-index",
        type=int,
        default=0,
        help="The detailed-output file index to generate plots for (0-indexed)",
    )
    parser.add_argument(
        "--plot-type",
        default="summary",
        choices={"masses", "radii", "orbit", "hr_diagram", "summary"},
        help="The plot to generate",
    )

    full_args = sys.argv[1:]
    for arg in full_args:
        if arg in FIXED_ARGS:
            raise ValueError(f"Argument '{arg}' is fixed by this script")

    options, argv = CompasOptions.from_argv(full_args)
    args = parser.parse_args(argv)

    if args.rundir:
        rundir = os.path.join(args.output, args.rundir, "Detailed_Output")
    else:
        # always generate BSE-mode detailed output, and timestamp each run
        ts_suffix = int(datetime.now(timezone.utc).timestamp())
        options = options.evolve(
            mode="BSE",
            detailed_output=True,
            logfile_detailed_output=OUTPUT_PREFIX,
            output_container=f"{options.output_container}_{ts_suffix}",
        )

        # run compas and print the usual output
        output = run_compas(options, args.input, args.output)
        print(f"**** COMPAS output ****\n======================={output.decode()}")

        rundir = os.path.join(args.output, options.output_container, "Detailed_Output")

    # load the data from the standard output file name
    filename = os.path.join(rundir, f"{OUTPUT_PREFIX}_{args.run_index}.h5")
    raw_df = gio.load(filename, STANDARD_COLUMNS)
    event_df = gio.select_events(raw_df, EVENT_COLUMNS)

    # generate the plot
    match args.plot_type:
        case "masses":
            gplt.plot_stellar_masses(raw_df, event_df)
        case "radii":
            gplt.plot_stellar_radii(raw_df, event_df)
        case "orbit":
            gplt.plot_orbit_parameters(raw_df, event_df)
        case "hr_diagram":
            gplt.plot_hr_diagram(raw_df, event_df)
        case "summary":
            gplt.plot_summary(raw_df, event_df)
        case other:
            raise ValueError(f"Invalid plot type: '{other}'")


if __name__ == "__main__":
    main()
