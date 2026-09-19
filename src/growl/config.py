from typing import ClassVar, Literal

from growl.args import (
    AllowCompasRange,
    AllowCompasRangeOrSet,
    AllowCompasSet,
    AllowCompasVector,
    GrowlArgs,
    GrowlField,
    growl_transform,
)


@growl_transform
class CompasOptions(GrowlArgs):
    command: ClassVar[str] = "COMPAS"

    add_options_to_sysparms: AllowCompasSet[
        Literal[
            "ALWAYS",
            "GRID",
            "NEVER",
        ],
    ] = GrowlField(
        description=(
            r"Add columns for program options to SSE System Parameters/BSE System Parameters file "
            r"(mode dependent)."
        ),
        default="GRID",
    )
    allow_non_stripped_ecsn: AllowCompasSet[bool] = GrowlField(
        description=r"Allow ECSNe in effectively single progenitors.",
        default=False,
        flag="--allow-non-stripped-ECSN",
    )
    allow_rlof_at_birth: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Allow binaries that have one or both stars in RLOF at birth to evolve as over-contact"
            r" systems."
        ),
        default=True,
    )
    allow_touching_at_birth: AllowCompasSet[bool] = GrowlField(
        description=r"Allow binaries that are touching at birth to be included in the sampling.",
        default=False,
    )
    angular_momentum_conservation_during_circularisation: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Conserve angular momentum when binary is circularised when entering a Mass Transfer "
            r"episode."
        ),
        default=False,
    )
    black_hole_kicks_mode: AllowCompasSet[
        Literal[
            "FULL",
            "REDUCED",
            "ZERO",
            "FALLBACK",
        ],
    ] = GrowlField(
        description=(
            r"Black hole kicks relative to NS kicks (not relevant for `MULLERMANDEL` "
            r"--remnant-mass-prescription)."
        ),
        default="FALLBACK",
    )
    case_bb_stability_prescription: AllowCompasSet[
        Literal[
            "ALWAYS_STABLE",
            "ALWAYS_STABLE_ONTO_NSBH",
            "TREAT_AS_OTHER_MT",
            "ALWAYS_UNSTABLE",
        ],
    ] = GrowlField(
        description=r"Prescription for the stability of case BB/BC mass transfer.",
        default="ALWAYS_STABLE",
    )
    check_photon_tiring_limit: AllowCompasSet[bool] = GrowlField(
        description=r"Check the photon tiring limit is not exceeded during mass loss.",
        default=False,
    )
    chemically_homogeneous_evolution_mode: AllowCompasSet[
        Literal[
            "NONE",
            "OPTIMISTIC",
            "PESSIMISTIC",
        ],
    ] = GrowlField(
        description=(
            r"Chemically Homogeneous Evolution mode. See [Riley2021] for details of the "
            r"implementation of Chemically Homogeneous Evolution in COMPAS"
        ),
        default="PESSIMISTIC",
    )
    circularise_binary_during_mass_transfer: AllowCompasSet[bool] = GrowlField(
        description=r"Circularise binary when it enters a Mass Transfer episode.",
        default=True,
    )
    common_envelope_allow_immediate_rlof_post_ce_survive: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Allow binaries that experience Roche lobe overflow immediately at the end of the CE "
            r"phase to survive."
        ),
        default=False,
        flag="--common-envelope-allow-immediate-RLOF-post-CE-survive",
    )
    common_envelope_allow_main_sequence_survive: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Allow main sequence accretors to survive common envelope evolution if other criteria "
            r"point to survival."
        ),
        default=True,
    )
    common_envelope_allow_radiative_envelope_survive: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Allow binaries with an evolved component with a radiative envelope to survive the "
            r"common envelope phase (they always survive in the `--common-envelope-formalism "
            r"TWO_STAGE` option)."
        ),
        default=False,
    )
    common_envelope_alpha: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Common Envelope efficiency alpha.",
        default=1.0,
    )
    common_envelope_alpha_thermal: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Thermal energy contribution to the total envelope binding energy. Defined such that "
            r"\lambda = \alpha_{th} \times \lambda_{b} + (1.0 - \alpha_{th}) \times \lambda_{g}."
        ),
        default=1.0,
    )
    common_envelope_formalism: AllowCompasSet[
        Literal[
            "ENERGY",
            "TWO_STAGE",
        ],
    ] = GrowlField(
        description=r"CE formalism prescription.",
        default="ENERGY",
    )
    common_envelope_lambda: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Common Envelope lambda. Only used when --common-envelope-lambda-prescription = "
            r"LAMBDA_FIXED."
        ),
        default=0.1,
    )
    common_envelope_lambda_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative constant to be applied to the common envelope lambda parameter for any"
            r" prescription."
        ),
        default=1.0,
    )
    common_envelope_lambda_nanjing_enhanced: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Continuous extrapolation beyond maximum radius range in Nanjing lambda's as "
            r"implemented in StarTrack. Only used when --common-envelope-lambda-prescription = "
            r"LAMBDA_NANJING."
        ),
        default=True,
    )
    common_envelope_lambda_nanjing_interpolate_in_mass: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Interpolate Nanjing lambda parameters across different mass models. Only used when "
            r"--common-envelope-lambda-prescription = LAMBDA_NANJING. Requires "
            r"--common-envelope-lambda-nanjing-enhanced."
        ),
        default=True,
    )
    common_envelope_lambda_nanjing_interpolate_in_metallicity: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Interpolate Nanjing lambda parameters across population I and population II "
            r"metallicity models. Only used when --common-envelope-lambda-prescription = "
            r"LAMBDA_NANJING. Requires --common-envelope-lambda-nanjing-enhanced."
        ),
        default=True,
    )
    common_envelope_lambda_nanjing_use_rejuvenated_mass: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Use rejuvenated or effective ZAMS mass instead of true birth mass when computing "
            r"Nanjing lambda parameters. Only used when --common-envelope-lambda-prescription = "
            r"LAMBDA_NANJING."
        ),
        default=False,
    )
    common_envelope_lambda_prescription: AllowCompasSet[
        Literal[
            "LAMBDA_FIXED",
            "LAMBDA_LOVERIDGE",
            "LAMBDA_NANJING",
            "LAMBDA_KRUCKOW",
            "LAMBDA_DEWI",
        ],
    ] = GrowlField(
        description=r"CE lambda (envelope binding energy) prescription.",
        default="LAMBDA_NANJING",
    )
    common_envelope_mass_accretion_constant: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value of mass accreted by NS/BH during common envelope evolution if assuming all "
            r"NS/BH accrete same amount of mass. Used when "
            r"--common-envelope-mass-accretion-prescription = CONSTANT, ignored otherwise."
        ),
        default=0.0,
    )
    common_envelope_mass_accretion_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Maximum amount of mass accreted by NS/BHs during common envelope evolution (M_\odot)."
        ),
        default=0.1,
    )
    common_envelope_mass_accretion_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Minimum amount of mass accreted by NS/BHs during common envelope evolution (M_\odot)."
        ),
        default=0.04,
    )
    common_envelope_mass_accretion_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "CONSTANT",
            "UNIFORM",
            "MACLEOD",
            "CHEVALIER",
        ],
    ] = GrowlField(
        description=(
            r"Assumption about whether NS/BHs can accrete mass during common envelope evolution. "
            r"ZERO is no accretion; CONSTANT means a fixed amount of accretion determined by "
            r"--common-envelope-mass-accretion-constant; UNIFORM means a uniform random draw "
            r"between --common-envelope-mass-accretion-min and --common-envelope-mass-accretion-max"
            r" (Oslowski et al., 2011);, MACLEOD follows the prescription of MacLeod et al., 2015, "
            r"and CHEVALIER follows the accretion assumptions in Chevalier et al. 1993 as in Model "
            r"2 from van Son et al. 2020"
        ),
        default="ZERO",
    )
    common_envelope_recombination_energy_density: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Recombination energy density (erg g−1).",
        default=15000000000000.0,
    )
    common_envelope_slope_kruckow: AllowCompasSet[str] = GrowlField(
        description=(
            r"Slope for the Kruckow lambda (see Kruckow et al. 2016 as implemented by Vigna-Gomez "
            r"et al. 2018)."
        ),
        default="−0.833333",
    )
    convective_envelope_mass_threshold: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Mass threshold of envelope which should be convective, above which the envelopes of "
            r"giants are labelled convective. Only used for --envelope-state-prescription = "
            r"CONVECTIVE_MASS_FRACTION, ignored otherwise."
        ),
        default=0.1,
    )
    convective_envelope_temperature_threshold: AllowCompasRangeOrSet[int] = GrowlField(
        description=(
            r"Temperature [K] threshold, below which the envelopes of giants are convective. Only "
            r"used for --envelope-state-prescription = FIXED_TEMPERATURE, ignored otherwise."
        ),
        default=5370,
    )
    cool_wind_mass_loss_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative constant for wind mass loss of cool stars, i.e. those with "
            r"temperatures below the VINK_MASS_LOSS_MINIMUM_TEMP (default 12500K)."
        ),
        default=1.0,
    )
    create_yaml_file: str = GrowlField(
        description=r"Creates new YAML file. Argument is filename for new YAML file.",
        default="None",
        flag="--create-YAML-file",
    )
    critical_mass_ratio_hg_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a HG star to a degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=0.21,
        flag="--critical-mass-ratio-HG-degenerate-accretor",
    )
    critical_mass_ratio_hg_non_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a HG star to a non-degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=0.25,
        flag="--critical-mass-ratio-HG-non-degenerate-accretor",
    )
    critical_mass_ratio_ms_high_mass_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a MS star to a degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=0.0,
        flag="--critical-mass-ratio-MS-high-mass-degenerate-accretor",
    )
    critical_mass_ratio_ms_high_mass_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a MS star to a non-degenerate accretor. 0 is "
                r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
                r"CLAEYS, ignored otherwise."
            ),
            default=0.625,
            flag="--critical-mass-ratio-MS-high-mass-non-degenerate-accretor",
        )
    )
    critical_mass_ratio_ms_low_mass_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a MS star to a degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=1.0,
        flag="--critical-mass-ratio-MS-low-mass-degenerate-accretor",
    )
    critical_mass_ratio_ms_low_mass_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a MS star to a non-degenerate accretor. 0 is "
                r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
                r"CLAEYS, ignored otherwise."
            ),
            default=1.44,
            flag="--critical-mass-ratio-MS-low-mass-non-degenerate-accretor",
        )
    )
    critical_mass_ratio_giant_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a giant star to a degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=0.87,
    )
    critical_mass_ratio_giant_non_degenerate_accretor: AllowCompasSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a giant star to a non-degenerate accretor. 0 is "
            r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
            r"CLAEYS, ignored otherwise."
        ),
        default=-1.0,
    )
    critical_mass_ratio_helium_hg_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a helium HG star to a degenerate accretor. 0 is "
            r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
            r"CLAEYS, ignored otherwise."
        ),
        default=0.21,
        flag="--critical-mass-ratio-helium-HG-degenerate-accretor",
    )
    critical_mass_ratio_helium_hg_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a helium HG star to a non-degenerate accretor. 0 "
                r"is always stable, < 0 is disabled. Only used for "
                r"--critical-mass-ratio-prescription CLAEYS, ignored otherwise."
            ),
            default=0.25,
            flag="--critical-mass-ratio-helium-HG-non-degenerate-accretor",
        )
    )
    critical_mass_ratio_helium_ms_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a helium MS star to a degenerate accretor. 0 is "
            r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
            r"CLAEYS, ignored otherwise."
        ),
        default=0.0,
        flag="--critical-mass-ratio-helium-MS-degenerate-accretor",
    )
    critical_mass_ratio_helium_ms_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a helium MS star to a non-degenerate accretor. 0 "
                r"is always stable, < 0 is disabled. Only used for "
                r"--critical-mass-ratio-prescription CLAEYS, ignored otherwise."
            ),
            default=0.0,
            flag="--critical-mass-ratio-helium-MS-non-degenerate-accretor",
        )
    )
    critical_mass_ratio_helium_giant_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a helium giant star to a degenerate accretor. 0 is "
            r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
            r"CLAEYS, ignored otherwise."
        ),
        default=0.87,
    )
    critical_mass_ratio_helium_giant_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a helium giant star to a non-degenerate accretor."
                r" 0 is always stable, < 0 is disabled. Only used for "
                r"--critical-mass-ratio-prescription CLAEYS, ignored otherwise."
            ),
            default=1.28,
        )
    )
    critical_mass_ratio_prescription: AllowCompasSet[
        Literal[
            "NONE",
            "ZERO",
            "CLAEYS",
            "GE",
            "GE_IC",
            "HURLEY_HJELLMING_WEBBINK",
        ],
    ] = GrowlField(
        description=r"Critical mass ratio stability prescription (if any).",
        default="NONE",
    )
    critical_mass_ratio_white_dwarf_degenerate_accretor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical mass ratio for MT from a white dwarf to a degenerate accretor. 0 is always "
            r"stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription CLAEYS, "
            r"ignored otherwise."
        ),
        default=1.6,
    )
    critical_mass_ratio_white_dwarf_non_degenerate_accretor: AllowCompasRangeOrSet[float] = (
        GrowlField(
            description=(
                r"Critical mass ratio for MT from a white dwarf to a non-degenerate accretor. 0 is "
                r"always stable, < 0 is disabled. Only used for --critical-mass-ratio-prescription "
                r"CLAEYS, ignored otherwise."
            ),
            default=0.0,
        )
    )
    debug_classes: AllowCompasVector[str] = GrowlField(
        description=(
            r"Developer-defined debug classes to enable (vector). See Vector program options for "
            r"option format."
        ),
        default="All",
    )
    debug_level: AllowCompasRange[int] = GrowlField(
        description=r"Determines which print statements are displayed for debugging.",
        default=0,
    )
    debug_to_file: bool = GrowlField(
        description=r"Write debug statements to file.",
        default=False,
    )
    detailed_output: bool = GrowlField(
        description=r"Print BSE detailed information to file.",
        default=False,
    )
    eccentricity: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Initial eccentricity for a binary star when evolving in BSE mode.",
        default=0.0,
    )
    eccentricity_distribution: AllowCompasSet[
        Literal[
            "ZERO",
            "FLAT",
            "GELLER+2013",
            "THERMAL",
            "DUQUENNOYMAYOR1991",
            "SANA2012",
        ],
    ] = GrowlField(
        description=r"Initial eccentricity distribution.",
        default="ZERO",
    )
    eccentricity_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum eccentricity to generate.",
        default=1.0,
    )
    eccentricity_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum eccentricity to generate.",
        default=0.0,
    )
    eddington_accretion_factor: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplication factor for Eddington accretion for NS & BH (i.e. > 1 is "
            r"super-eddington and 0 is no accretion)."
        ),
        default=1.0,
    )
    emit_gravitational_radiation: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Emit gravitational radiation at each timestep of binary evolution according to Peters"
            r" 1964."
        ),
        default=False,
    )
    enable_warnings: AllowCompasSet[bool] = GrowlField(
        description=r"Display warning messages to stdout.",
        default=False,
    )
    enable_rotationally_enhanced_mass_loss: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Enable rotationally enhanced mass loss for rapidly rotating stars following Langer "
            r"(1998)"
        ),
        default=False,
    )
    enhance_che_lifetimes_luminosities: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Enhance lifetimes and luminosities of CH stars using a fit to detailed models from "
            r"Szecsi et al. (2015)"
        ),
        default=True,
        flag="--enhance-CHE-lifetimes-luminosities",
    )
    envelope_state_prescription: AllowCompasSet[
        Literal[
            "LEGACY",
            "HURLEY",
            "FIXED_TEMPERATURE",
            "CONVECTIVE_MASS_FRACTION",
        ],
    ] = GrowlField(
        description=(
            r"Prescription for determining whether the envelope of the star is convective or "
            r"radiative."
        ),
        default="LEGACY",
    )
    errors_to_file: bool = GrowlField(
        description=r"Write error messages to file.",
        default=False,
    )
    expel_convective_envelope_above_luminosity_threshold: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Expel convective envelope in a pulsation if the luminosity to mass ratio exceeds the "
            r"threshold given by --luminosity-to-mass-threshold"
        ),
        default=False,
    )
    evolve_double_white_dwarfs: AllowCompasSet[bool] = GrowlField(
        description=r"Continue evolving double white dwarf systems after their formation.",
        default=False,
    )
    evolve_main_sequence_mergers: AllowCompasSet[bool] = GrowlField(
        description=r"Continue evolving the remnant after a main sequence merger.",
        default=False,
    )
    evolve_pulsars: AllowCompasSet[bool] = GrowlField(
        description=r"Evolve pulsar properties of Neutron Stars.",
        default=False,
    )
    evolve_unbound_systems: AllowCompasSet[bool] = GrowlField(
        description=r"Continue evolving stars even if the binary is disrupted.",
        default=True,
    )
    fix_dimensionless_kick_magnitude: AllowCompasSet[str] = GrowlField(
        description=r"Fix dimensionless kick magnitude to this value.",
        default="n/a",
    )
    fp_error_mode: AllowCompasSet[
        Literal[
            "OFF",
            "ON",
            "DEBUG",
        ],
    ] = GrowlField(
        description=r"Specifies the floating-point error handling mode.",
        default="OFF",
    )
    fryer_supernova_engine: AllowCompasSet[
        Literal[
            "DELAYED",
            "RAPID",
        ],
    ] = GrowlField(
        description=(
            r"Supernova engine type if using the remnant mass prescription from [Fryer2012]."
        ),
        default="DELAYED",
    )
    fryer_22_fmix: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Parameter describing the mixing growth time when using the 'FRYER2022' remnant mass "
            r"prescription [Fryer2022]."
        ),
        default=0.5,
    )
    fryer_22_mcrit: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Critical CO core mass for black hole formation when using the 'FRYER2022' remnant "
            r"mass distribution [Fryer2022]."
        ),
        default=5.75,
    )
    grid: str = GrowlField(
        description=r"Grid filename. (See grid file )",
        default="",
    )
    grid_lines_to_process: str = GrowlField(
        description=r"The number of grid file lines to be processed.",
        default="Process",
    )
    grid_start_line: AllowCompasRange[int] = GrowlField(
        description=r"The first line of the grid file to be processed.",
        default=0,
    )
    hdf5_buffer_size: AllowCompasRange[int] = GrowlField(
        description=(
            r"The HDF5 IO buffer size for writing to HDF5 logfiles (number of HDF5 chunks)."
        ),
        default=1,
    )
    hdf5_chunk_size: AllowCompasRange[int] = GrowlField(
        description=(
            r"The HDF5 dataset chunk size to be used when creating HDF5 logfiles (number of logfile"
            r" entries)."
        ),
        default=100000,
    )
    include_wd_binaries_as_dco: AllowCompasSet[bool] = GrowlField(
        description=(
            r"When enabled, changes the definition of \"Double Compact Object\" from a binary "
            r"comprised of any two of {Neutron Star, Black Hole} to a binary star comprised of any "
            r"two of {Helium White Dwarf, Carbon-Oxygen White Dwarf, Oxygen-Neon White Dwarf, "
            r"Neutron Star, Black Hole}."
        ),
        default=False,
        flag="--include-WD-binaries-as-DCO",
    )
    initial_mass: AllowCompasSet[str] = GrowlField(
        description=r"Initial mass for a single star when evolving in SSE mode (M_\odot).",
        default="Sampled",
    )
    initial_mass_1: AllowCompasSet[str] = GrowlField(
        description=r"Initial mass for the primary star when evolving in BSE mode (M_\odot).",
        default="Sampled",
    )
    initial_mass_2: AllowCompasSet[str] = GrowlField(
        description=r"Initial mass for the secondary star when evolving in BSE mode (M_\odot).",
        default="Sampled",
    )
    initial_mass_function: AllowCompasSet[
        Literal[
            "SALPETER",
            "POWERLAW",
            "UNIFORM",
            "KROUPA",
        ],
    ] = GrowlField(
        description=r"Initial mass function.",
        default="KROUPA",
    )
    initial_mass_function_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The maximum mass (in Msol) to sample from the initial mass function (IMF), (only used"
            r" when sampling initial mass) (M_\odot)."
        ),
        default=150.0,
    )
    initial_mass_function_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The minimum mass (in Msol) to sample from the initial mass function (IMF), (only used"
            r" when sampling initial mass) (M_\odot)."
        ),
        default=5.0,
    )
    initial_mass_function_power: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"The power to use when using the POWERLAW IMF.",
        default=0.0,
    )
    kick_direction_distribution: AllowCompasSet[
        Literal[
            "ISOTROPIC",
            "INPLANE",
            "PERPENDICULAR",
            "POWERLAW",
            "WEDGE",
            "POLES",
        ],
    ] = GrowlField(
        description=r"Natal kick direction distribution.",
        default="ISOTROPIC",
    )
    kick_direction_power: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Power for power law kick direction distribution, where 0.0 = isotropic, +ve = polar, "
            r"-ve = in plane."
        ),
        default=0.0,
    )
    kick_magnitude: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value to be used as the (drawn) kick magnitude for a single star when evolving in SSE"
            r" mode, should the star undergo a supernova event (km s^{−1}). If a value for option "
            r"--kick-magnitude-random is specified, it will be used in preference to "
            r"--kick-magnitude."
        ),
        default=0.0,
    )
    kick_magnitude_1: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value to be used as the (drawn) kick magnitude for the primary star of a binary "
            r"system when evolving in BSE mode, should the star undergo a supernova event (km "
            r"s^{−1}). If a value for option --kick-magnitude-random-1 is specified, it will be "
            r"used in preference to --kick-magnitude-1."
        ),
        default=0.0,
    )
    kick_magnitude_2: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value to be used as the (drawn) kick magnitude for the secondary star of a binary "
            r"system when evolving in BSE mode, should the star undergo a supernova event (km "
            r"s^{−1}). If a value for option --kick-magnitude-random-2 is specified, it will be "
            r"used in preference to --kick-magnitude-2."
        ),
        default=0.0,
    )
    kick_magnitude_distribution: AllowCompasSet[
        Literal[
            "ZERO",
            "FIXED",
            "FLAT",
            "MAXWELLIAN",
            "BRAYELDRIDGE",
            "MULLER2016",
            "MULLER2016MAXWELLIAN",
            "MULLERMANDEL",
            "LOGNORMAL",
        ],
    ] = GrowlField(
        description=r"Natal kick magnitude distribution.",
        default="MULLERMANDEL",
    )
    kick_magnitude_max: AllowCompasSet[str] = GrowlField(
        description=(
            r"Maximum drawn kick magnitude (km s^{−1}). Must be > 0 if using "
            r"--kick-magnitude-distribution = FLAT."
        ),
        default="−1.0",
    )
    kick_magnitude_random: AllowCompasSet[float | None] = GrowlField(
        description=(
            r"CDF value to be used to draw the kick magnitude for a single star when evolving in "
            r"SSE mode, should the star undergo a supernova event and should the chosen "
            r"distribution sample from a cumulative distribution function. Must be a floating-point"
            r" number in the range [0.0, 1.0). The specified value for this option will be used in "
            r"preference to any specified value for --kick-magnitude."
        ),
        default=None,
    )
    kick_magnitude_random_1: AllowCompasSet[float | None] = GrowlField(
        description=(
            r"CDF value to be used to draw the kick magnitude for the primary star of a binary "
            r"system when evolving in BSE mode, should the star undergo a supernova event and "
            r"should the chosen distribution sample from a cumulative distribution function. Must "
            r"be a floating-point number in the range [0.0, 1.0). The specified value for this "
            r"option will be used in preference to any specified value for --kick-magnitude-1."
        ),
        default=None,
    )
    kick_magnitude_random_2: AllowCompasSet[float | None] = GrowlField(
        description=(
            r"CDF value to be used to draw the kick magnitude for the secondary star of a binary "
            r"system when evolving in BSE mode, should the star undergo a supernova event and "
            r"should the chosen distribution sample from a cumulative distribution function. Must "
            r"be a floating-point number in the range [0.0, 1.0). The specified value for this "
            r"option will be used in preference to any specified value for --kick-magnitude-2."
        ),
        default=None,
    )
    kick_magnitude_sigma_ccsn_bh: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Sigma for chosen kick magnitude distribution for black holes (km s^{−1}). Ignored if "
            r"not needed for the chosen kick magnitude distribution."
        ),
        default=217.0,
        flag="--kick-magnitude-sigma-CCSN-BH",
    )
    kick_magnitude_sigma_ccsn_ns: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Sigma for chosen kick magnitude distribution for neutron stars (km s^{−1}). Ignored "
            r"if not needed for the chosen kick magnitude distribution."
        ),
        default=217.0,
        flag="--kick-magnitude-sigma-CCSN-NS",
    )
    kick_magnitude_sigma_ecsn: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Sigma for chosen kick magnitude distribution for ECSN (km s^{−1}). Ignored if not "
            r"needed for the chosen kick magnitude distribution."
        ),
        default=30.0,
        flag="--kick-magnitude-sigma-ECSN",
    )
    kick_magnitude_sigma_ussn: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Sigma for chosen kick magnitude distribution for USSN (km s^{−1}). Ignored if not "
            r"needed for the chosen kick magnitude distribution."
        ),
        default=30.0,
        flag="--kick-magnitude-sigma-USSN",
    )
    kick_mean_anomaly_1: AllowCompasSet[float | None] = GrowlField(
        description=(
            r"The mean anomaly at the instant of the supernova for the primary star of a binary "
            r"system when evolving in BSE mode, should it undergo a supernova event. Must be a "
            r"floating-point number in the range [0.0, 2\pi)."
        ),
        default=None,
    )
    kick_mean_anomaly_2: AllowCompasSet[float | None] = GrowlField(
        description=(
            r"The mean anomaly at the instant of the supernova for the secondary star of a binary "
            r"system when evolving in BSE mode, should it undergo a supernova event. Must be a "
            r"floating-point number in the range [0.0, 2\pi)."
        ),
        default=None,
    )
    kick_phi_1: AllowCompasSet[str] = GrowlField(
        description=(
            r"The angle between ’x’ and ’y’, both in the orbital plane of the supernova vector, for"
            r" the primary star of a binary system when evolving in BSE mode, should it undergo a "
            r"supernova event (radians)."
        ),
        default="Drawn",
    )
    kick_phi_2: AllowCompasSet[str] = GrowlField(
        description=(
            r"The angle between ’x’ and ’y’, both in the orbital plane of the supernova vector, for"
            r" the secondary star of a binary system when evolving in BSE mode, should it undergo a"
            r" supernova event (radians)."
        ),
        default="Drawn",
    )
    kick_scaling_factor: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Arbitrary factor used to scale kicks.",
        default=1.0,
    )
    kick_theta_1: AllowCompasSet[str] = GrowlField(
        description=(
            r"The angle between the orbital plane and the ’z’ axis of the supernova vector for the "
            r"primary star of a binary system when evolving in BSE mode, should it undergo a "
            r"supernova event (radians)."
        ),
        default="Drawn",
    )
    kick_theta_2: AllowCompasSet[str] = GrowlField(
        description=(
            r"The angle between the orbital plane and the ’z’ axis of the supernova vector for the "
            r"secondary star of a binary system when evolving in BSE mode, should it undergo a "
            r"supernova event (radians)."
        ),
        default="Drawn",
    )
    lbv_mass_loss_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "HURLEY",
            "HURLEY_ADD",
            "BELCZYNSKI",
        ],
    ] = GrowlField(
        description=r"Luminous blue variable mass loss prescription.",
        default="HURLEY_ADD",
        flag="--LBV-mass-loss-prescription",
    )
    log_classes: AllowCompasVector[str] = GrowlField(
        description=(
            r"Logging classes to be enabled (vector). See Vector program options for option format."
        ),
        default="All",
    )
    logfile_common_envelopes: str = GrowlField(
        description=r"Filename for Common Envelopes logfile (BSE mode).",
        default="BSE_Common_Envelopes",
    )
    logfile_common_envelopes_record_types: str = GrowlField(
        description=r"Enabled record types for Common Envelopes logfile (BSE mode).",
        default="-1",
    )
    logfile_definitions: str = GrowlField(
        description=r"Filename for logfile record definitions file.",
        default="",
    )
    logfile_detailed_output: str = GrowlField(
        description=r"Filename for the BSE/SSE Detailed Output logfile.",
        default="SSE_Detailed_Output",
    )
    logfile_detailed_output_record_types: AllowCompasRange[int] = GrowlField(
        description=r"Enabled record types for the BSE/SSE Detailed Output logfile.",
        default=25,
    )
    logfile_double_compact_objects: str = GrowlField(
        description=r"Filename for the Double Compact Objects logfile (BSE mode).",
        default="BSE_Double_Compact_Objects",
    )
    logfile_double_compact_objects_record_types: str = GrowlField(
        description=r"Enabled record types for the Double Compact Objects logfile (BSE mode).",
        default="-1",
    )
    logfile_name_prefix: str = GrowlField(
        description=r"Prefix for logfile names.",
        default="",
    )
    logfile_pulsar_evolution: str = GrowlField(
        description=r"Filename for the Pulsar Evolution logfile (BSE mode).",
        default="BSE_Pulsar_Evolution",
    )
    logfile_pulsar_evolution_record_types: AllowCompasRange[int] = GrowlField(
        description=r"Enabled record types for the BSE/SSE Pulsar Evolution logfile.",
        default=4,
    )
    logfile_rlof_parameters: str = GrowlField(
        description=r"Filename for the RLOF Printing logfile (BSE mode).",
        default="BSE_RLOF",
    )
    logfile_rlof_parameters_record_types: str = GrowlField(
        description=r"Enabled record types for the RLOF Printing logfile (BSE mode).",
        default="-1",
    )
    logfile_supernovae: str = GrowlField(
        description=r"Filename for the Supernovae logfile.",
        default="SSE_Supernovae",
    )
    logfile_supernovae_record_types: str = GrowlField(
        description=r"Enabled record types for the Supernovae logfile.",
        default="-1",
    )
    logfile_switch_log: str = GrowlField(
        description=r"Filename for the Switch Log logfile.",
        default="SSE_Switch_Log",
    )
    logfile_system_snapshot_log: str = GrowlField(
        description=r"Filename for the System Snapshot logfile.",
        default="SSE_System_Snapshot_Log",
    )
    logfile_system_snapshot_log_record_types: str = GrowlField(
        description=r"Enabled record types for the System Snapshot logfile.",
        default="-1",
    )
    logfile_system_parameters: str = GrowlField(
        description=r"Filename for the System Parameters logfile (BSE mode).",
        default="SSE_System_Parameters",
    )
    logfile_system_parameters_record_types: str = GrowlField(
        description=r"Enabled record types for the System Parameters logfile (BSE mode).",
        default="-1",
    )
    logfile_type: str = GrowlField(
        description=(
            r"The type of logfile to be produced by COMPAS. Options are: HDF5, CSV, TSV, TXT."
        ),
        default="HDF5",
    )
    log_level: AllowCompasRange[int] = GrowlField(
        description=r"Determines which print statements are included in the logfile.",
        default=0,
    )
    luminous_blue_variable_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative constant for LBV mass loss. (Use 10 for Mennekens & Vanbeveren "
            r"(2014)). Note that wind mass loss will also be multiplied by the "
            r"--overall-wind-mass-loss-multiplier."
        ),
        default=1.5,
    )
    luminosity_to_mass_threshold: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Threshold \log_{10}(Luminosity/Mass) (in solar units) above which, if the option "
            r"expel-convective-envelope-above-luminosity-threshold is set to TRUE, pulsations eject"
            r" the convective envelope"
        ),
        default=4.2,
    )
    main_sequence_core_mass_prescription: AllowCompasSet[
        Literal[
            "HURLEY",
            "MANDEL",
            "BRCEK",
        ],
    ] = GrowlField(
        description=r"Main sequence core mass prescription.",
        default="MANDEL",
    )
    maltsev_fallback: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Fixed fallback fraction when using MALTSEV2024 remnant mass prescription (must be "
            r"between 0 and 1). A value of 0.0 means that fallback BHs get no fallback, only the "
            r"mass of the proto-NS remnant (and will get flagged as NSs). A value of 1.0 means that"
            r" fallback BHs get total fallback, taking the mass of the progenitor up to and "
            r"including the He core (but not the H envelope)."
        ),
        default=0.5,
    )
    maltsev_mode: AllowCompasSet[
        Literal[
            "OPTIMISTIC",
            "BALANCED",
            "PESSIMISTIC",
        ],
    ] = GrowlField(
        description=(
            r"Choice of which variant for the MALTSEV remnant mass prescription. Variants pertain "
            r"to the treatment of extrapolation at low metallicities, and are described in detail "
            r"in Willcox+ 2025."
        ),
        default="BALANCED",
    )
    mass_change_fraction: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Approximate desired fractional change in stellar mass on phase when setting SSE and "
            r"BSE timesteps (applied before --timestep--multiplier). Recommended value is 0.005. A "
            r"value of 0.0 means that this choice is ignored, and timestep estimates will be "
            r"calculated by COMPAS."
        ),
        default=0.0,
    )
    mass_loss_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "HURLEY",
            "BELCZYNSKI2010",
            "MERRITT2025",
        ],
    ] = GrowlField(
        description=r"Mass loss prescription.",
        default="MERRITT2025",
    )
    mass_ratio: AllowCompasSet[str] = GrowlField(
        description=(
            r"Mass ratio \frac{m2}{m1} used to determine secondary mass if not specified via "
            r"--initial-mass-2."
        ),
        default="value",
    )
    mass_ratio_distribution: AllowCompasSet[
        Literal[
            "FLAT",
            "DUQUENNOYMAYOR1991",
            "SANA2012",
        ],
    ] = GrowlField(
        description=r"Initial mass ratio distribution for q = \frac{m2}{m1}.",
        default="FLAT",
    )
    mass_ratio_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum mass ratio \frac{m2}{m1} to generate.",
        default=1.0,
    )
    mass_ratio_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum mass ratio \frac{m2}{m1} to generate.",
        default=0.01,
    )
    mass_transfer_accretion_efficiency_prescription: AllowCompasSet[
        Literal[
            "THERMAL",
            "FIXED",
            "HAMSTARS",
        ],
    ] = GrowlField(
        description=r"Mass transfer accretion efficiency prescription.",
        default="THERMAL",
    )
    mass_transfer_angular_momentum_loss_prescription: AllowCompasSet[
        Literal[
            "JEANS",
            "ISOTROPIC",
            "CIRCUMBINARY",
            "KLENCKI_LINEAR",
            "MACLEOD_LINEAR",
            "ARBITRARY",
        ],
    ] = GrowlField(
        description=r"Mass Transfer Angular Momentum Loss prescription.",
        default="ISOTROPIC",
    )
    mass_transfer_fa: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Mass Transfer fraction accreted (beta). Used when "
            r"--mass-transfer-accretion-efficiency-prescription = FIXED."
        ),
        default=0.5,
    )
    mass_transfer_jloss: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Specific angular momentum with which the non-accreted system leaves the system. Used "
            r"when --mass-transfer-angular-momentum-loss-prescription = ARBITRARY, ignored "
            r"otherwise."
        ),
        default=1.0,
    )
    mass_transfer_jloss_linear_fraction_degen: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Specific angular momentum interpolation fraction for degenerate accretors, linear "
            r"between 0 and 1 corresponding to the accretor and L2 point. Used when "
            r"--mass-transfer-angular-momentum-loss-prescription = KLENCKI_LINEAR or "
            r"MACLEOD_LINEAR, ignored otherwise."
        ),
        default=0.5,
    )
    mass_transfer_jloss_linear_fraction_non_degen: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Specific angular momentum interpolation fraction for non-degenerate accretors, linear"
            r" between 0 and 1 corresponding to the accretor and L2 point. Used when "
            r"--mass-transfer-angular-momentum-loss-prescription = KLENCKI_LINEAR or "
            r"MACLEOD_LINEAR, ignored otherwise."
        ),
        default=0.5,
    )
    mass_transfer_rejuvenation_prescription: AllowCompasSet[
        Literal[
            "HURLEY",
            "STARTRACK",
        ],
    ] = GrowlField(
        description=r"Mass Transfer Rejuvenation prescription.",
        default="STARTRACK",
    )
    mass_transfer_thermal_limit_accretor_multiplier: AllowCompasSet[
        Literal[
            "CFACTOR",
            "ROCHELOBE",
        ],
    ] = GrowlField(
        description=r"Mass Transfer Thermal Accretion limit multiplier.",
        default="CFACTOR",
    )
    mass_transfer_thermal_limit_c: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Mass Transfer Thermal rate factor for the accretor.",
        default=10.0,
        flag="--mass-transfer-thermal-limit-C",
    )
    maximum_evolution_time: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Maximum time to evolve binaries (Myr). Evolution of the binary will stop if this "
            r"number is reached."
        ),
        default=13700.0,
    )
    maximum_mass_donor_nandez_ivanova: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Maximum donor mass allowed for the revised common envelope formalism of Nandez & "
            r"Ivanova (M_\odot)."
        ),
        default=2.0,
    )
    maximum_neutron_star_mass: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum mass of a neutron star (M_\odot).",
        default=2.5,
    )
    maximum_number_timestep_iterations: AllowCompasRangeOrSet[int] = GrowlField(
        description=(
            r"Maximum number of timesteps to evolve binary. Evolution of the binary will stop if "
            r"this number is reached."
        ),
        default=99999,
    )
    mcbur1: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Minimum core mass at base of AGB to avoid fully degenerate CO core formation "
            r"(M_\odot). e.g. 1.6 in [Hurley2000] presciption; 1.83 in [Fryer2012] and Belczynski "
            r"et al. (2008) models."
        ),
        default=1.6,
    )
    metallicity: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Metallicity. The value specified for metallicity is applied to both stars for BSE "
            r"mode."
        ),
        default=0.0142,
    )
    metallicity_distribution: AllowCompasSet[
        Literal[
            "ZSOLAR",
            "LOGUNIFORM",
        ],
    ] = GrowlField(
        description=r"Metallicity distribution.",
        default="ZSOLAR",
    )
    metallicity_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum metallicity to generate.",
        default=0.03,
    )
    metallicity_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum metallicity to generate.",
        default=0.0001,
    )
    minimum_sampled_secondary_mass: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Minimum mass value that can be sampled from the IMF when sampling the mass of the "
            r"secondary star (M_\odot)."
        ),
        default=0.1,
    )
    mode: Literal[
        "SSE",
        "BSE",
    ] = GrowlField(
        description=r"The mode of evolution.",
        default="BSE",
    )
    muller_mandel_kick_multiplier_bh: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Scaling prefactor for BH kicks when using the `MULLERMANDEL` kick magnitude "
            r"distribution"
        ),
        default=200.0,
        flag="--muller-mandel-kick-multiplier-BH",
    )
    muller_mandel_kick_multiplier_ns: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Scaling prefactor for NS kicks when using the `MULLERMANDEL` kick magnitude "
            r"distribution"
        ),
        default=630.0,
        flag="--muller-mandel-kick-multiplier-NS",
    )
    muller_mandel_sigma_kick_bh: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Scatter width for BH kicks when using the `MULLERMANDEL` kick magnitude distribution"
        ),
        default=0.45,
        flag="--muller-mandel-sigma-kick-BH",
    )
    muller_mandel_sigma_kick_ns: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Scatter width for NS kicks when using the `MULLERMANDEL` kick magnitude distribution"
        ),
        default=0.45,
        flag="--muller-mandel-sigma-kick-NS",
    )
    natal_kick_for_ppisn: AllowCompasSet[bool] = GrowlField(
        description=(
            r"TRUE indicates PPISN remnants will receive natal kicks via the same prescription as "
            r"CCSN remnants. FALSE indicates PPISN remnants will receive no natal kicks."
        ),
        default=True,
        flag="--natal-kick-for-PPISN",
    )
    neutrino_mass_loss_bh_formation: AllowCompasSet[
        Literal[
            "FIXED_FRACTION",
            "FIXED_MASS",
        ],
    ] = GrowlField(
        description=(
            r"Assumption about neutrino mass loss during BH formation (works with `FRYER2012` or "
            r"`FRYER2022` --remnant-mass-prescription, but not `MULLERMANDEL`)."
        ),
        default="FIXED_MASS",
        flag="--neutrino-mass-loss-BH-formation",
    )
    neutrino_mass_loss_bh_formation_value: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Amount of mass lost in neutrinos during BH formation (either as fraction or in solar "
            r"masses, depending on the value of --neutrino-mass-loss-bh-formation)."
        ),
        default=0.1,
        flag="--neutrino-mass-loss-BH-formation-value",
    )
    neutron_star_accretion_in_ce: AllowCompasSet[
        Literal[
            "ZERO",
            "DISK",
            "SURFACE",
        ],
    ] = GrowlField(
        description=(
            r"Assumption about neutron star accretion in CE. ZERO indicates no accretion onto NS in"
            r" CE. DISK indicates a RLOF like disk accretion onto NS at Alfven radius. SURFACE "
            r"indicates mass is directly accreted onto the surface of the NS."
        ),
        default="ZERO",
    )
    neutron_star_equation_of_state: AllowCompasSet[
        Literal[
            "SSE",
            "ARP3",
        ],
    ] = GrowlField(
        description=r"Neutron star equation of state.",
        default="SSE",
    )
    notes: AllowCompasVector[str] = GrowlField(
        description=r"Annotation strings (vector). See Vector program options for option format.",
        default="",
    )
    notes_hdrs: AllowCompasVector[str] = GrowlField(
        description=(
            r"Annotations header strings (vector). See Vector program options for option format."
        ),
        default="No",
    )
    number_of_systems: AllowCompasRangeOrSet[int] = GrowlField(
        description=(
            r"The number of systems to simulate. Single stars for SSE mode; binary stars for BSE "
            r"mode. This option is ignored if either of the following is true:"
        ),
        default=10,
    )
    ob_mass_loss_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "VINK2001",
            "VINK2021",
            "BJORKLUND2022",
            "KRTICKA2018",
        ],
    ] = GrowlField(
        description=r"Main sequence mass loss prescription.",
        default="VINK2021",
        flag="--OB-mass-loss-prescription",
    )
    orbital_period: AllowCompasSet[str] = GrowlField(
        description=(
            r"Initial orbital period for a binary star when evolving in BSE mode (days). Used only "
            r"if the semi-major axis is not specified via --semi-major-axis."
        ),
        default="value",
    )
    orbital_period_distribution: AllowCompasSet[Literal["FLATINLOG",],] = GrowlField(
        description=r"Initial orbital period distribution.",
        default="FLATINLOG",
    )
    orbital_period_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum period to generate (days).",
        default=1000.0,
    )
    orbital_period_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum period to generate (days).",
        default=1.1,
    )
    output_container: str = GrowlField(
        description=r"Container (directory) name for output files.",
        default="COMPAS_Output",
    )
    output_path: str = GrowlField(
        description=(
            r"Path to which output is saved (i.e. directory in which the output container is "
            r"created)."
        ),
        default="",
    )
    overall_wind_mass_loss_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative constant for overall wind mass loss. Note that this multiplication "
            r"factor is applied after the luminous-blue-variable-multiplier, the "
            r"wolf-rayet-multiplier, and the cool-wind-mass-loss-multiplier."
        ),
        default=1.0,
    )
    pair_instability_supernovae: AllowCompasSet[bool] = GrowlField(
        description=r"Enable pair instability supernovae (PISN).",
        default=True,
    )
    pisn_lower_limit: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum core mass for PISN (M_\odot).",
        default=60.0,
        flag="--PISN-lower-limit",
    )
    pisn_upper_limit: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum core mass for PISN (M_\odot).",
        default=135.0,
        flag="--PISN-upper-limit",
    )
    population_data_printing: bool = GrowlField(
        description=r"Print details of population.",
        default=False,
    )
    ppi_co_core_shift_hendriks: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Shift in CO core mass for PPI (in Msol) for the Hendriks+23 PPI prescription",
        default=0.0,
        flag="--PPI-CO-Core-Shift-Hendriks",
    )
    ppi_lower_limit: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum core mass for PPI (M_\odot).",
        default=35.0,
        flag="--PPI-lower-limit",
    )
    ppi_upper_limit: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum core mass for PPI (M_\odot).",
        default=60.0,
        flag="--PPI-upper-limit",
    )
    print_bool_as_string: bool = GrowlField(
        description=r"Print boolean properties as ’TRUE’ or ’FALSE’.",
        default=False,
    )
    pulsar_birth_magnetic_field_distribution: AllowCompasSet[
        Literal[
            "FLATINLOG",
            "UNIFORM",
            "LOGNORMAL",
        ],
    ] = GrowlField(
        description=r"Pulsar birth magnetic field distribution.",
        default="LOGNORMAL",
    )
    pulsar_birth_magnetic_field_distribution_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum (log_{10}) pulsar birth magnetic field.",
        default=13.0,
    )
    pulsar_birth_magnetic_field_distribution_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum (log_{10}) pulsar birth magnetic field.",
        default=11.0,
    )
    pulsar_birth_magnetic_field_distribution_mean: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Mean of lognormal (log_{10}) pulsar birth magnetic field.",
        default=12.65,
    )
    pulsar_birth_magnetic_field_distribution_sigma: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Sigma of lognormal (log_{10}) pulsar birth magnetic field.",
        default=0.55,
    )
    pulsar_birth_spin_period_distribution: AllowCompasSet[
        Literal[
            "UNIFORM",
            "NORMAL",
        ],
    ] = GrowlField(
        description=r"Pulsar birth spin period distribution.",
        default="NORMAL",
    )
    pulsar_birth_spin_period_distribution_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum pulsar birth spin period (ms).",
        default=100.0,
    )
    pulsar_birth_spin_period_distribution_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum pulsar birth spin period (ms).",
        default=10.0,
    )
    pulsar_birth_spin_period_distribution_mean: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Mean of normal pulsar birth spin period (ms) distribution.",
        default=75.0,
    )
    pulsar_birth_spin_period_distribution_sigma: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Sigma of normal pulsar birth spin period (ms) distribution.",
        default=25.0,
    )
    pulsar_magnetic_field_decay_massscale: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Mass scale on which magnetic field decays during accretion (M_\odot).",
        default=0.025,
    )
    pulsar_magnetic_field_decay_timescale: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Timescale on which magnetic field decays (Myr).",
        default=1000.0,
    )
    pulsar_minimum_magnetic_field: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"log_{10} of the minimum pulsar magnetic field (Gauss).",
        default=8.0,
    )
    pulsational_pair_instability: AllowCompasSet[bool] = GrowlField(
        description=r"Enable mass loss due to pulsational-pair-instability (PPI).",
        default=True,
    )
    pulsational_pair_instability_prescription: AllowCompasSet[
        Literal[
            "HENDRIKS",
            "WOOSLEY",
            "STARTRACK",
            "MARCHANT",
            "FARMER",
        ],
    ] = GrowlField(
        description=(
            r"Pulsational pair instability prescription (only relevant when using "
            r"--pulsational-pair-instability)."
        ),
        default="MARCHANT",
    )
    quiet: bool = GrowlField(
        description=r"Suppress printing to stdout.",
        default=False,
    )
    radial_change_fraction: AllowCompasRangeOrSet[int] = GrowlField(
        description=(
            r"Approximate desired fractional change in stellar radius on phase when setting SSE and"
            r" BSE timesteps (applied before --timestep--multiplier). Recommended value is 0.005. A"
            r" value of 0.0 means that this choice is ignored and timestep estimates will be "
            r"calculated by COMPAS."
        ),
        default=0,
    )
    random_seed: AllowCompasRangeOrSet[int] = GrowlField(
        description=r"Value to use as the seed for the random number generator.",
        default=0,
    )
    remnant_mass_prescription: AllowCompasSet[
        Literal[
            "HURLEY2000",
            "BELCZYNSKI2002",
            "FRYER2012",
            "FRYER2022",
            "MULLER2016",
            "MULLERMANDEL",
            "SCHNEIDER2020",
            "SCHNEIDER2020ALT",
            "MALTSEV2024",
        ],
    ] = GrowlField(
        description=r"Remnant mass prescription.",
        default="MULLERMANDEL",
    )
    response_to_spin_up: AllowCompasSet[
        Literal[
            "TRANSFER_TO_ORBIT",
            "KEPLERIAN_LIMIT",
            "NO_LIMIT",
        ],
    ] = GrowlField(
        description=r"Response of the star to super-critical accretion-induced spin-up",
        default="TRANSFER_TO_ORBIT",
    )
    revised_energy_formalism_nandez_ivanova: AllowCompasSet[bool] = GrowlField(
        description=r"Enable revised energy formalism of Nandez & Ivanova.",
        default=False,
    )
    rlof_printing: bool = GrowlField(
        description=r"Print RLOF events to logfile.",
        default=True,
    )
    rocket_kick_magnitude_1: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Magnitude of post-SN pulsar rocket kick for the primary, in km/s.",
        default=0.0,
    )
    rocket_kick_magnitude_2: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Magnitude of post-SN pulsar rocket kick for the secondary, in km/s.",
        default=0.0,
    )
    rocket_kick_phi_1: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The in-plane angle [0.0, 2pi) of the rocket kick velocity that primary neutron star "
            r"receives following the supernova."
        ),
        default=0.0,
    )
    rocket_kick_phi_2: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The in-plane angle [0.0, 2pi) of the rocket kick velocity that secondary neutron star"
            r" receives following the supernova."
        ),
        default=0.0,
    )
    rocket_kick_theta_1: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The polar angle [0, pi] of the rocket kick velocity that primary neutron star "
            r"receives following the supernova. 0 is aligned with orbital AM."
        ),
        default=0.0,
    )
    rocket_kick_theta_2: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"The polar angle [0, pi]` of the rocket kick velocity that secondary neutron star "
            r"receives following the supernova. 0 is aligned with orbital AM."
        ),
        default=0.0,
    )
    rotational_frequency: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Initial rotational frequency of the star for SSE (Hz).",
        default=0.0,
    )
    rotational_frequency_1: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Initial rotational frequency of the primary star for BSE (Hz).",
        default=0.0,
    )
    rotational_frequency_2: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Initial rotational frequency of the secondary star for BSE (Hz).",
        default=0.0,
    )
    rotational_velocity_distribution: AllowCompasSet[
        Literal[
            "ZERO",
            "HURLEY",
            "VLTFLAMES",
        ],
    ] = GrowlField(
        description=r"Initial rotational velocity distribution.",
        default="ZERO",
    )
    rsg_mass_loss_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "VINKSABHAHIT2023",
            "BEASOR2020",
            "DECIN2023",
            "YANG2023",
            "KEE2021",
            "NJ90",
        ],
    ] = GrowlField(
        description=r"Red supergiant mass loss prescription.",
        default="DECIN2023",
        flag="--RSG-mass-loss-prescription",
    )
    scale_che_mass_loss_with_surface_helium_abundance: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Scale mass loss for chemically homogeneously evolving (CHE) stars with the surface "
            r"helium abundance. Transition from OB to WR mass loss towards the end of the main "
            r"sequence."
        ),
        default=True,
        flag="--scale-CHE-mass-loss-with-surface-helium-abundance",
    )
    scale_terminal_wind_velocity_with_metallicity_power: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Scale terminal wind velocity with metallicity to this power",
        default=0.0,
    )
    semi_major_axis: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Initial semi-major axis for a binary star when evolving in BSE mode (AU).",
        default=0.1,
    )
    semi_major_axis_distribution: AllowCompasSet[
        Literal[
            "FLATINLOG",
            "DUQUENNOYMAYOR1991",
            "SANA2012",
        ],
    ] = GrowlField(
        description=r"Initial semi-major axis distribution.",
        default="FLATINLOG",
    )
    semi_major_axis_max: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Maximum semi-major axis to generate (AU).",
        default=1000.0,
    )
    semi_major_axis_min: AllowCompasRangeOrSet[float] = GrowlField(
        description=r"Minimum semi-major axis to generate (AU).",
        default=0.01,
    )
    stellar_zeta_prescription: AllowCompasSet[
        Literal[
            "SOBERMAN",
            "HURLEY",
            "ARBITRARY",
        ],
    ] = GrowlField(
        description=r"Prescription for convective donor radial response zeta.",
        default="SOBERMAN",
    )
    store_input_files: bool = GrowlField(
        description=(
            r"Enables copying of any specified grid file and/or logfile-definitios file to the "
            r"COMPAS output container."
        ),
        default=True,
    )
    switch_log: AllowCompasSet[bool] = GrowlField(
        description=r"Enables printing of the Switch Log logfile.",
        default=False,
    )
    system_snapshot_age_thresholds: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Age thresholds for the System Snapshot logfile. This is a vector option: one or more "
            r"age threshold values may be specified. See Vector program options for option format. "
            r"In SSE mode, writing to the System Snapshot logfile is triggered when the age of the "
            r"star exceeds any of the age thresholds set. A record is written to the System "
            r"Snapshot logfile on the first timestep at which the age threshold is exceeded. In BSE"
            r" mode, writing to the System Snapshot logfile is triggered when the age of either of "
            r"the constituent stars exceeds any of the age thresholds set. A record is written to "
            r"the System Snapshot logfile on the first timestep at which the age threshold is "
            r"exceeded. It is possible for two records to be logged for each age threshold if the "
            r"constiuent stars exceed the threshold on different timesteps. Note that the age of "
            r"stars may be reduced for various reasons (phase change, rejuvenation, winds/mass "
            r"transfer, etc.), and if the age of a star drops below an age threshold, another "
            r"record will be logged if the star then ages beyond the same threshold (so several "
            r"records might be logged for the same star crossing the same threshold if the age of "
            r"the star oscillates around the threshold)."
        ),
        default=None,
    )
    system_snapshot_time_thresholds: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Time thresholds for the System Snapshot logfile. This is a vector option: one or more"
            r" time threshold values may be specified. See Vector program options for option "
            r"format. In SSE and BSE mode, writing to the System Snapshot logfile is triggered when"
            r" the simulation time exceeds any of the time thresholds set. A record is written to "
            r"the System Snapshot logfile on the first timestep at which the simulation time "
            r"threshold is exceeded."
        ),
        default=None,
    )
    tides_prescription: AllowCompasSet[
        Literal[
            "NONE",
            "PERFECT",
            "KAPIL2026",
            "ZAHN1977",
        ],
    ] = GrowlField(
        description=r"Prescription for tidal evolution of the binary.",
        default="NONE",
    )
    timestep_filename: str = GrowlField(
        description=r"User-defined timesteps filename. (See Timestep files )",
        default="",
    )
    timestep_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative factor for timestep duration. This multiplier is applied after the "
            r"timesteps are chosen using other program options such as --radial-change-fraction and"
            r" --mass-change-fraction, and will therefore override expected behaviour. This option "
            r"can be used in conjunction with --timestep-multipliers, in which case this "
            r"multiplier, and the appropriate phase-dependent multiplier (specified by "
            r"--timestep-multipliers) are both applied."
        ),
        default=1.0,
    )
    timestep_multipliers: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Phase-dependent multiplicative factors for timestep duration. This is a vector "
            r"option: one or more timestep multiplier values may be specified. See Vector program "
            r"options for option format. A multiplicative factor can be specified for each phase "
            r"(stellar type), where the ordinal value (zero-based) of the option value indicates "
            r"the stellar type (from MS_LTE_07 to CHEMICALLY_HOMOGENEOUS, see stellar type list at "
            r"../../Developer guide/Headers/typedefs-dot-h>). This multiplier is applied after the "
            r"timesteps are chosen using other program options such as --radial-change-fraction and"
            r" --mass-change-fraction, and will therefore override expected behaviour. This option "
            r"can be used in conjunction with --timestep-multiplier, in which case that multiplier,"
            r" and the appropriate phase-dependent multiplier (specified by --timestep-multipliers)"
            r" are both applied."
        ),
        default=1.0,
    )
    use_mass_transfer: AllowCompasSet[bool] = GrowlField(
        description=r"Enable mass transfer.",
        default=True,
    )
    ussn_kicks_override_mandel_muller: AllowCompasSet[bool] = GrowlField(
        description=(
            r"Use user-defined USSN kicks (as a fixed value) in lieu of the Mandel & Muller kick "
            r"prescription for USSNe."
        ),
        default=False,
        flag="--USSN-kicks-override-mandel-muller",
    )
    vms_mass_loss_prescription: AllowCompasSet[
        Literal[
            "ZERO",
            "VINK2011",
            "SABHAHIT2023",
            "BESTENLEHNER2020",
        ],
    ] = GrowlField(
        description=r"Very massive main sequence mass loss prescription.",
        default="SABHAHIT2023",
        flag="--VMS-mass-loss-prescription",
    )
    wolf_rayet_multiplier: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Multiplicative constant for Wolf Rayet winds. Note that wind mass loss will also be "
            r"multiplied by the overall-wind-mass-loss-multiplier."
        ),
        default=1.0,
    )
    wr_mass_loss_prescription: AllowCompasSet[
        Literal[
            "BELCZYNSKI2010",
            "SANDERVINK2023",
            "SHENAR2019",
            "ZERO",
        ],
    ] = GrowlField(
        description=r"Wolf-Rayet mass loss prescription.",
        default="SANDERVINK2023",
        flag="--WR-mass-loss-prescription",
    )
    yaml_template: str = GrowlField(
        description=r"Template filename for creation of YAML file (see also --create-YAML-file).",
        default="",
        flag="--YAML-template",
    )
    zeta_adiabatic_arbitrary: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value of logarithmic derivative of radius with respect to mass, \zeta adiabatic."
        ),
        default=10000.0,
    )
    zeta_main_sequence: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value of logarithmic derivative of radius with respect to mass, \zeta on the main "
            r"sequence."
        ),
        default=2.0,
    )
    zeta_radiative_giant_star: AllowCompasRangeOrSet[float] = GrowlField(
        description=(
            r"Value of logarithmic derivative of radius with respect to mass, \zeta for "
            r"radiative-envelope giant-like stars (including Hertzsprung Gap (HG) stars)."
        ),
        default=6.5,
    )
