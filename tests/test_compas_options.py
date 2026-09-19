from typing import ClassVar, Literal

import pytest

from growl.args import (
    AllowCompasRangeOrSet,
    AllowCompasSet,
    AllowCompasVector,
    CompasRange,
    CompasSet,
    GrowlArgs,
    GrowlField,
    growl_transform,
)


@growl_transform
class FakeCompasOptions(GrowlArgs):
    command: ClassVar[str] = "COMPAS"

    metallicity: AllowCompasRangeOrSet[float] = GrowlField(default=None)
    output_path: str | None = GrowlField(default=None)
    eccentricity_distribution: AllowCompasSet[
        Literal["ZERO", "FLAT", "GELLER+2013", "THERMAL", "DUQUENNOYMAYOR1991", "SANA2012"]
    ] = GrowlField(default="ZERO")
    black_hole_kicks_mode: AllowCompasSet[Literal["FULL", "REDUCED", "ZERO", "FALLBACK"]] = (
        GrowlField(default="FALLBACK")
    )
    notes: AllowCompasVector[str] = GrowlField(default=None)


@pytest.fixture
def compas_argv() -> list[str]:
    return [
        "COMPAS",
        "--metallicity",
        "r[0.0001,5,0.0013]",
        "--output-path",
        "/data/compas-run",
        "--eccentricity-distribution",
        "ZERO",
        "--black-hole-kicks-mode",
        "s[FULL,REDUCED,ZERO]",
        "--notes",
        "[,,annotation3,,annotation5]",
    ]


@pytest.fixture
def non_compas_argv() -> list[str]:
    return ["--other", "test"]


@pytest.fixture
def compas_options() -> FakeCompasOptions:
    return FakeCompasOptions(
        metallicity=CompasRange(0.0001, 5, 0.0013),
        output_path="/data/compas-run",
        black_hole_kicks_mode=CompasSet(("FULL", "REDUCED", "ZERO")),
        notes=("", "", "annotation3", "", "annotation5"),
    )


def test_growl_args_to_argv(compas_argv, compas_options):
    re_argv = compas_options.to_argv()
    assert compas_argv == re_argv


def test_argv_to_growl_args(compas_argv, non_compas_argv, compas_options):
    re_opts, remaining = FakeCompasOptions.from_argv(compas_argv + non_compas_argv)
    assert compas_options == re_opts
    assert non_compas_argv == remaining
