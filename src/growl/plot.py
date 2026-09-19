import matplotlib.pyplot as plt
import polars as pl
from matplotlib.lines import Line2D

from .constants import MassTransferState, StellarType

### plotting style: keep grid/axes recessive so the data dominates ###
plt.rcParams.update(
    {
        "figure.dpi": 110,
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": ":",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
    }
)

# Colour convention, matching GWLandscape output:
#   star 1 = red, star 2 = blue, whole system = black.
# We ALSO vary linestyle, so the plots stay readable in greyscale / for colour-blind readers.
C1, C2, CSYS = "#C1272D", "#0B5FA5", "#222222"


def plot_stellar_masses(lazy_df: pl.LazyFrame, lazy_events: pl.LazyFrame):
    _, ax = plt.subplots(figsize=(9, 5))

    df: pl.DataFrame = lazy_df.select(
        "time", "mass_1", "mass_2", "mass_he_core_1", "mass_he_core_2"
    ).collect()

    ax.plot(
        df["time"],
        df["mass_1"] + df["mass_2"],
        color=CSYS,
        lw=2,
        label="Total system mass",
    )
    ax.plot(df["time"], df["mass_1"], color=C1, lw=2, label="Star 1 — total mass")
    ax.plot(df["time"], df["mass_2"], color=C2, lw=2, label="Star 2 — total mass")

    ax.plot(
        df["time"],
        df["mass_he_core_1"],
        color=C1,
        lw=1.5,
        ls="--",
        label="Star 1 — He core",
    )
    ax.plot(
        df["time"],
        df["mass_he_core_2"],
        color=C2,
        lw=1.5,
        ls="--",
        label="Star 2 — He core",
    )

    # annotate the two interaction episodes
    events = (
        lazy_events.select("time_final", "event_types")
        .filter(pl.col("event_types").list.contains("mt_history"))
        .collect()
    )
    for ev in events.iter_rows():
        ax.axvline(ev[0], color="grey", lw=1, ls="-", alpha=0.5, zorder=0)

    ax.set_ylim(-3, 95)  # headroom so the legend sits clear above the data
    ax.annotate(
        "stable mass transfer\n1 → 2 strips star 1",
        xy=(6.13, 22),
        xytext=(3.4, 18),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )
    ax.annotate(
        "common\nenvelope",
        xy=(7.58, 30),
        xytext=(6.9, 12),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )

    ax.set_xlabel("Time [Myr]")
    ax.set_ylabel(r"Mass [M$_\odot$]")
    ax.set_title("Masses of both stars over the life of the binary", loc="left", fontsize=12)
    ax.legend(loc="upper left", fontsize=9, ncol=3)
    plt.tight_layout()
    plt.show()


def plot_stellar_radii(lazy_df: pl.LazyFrame, lazy_events: pl.LazyFrame):
    del lazy_events
    _, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    df = lazy_df.select("time", "radius_1", "radius_2", "rochelobe_1", "rochelobe_2").collect()

    for ax, star, colour in [(axes[0], 1, C1), (axes[1], 2, C2)]:
        ax.plot(
            df["time"],
            df[f"radius_{star}"],
            color=colour,
            lw=2,
            label=f"Star {star} — stellar radius",
        )
        ax.plot(
            df["time"],
            df[f"rochelobe_{star}"],
            color=colour,
            lw=1.5,
            ls="--",
            label=f"Star {star} — Roche lobe radius",
        )

        # shade the intervals where this star overflows its Roche lobe
        overflowing = df[f"radius_{star}"] >= df[f"rochelobe_{star}"]
        ax.fill_between(
            df["time"],
            1e-2,
            1e4,
            where=overflowing,
            color="grey",
            alpha=0.25,
            label="Roche lobe overflow",
            zorder=0,
        )

        ax.set_yscale("log")
        ax.set_ylim(0.5, 5e3)
        ax.set_ylabel(r"Radius [R$_\odot$]")
        ax.legend(loc="upper left", fontsize=9)

    axes[0].set_title(
        "Stellar radius vs Roche lobe radius — mass transfer starts where they meet",
        loc="left",
        fontsize=12,
    )
    axes[1].set_xlabel("Time [Myr]")
    plt.tight_layout()
    plt.show()


def plot_orbit_parameters(lazy_df: pl.LazyFrame, lazy_events: pl.LazyFrame):
    _, axes = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)

    df = lazy_df.select("time", "semimajoraxis", "eccentricity", "mt_history").collect()

    axes[0].plot(df["time"], df["semimajoraxis"], color=CSYS, lw=2)
    axes[0].set_yscale("log")
    axes[0].set_ylabel(r"Semi-major axis $a$ [R$_\odot$]")
    axes[0].set_title(
        "The orbit: widened by mass transfer, then crushed by the common envelope",
        loc="left",
        fontsize=12,
    )

    axes[1].plot(df["time"], df["eccentricity"], color=CSYS, lw=2)
    axes[1].set_ylabel("Eccentricity $e$")
    axes[1].set_xlabel("Time [Myr]")
    axes[1].set_ylim(-0.05, 1.0)

    events = (
        lazy_events.select("time_final", "event_types")
        .filter(pl.col("event_types").list.contains("mt_history"))
        .collect()
    )
    for ax in axes:
        for ev in events.iter_rows():
            ax.axvline(ev[0], color="grey", lw=1, alpha=0.6, zorder=0)

    axes[0].annotate(
        "mass transfer widens\nthe orbit",
        xy=(6.3, 1990),
        xytext=(3.2, 1500),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )
    axes[0].annotate(
        "common envelope\ncrushes the orbit",
        xy=(7.6, 40),
        xytext=(5.3, 25),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )

    plt.tight_layout()
    plt.show()

    # Find the common envelope from the data itself (MT_History == 4), rather than
    # hard-coding a time: the row before it starts is the orbit "just before" the CE.
    ce_start = df["mt_history"].index_of(MassTransferState.Envelope21.state)
    if ce_start is None:
        print(f"No {MassTransferState.Envelope21.description} found ")
        return

    a_before = df["semimajoraxis"][ce_start - 1]
    a_at_ce = df["semimajoraxis"][ce_start]
    a_final = df["semimajoraxis"][-1]

    print(f"Separation just before the common envelope : {a_before:8.2f} Rsun")
    print(f"Separation just after  the common envelope : {a_at_ce:8.2f} Rsun")
    print(f"  --> the CE shrank the orbit by a factor of {a_before / a_at_ce:.1f}")
    print(f"Final separation of the binary black hole   : {a_final:8.2f} Rsun")


def plot_hr_diagram(lazy_df: pl.LazyFrame, lazy_events: pl.LazyFrame):
    del lazy_events
    _, ax = plt.subplots(figsize=(8, 6.5))

    df = lazy_df.select(
        "stellar_type_1", "stellar_type_2", "teff_1", "teff_2", "luminosity_1", "luminosity_2"
    ).collect()

    # only plot while each object is still a star -- black holes have no meaningful Teff/L
    for star, colour, name in [(1, C1, "Star 1"), (2, C2, "Star 2")]:
        star_df = df.filter(pl.col(f"stellar_type_{star}") <= 9)
        teff, lumi = star_df[f"teff_{star}"], star_df[f"luminosity_{star}"]
        ax.plot(teff, lumi, color=colour, lw=1.8, label=name)
        ax.plot(teff[0], lumi[0], "o", color=colour, ms=9, mec="white", mew=1.5)
        ax.plot(teff[-1], lumi[-1], "*", color=colour, ms=17, mec="white", mew=1)

    # the Sun, for scale -- note how far below these massive stars it sits
    ax.plot(5772, 1.0, "o", color="orange", ms=9, mec="black", mew=0.6)
    ax.annotate(
        "the Sun\n(for scale)",
        xy=(5772, 1.0),
        xytext=(9000, 6),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()  # HR convention: hot on the LEFT
    ax.set_xlabel(r"Effective temperature $T_{\rm eff}$ [K]  $\longleftarrow$ hotter")
    ax.set_ylabel(r"Luminosity [L$_\odot$]")
    ax.set_title(
        "Hertzsprung–Russell diagram: the evolutionary tracks of both stars",
        loc="left",
        fontsize=12,
    )

    handles = [
        Line2D([], [], color=C1, lw=2, label="Star 1"),
        Line2D([], [], color=C2, lw=2, label="Star 2"),
        Line2D([], [], color="grey", marker="o", ls="none", label="birth (ZAMS)"),
        Line2D(
            [],
            [],
            color="grey",
            marker="*",
            ls="none",
            ms=13,
            label="last moment as a star",
        ),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=9)
    plt.tight_layout()
    plt.show()


def plot_summary(lazy_df: pl.LazyFrame, lazy_events: pl.LazyFrame):
    _, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    df: pl.DataFrame = lazy_df.select(
        "time",
        "mass_1",
        "mass_2",
        "mass_he_core_1",
        "mass_he_core_2",
        "radius_1",
        "radius_2",
        "rochelobe_1",
        "rochelobe_2",
        "semimajoraxis",
        "eccentricity",
        "stellar_type_1",
        "stellar_type_2",
        "unbound",
    ).collect()

    # --- panel 1: masses -----------------------------------------------------------
    ax = axes[0]
    ax.plot(df["time"], df["mass_1"], color=C1, lw=2, label="Star 1")
    ax.plot(df["time"], df["mass_2"], color=C2, lw=2, label="Star 2")
    ax.plot(df["time"], df["mass_he_core_1"], color=C1, lw=1.3, ls="--", label="Star 1 He core")
    ax.plot(df["time"], df["mass_he_core_2"], color=C2, lw=1.3, ls="--", label="Star 2 He core")
    ax.set_ylabel(r"Mass [M$_\odot$]")
    ax.set_ylim(-2, 52)  # headroom for the legend and annotations
    ax.legend(fontsize=8, ncol=4, loc="upper left")
    ax.set_title("The complete life of a binary black hole progenitor", loc="left", fontsize=13)

    # --- panel 2: radii and Roche lobes --------------------------------------------
    ax = axes[1]
    ax.plot(df["time"], df["radius_1"], color=C1, lw=2, label="Star 1 radius")
    ax.plot(df["time"], df["radius_2"], color=C2, lw=2, label="Star 2 radius")
    ax.plot(df["time"], df["rochelobe_1"], color=C1, lw=1.3, ls="--", label="Star 1 Roche lobe")
    ax.plot(df["time"], df["rochelobe_2"], color=C2, lw=1.3, ls="--", label="Star 2 Roche lobe")
    ax.set_yscale("log")
    # Clip the y-axis to stellar radii: after collapse the "radius" is the compact
    # object's (~1e-4 Rsun, a few km), which would otherwise squash the whole panel.
    ax.set_ylim(0.5, 5e3)
    ax.set_ylabel(r"Radius [R$_\odot$]")
    ax.legend(fontsize=8, ncol=2, loc="lower left")

    # --- panel 3: separation -------------------------------------------------------
    ax = axes[2]
    ax.plot(df["time"], df["semimajoraxis"], color=CSYS, lw=2)
    ax.set_yscale("log")
    ax.set_ylabel(r"$a$ [R$_\odot$]")

    # --- panel 4: stellar type -----------------------------------------------------
    ax = axes[3]
    ax.step(df["time"], df["stellar_type_1"], color=C1, lw=2, where="post", label="Star 1")
    ax.step(
        df["time"],
        df["stellar_type_2"],
        color=C2,
        lw=2,
        where="post",
        ls="--",
        label="Star 2",
    )
    visited = sorted(set(df["stellar_type_1"]) | set(df["stellar_type_2"]))
    ax.set_yticks(visited)
    ax.set_yticklabels([StellarType(t) for t in visited], fontsize=8)
    ax.set_ylabel("Stellar type")
    ax.set_xlabel("Time [Myr]")
    ax.legend(fontsize=8, loc="upper left")

    # mark the interaction events across every panel
    events = (
        lazy_events.select("time_final", "event_types")
        .filter(pl.col("event_types").list.contains("mt_history"))
        .collect()
    )
    for ax in axes:
        for ev in events.iter_rows():
            ax.axvline(ev[0], color="grey", lw=1, alpha=0.6, zorder=0)

    axes[0].annotate(
        "stable\nmass transfer",
        xy=(6.13, 24),
        xytext=(4.5, 14),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )
    axes[0].annotate(
        "common\nenvelope",
        xy=(7.58, 24),
        xytext=(6.9, 8),
        fontsize=9,
        ha="center",
        arrowprops=dict(arrowstyle="->", color="grey", lw=1),
    )

    plt.tight_layout()
    plt.show()

    time = df["time"][-1]
    print(f"FINAL STATE at t = {time:.2f} Myr")

    st1, m1 = StellarType(df["stellar_type_1"][-1]), df["mass_1"][-1]
    print(f"  Star 1: {st1}, {m1:.2f} Msun")

    st2, m2 = StellarType(df["stellar_type_2"][-1]), df["mass_2"][-1]
    print(f"  Star 2: {st2}, {m2:.2f} Msun")

    semimajoraxis, eccentricity = df["semimajoraxis"][-1], df["eccentricity"][-1]
    print(f"  Separation: {semimajoraxis:.2f} Rsun, eccentricity {eccentricity:.3f}")

    unbound = "NO - disrupted" if df["unbound"][-1] else "YES - still a binary"
    print(f"  Bound? {unbound}")
