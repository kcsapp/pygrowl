import enum
import re
from dataclasses import dataclass
from functools import cache, cached_property
from typing import Any, Literal

import polars as pl
from pint import get_application_registry

### Useful units ###
ur = get_application_registry()
ur.define("ratio = [fraction]")
ur.define("state = [state]")
ur.define("@alias ratio = metallicity")
# ur.define("Myr = 1e6 * yr")
ratio = ur.ratio
state = ur.state
metallicity = ur.metallicity

K = ur.kelvin
s = ur.second
rad = ur.rad
Hz = ur.hertz
yr = ur.year
Myr = 1e6 * ur.yr
AU = ur.au
Gauss = ur.gauss

Msol = ur.Quantity(1.988475e30, ur.kilogram).plus_minus(0.000092e30)
Rsol = ur.Quantity(6.9566e8, ur.meter).plus_minus(0.0014e8)
Lsol = ur.Quantity(3.828e26, ur.watt)
Zsol = ur.Quantity(0.014, ur.metallicity)


### State defintions ###
class StateEnum(enum.Enum):
    @classmethod
    def _missing_(cls, value: Any):
        return next((v for v in cls if v.state == int(value)))

    @classmethod
    @cache
    def pl_enum(cls) -> pl.Enum:
        return pl.Enum([ev.value[0] for ev in cls])

    @cached_property
    def state(self) -> int:
        return self.value[0]

    @cached_property
    def description(self) -> str:
        return self.value[1]


class BinarySystemState(StateEnum):
    InitialState = (1, "the initial state of the binary")
    PostStellarTimestep = (
        2,
        "stellar timestep (i.e. the evolution of the constituent stars for a single timestep)",
    )
    PostBinaryTimestep = (
        3,
        "binary timestep (i.e. the evolution of the binary system for a single timestep)",
    )
    TimestepCompleted = (
        4,
        "completion of the timestep (after all changes to the binary and components)",
    )
    FinalState = (5, "the final state of the binary")
    StellarTypeChangeDuringCEE = (
        6,
        "a stellar type change during a common envelope event",
    )
    StellarTypeChangeDuringMT = (
        7,
        "a stellar type change during a mass transfer event",
    )
    StellarTypeChangeDuringMassResolution = (
        8,
        "a stellar type change during mass resolution",
    )
    StellarTypeChangeDuringCHEEquilibration = (
        9,
        "a stellar type change during mass equilibration for CHE",
    )
    PostMT = (10, "a mass transfer event")
    PostWinds = (11, "winds mass loss")
    PostCEE = (12, "a common envelope event")
    PostSN = (13, "a supernova event")
    PostMassResolution = (
        14,
        "mass resolution (i.e. after winds mass loss & mass transfer complete)",
    )
    PostMassResolutionMerger = (15, "a merger after mass resolution")
    PreStellarTimestep = (
        16,
        (
            "before a stellar timestep (i.e. the evolution of the constituent stars "
            "for a single timestep)"
        ),
    )


# COMPAS stellar type codes -- from src/typedefs.h in the COMPAS source
class StellarType(StateEnum):
    MainSequenceLowMass = (0, "Main sequence (<= 0.7 Msun)")
    MainSequence = (1, "Main sequence")
    HertzsprungGap = (2, "Hertzsprung gap")
    FirstGiantBranch = (3, "First giant branch")
    CoreHeliumBurn = (4, "Core helium burning")
    EarlyAGB = (5, "Early AGB")
    ThermalPulseAGB = (6, "Thermally pulsing AGB")
    NakedHeMS = (7, "Naked helium star MS")
    NakedHeHG = (8, "Naked helium star HG")
    NakedHeGB = (9, "Naked helium star GB")
    HeWhiteDwarf = (10, "Helium white dwarf")
    COWhiteDwarf = (11, "Carbon-oxygen white dwarf")
    ONeWhiteDwarf = (12, "Oxygen-neon white dwarf")
    NeutronStar = (13, "Neutron star")
    BlackHole = (14, "Black hole")
    MasslessRemnant = (15, "Massless remnant")
    Homogeneous = (16, "Chemically homogeneous")


# COMPAS mass transfer tracking codes -- MT_TRACKING enum in src/typedefs.h
class MassTransferState(StateEnum):
    NoMT = (0, "No mass transfer")
    Stable12 = (1, "Stable mass transfer: star 1 -> star 2")
    Stable21 = (2, "Stable mass transfer: star 2 -> star 1")
    Envelope12 = (3, "Common envelope: star 1 -> star 2 (survived)")
    Envelope21 = (4, "Common envelope: star 2 -> star 1 (survived)")
    EnvelopeDC = (5, "Common envelope: double-core (survived)")
    Merger = (6, "Merger")


class MassTransferTimescale(StateEnum):
    NoMT = (0, "No mass transfer")
    NuclearMT = (1, "Nuclear mass transfer")
    ThermalMT = (2, "Thermal mass transfer")
    EnvelopeMT = (3, "Common envelope mass transfer")


_INDEX_PAT = re.compile(r".*\(([12])\)")


@dataclass
class MeasurementContext:
    name: str
    desc: str
    type: pl.DataType | type[StateEnum]
    unit: ur.Unit

    @cached_property
    def index(self) -> int | None:
        m = _INDEX_PAT.match(self.name)
        return None if not m else int(m.group(1))

    @cached_property
    def colname(self) -> str:
        return self.name.replace(")", "").replace("(", "_").replace("@", "_").lower()

    @cached_property
    def description(self) -> str:
        match self.index:
            case 1:
                return self.desc.format(star="primary star")
            case 2:
                return self.desc.format(star="secondary star")
            case _:
                return self.desc.format(star="binary star system")


COLUMN_DATA: list[MeasurementContext] = [
    MeasurementContext("Age(1)", "Age of the {star}", pl.Float64(), Myr),
    MeasurementContext("Age(2)", "Age of the {star}", pl.Float64(), Myr),
    MeasurementContext(
        "Ang_Momentum(1)",
        "Anuglar momentum of the {star}",
        pl.Float64(),
        Msol * AU**2 / yr,
    ),
    MeasurementContext(
        "Ang_Momentum(2)",
        "Angular momentum of the {star}",
        pl.Float64(),
        Msol * AU**2 / yr,
    ),
    MeasurementContext(
        "Ang_Momentum_Total",
        "Total angular momentum of the {star}",
        pl.Float64(),
        Msol * AU**2 / yr,
    ),
    MeasurementContext(
        "Beta",
        "Fraction of the mass lost from the donor that ends up on the accretor",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Dominant_Mass_Loss_Rate(1)",
        "Rate of mass loss from the dominant source of that loss for the {star}",
        pl.Int32(),
        ratio,
    ),
    MeasurementContext(
        "Dominant_Mass_Loss_Rate(2)",
        "Rate of mass loss from the dominant source of that loss for the {star}",
        pl.Int32(),
        ratio,
    ),
    MeasurementContext(
        "Eccentricity",
        (
            "Deviation from circularity of the orbital of the {star}: the ratio of the "
            "center-to-focus distance to the semi-major axis"
        ),
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Energy_Total", "Total energy of the {star}", pl.Float64(), Msol * AU**2 / yr**2
    ),
    MeasurementContext("Luminosity(1)", "Luminositoy of the {star}", pl.Float64(), Lsol),
    MeasurementContext("Luminosity(2)", "Luminositoy of the {star}", pl.Float64(), Lsol),
    MeasurementContext("MT_History", "Mass Transfer state", MassTransferState, state),
    MeasurementContext("Mass(1)", "Current mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass(2)", "Current mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass@ZAMS(1)", "Mass at ZAMS ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass@ZAMS(2)", "Mass at ZAMS ({star})", pl.Float64(), Msol),
    MeasurementContext(
        "MassTransferRateDonor",
        "The rate at which mass is lost from the donor",
        pl.Float64(),
        Msol / Myr,
    ),
    MeasurementContext(
        "MassTransferTimescale",
        (
            "Mass transfer timescale, as indicated by the type of mass transfer (nuclear, thermal, "
            "common-envelope)"
        ),
        MassTransferTimescale,
        state,
    ),
    MeasurementContext("Mass_0(1)", "Effective initial mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_0(2)", "Effective initial mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_CO_Core(1)", "Carbon-Oxygen core mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_CO_Core(2)", "Carbon-Oxygen core mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_Core(1)", "Core mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_Core(2)", "Core mass ({star})", pl.Float64(), Msol),
    MeasurementContext(
        "Mass_Env(1)",
        "Envelope mass calculated using Hurley et al. (2000) ({star})",
        pl.Float64(),
        Msol,
    ),
    MeasurementContext(
        "Mass_Env(2)",
        "Envelope mass calculated using Hurley et al. (2000) ({star})",
        pl.Float64(),
        Msol,
    ),
    MeasurementContext("Mass_He_Core(1)", "Helium core mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mass_He_Core(2)", "Helium core mass ({star})", pl.Float64(), Msol),
    MeasurementContext("Mdot(1)", "Mass loss rate in winds ({star})", pl.Float64(), Msol / yr),
    MeasurementContext("Mdot(2)", "Mass loss rate in winds ({star})", pl.Float64(), Msol / yr),
    MeasurementContext(
        "Metallicity@ZAMS(1)", "Metallicity of {star} at ZAMS", pl.Float64(), metallicity
    ),
    MeasurementContext(
        "Metallicity@ZAMS(2)", "Metallicity of {star} at ZAMS", pl.Float64(), metallicity
    ),
    MeasurementContext("Omega(1)", "Angular frequency ({star})", pl.Float64(), Hz),
    MeasurementContext("Omega(2)", "Angular frequency ({star})", pl.Float64(), Hz),
    MeasurementContext("Omega_Break(1)", "Break-up angular frequency ({star})", pl.Float64(), Hz),
    MeasurementContext("Omega_Break(2)", "Break-up angular frequency ({star})", pl.Float64(), Hz),
    MeasurementContext(
        "Pulsar_Birth_Period(1)",
        "Pulsar spin period at birth of the {star}",
        pl.Float64(),
        s,
    ),
    MeasurementContext(
        "Pulsar_Birth_Period(2)",
        "Pulsar spin period at birth of the {star}",
        pl.Float64(),
        s,
    ),
    MeasurementContext(
        "Pulsar_Birth_Spin_Down(1)",
        "Pulsar spin-down rate as time derivative of spin frequency ({star})",
        pl.Float64(),
        rad,
    ),
    MeasurementContext(
        "Pulsar_Birth_Spin_Down(2)",
        "Pulsar spin-down rate as time derivative of spin frequency ({star})",
        pl.Float64(),
        rad,
    ),
    MeasurementContext(
        "Pulsar_Mag_Field(1)",
        "Pulsar magnetic field strength ({star})",
        pl.Float64(),
        Gauss,
    ),
    MeasurementContext(
        "Pulsar_Mag_Field(2)",
        "Pulsar magnetic field strength ({star})",
        pl.Float64(),
        Gauss,
    ),
    MeasurementContext(
        "Pulsar_Spin_Down(1)",
        "Pulsar spin-down rate as time derivative of spin frequency ({star})",
        pl.Float64(),
        rad,
    ),
    MeasurementContext(
        "Pulsar_Spin_Down(2)",
        "Pulsar spin-down rate as time derivative of spin frequency ({star})",
        pl.Float64(),
        rad,
    ),
    MeasurementContext(
        "Pulsar_Spin_Period(1)", "Pulsar spin period of the {star}", pl.Float64(), s
    ),
    MeasurementContext(
        "Pulsar_Spin_Period(2)", "Pulsar spin period of the {star}", pl.Float64(), s
    ),
    MeasurementContext("Radius(1)", "Radius of the {star}", pl.Float64(), Rsol),
    MeasurementContext("Radius(2)", "Radius of the {star}", pl.Float64(), Rsol),
    MeasurementContext(
        "Record_Type",
        "Indicator of the state of the {star} in binary evolution",
        BinarySystemState,
        state,
    ),
    MeasurementContext(
        "RocheLobe(1)", "Roche radius at peripasis of the {star}", pl.Float64(), Rsol
    ),
    MeasurementContext(
        "RocheLobe(2)", "Roche radius at peripasis of the {star}", pl.Float64(), Rsol
    ),
    MeasurementContext("SEED", "Random seed value", pl.UInt64(), state),
    MeasurementContext(
        "SemiMajorAxis", "Semi-major axis of the orbit of the {star}", pl.Float64(), Rsol
    ),
    MeasurementContext(
        "Stellar_Type(1)",
        "Indicator of the state of the {star} in binary evolution",
        StellarType,
        state,
    ),
    MeasurementContext(
        "Stellar_Type(2)",
        "Indicator of the state of the {star} in binary evolution",
        StellarType,
        state,
    ),
    MeasurementContext(
        "Stellar_Type@ZAMS(1)",
        "Indicator of the initial state of the {star} in binary evolution",
        StellarType,
        state,
    ),
    MeasurementContext(
        "Stellar_Type@ZAMS(2)",
        "Indicator of the initial state of the {star} in binary evolution",
        StellarType,
        state,
    ),
    MeasurementContext("Tau_Dynamical(1)", "Dynamical time of {star}", pl.Float64(), Myr),
    MeasurementContext("Tau_Dynamical(2)", "Dynamical time of {star}", pl.Float64(), Myr),
    MeasurementContext(
        "Tau_Radial(1)",
        "Radial expansion timescale: e-folding time of stellar radius of {star}",
        pl.Float64(),
        Myr,
    ),
    MeasurementContext(
        "Tau_Radial(2)",
        "Radial expansion timescale: e-folding time of stellar radius of {star}",
        pl.Float64(),
        Myr,
    ),
    MeasurementContext("Tau_Thermal(1)", "Thermal timescale of {star}", pl.Float64(), Myr),
    MeasurementContext("Tau_Thermal(2)", "Thermal timescale of {star}", pl.Float64(), Myr),
    MeasurementContext("Teff(1)", "Effective temperature of {star}", pl.Float64(), K),
    MeasurementContext("Teff(2)", "Effective temperature of {star}", pl.Float64(), K),
    MeasurementContext("Time", "Total time since ZAMS", pl.Float64(), Myr),
    MeasurementContext(
        "Unbound",
        "Indicates whether or not the binary system is unbound",
        pl.UInt8(),
        state,
    ),
    MeasurementContext(
        "Zeta_Hurley(1)",
        "Adiabatic exponent for {star} calculated per Hurley, et al. (2000) using core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Hurley(2)",
        "Adiabatic exponent for {star} calculated per Hurley, et al. (2000) using core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Hurley_He(1)",
        "Adiabatic exponent for {star} calculated per Hurley, et al. (2000) using He core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Hurley_He(2)",
        "Adiabatic exponent for {star} calculated per Hurley, et al. (2000) using He core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Soberman(1)",
        "Adiabatic exponent for {star} calculated per Soberman, et al. (1997) using core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Soberman(2)",
        "Adiabatic exponent for {star} calculated per Soberman, et al. (1997) using core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Soberman_He(1)",
        "Adiabatic exponent for {star} calculated per Soberman, et al. (1997) using He core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext(
        "Zeta_Soberman_He(2)",
        "Adiabatic exponent for {star} calculated per Soberman, et al. (1997) using He core mass",
        pl.Float64(),
        ratio,
    ),
    MeasurementContext("dT", "Current timestep", pl.Float64(), Myr),
    MeasurementContext(
        "dmMT(1)",
        "The amount of mass accreted to or donated from {star} during a mass transfer episode",
        pl.Float64(),
        Msol,
    ),
    MeasurementContext(
        "dmMT(2)",
        "The amount of mass accreted to or donated from {star} during a mass transfer episode",
        pl.Float64(),
        Msol,
    ),
    MeasurementContext(
        "dmWinds(1)",
        "The amount of mass lost from {star} due to winds",
        pl.Float64(),
        Msol,
    ),
    MeasurementContext(
        "dmWinds(2)",
        "The amount of mass lost from {star} due to winds",
        pl.Float64(),
        Msol,
    ),
]

StateColumn = Literal["stellar_type_1", "stellar_type_2", "record_type", "mt_history"]
