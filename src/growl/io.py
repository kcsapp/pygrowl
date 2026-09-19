from functools import reduce
from typing import Iterable

import h5py
import polars as pl

from .constants import COLUMN_DATA, StateColumn, StateEnum


def load(filename: str, columns: Iterable[str] | None = None) -> pl.LazyFrame:
    """Load a BSE Detailed Output h5 file as a polars LazyFrame.

    Args:
        filename (str): Path to the h5 file to load
        columns (Iterable[str] | None): If provided, the columns to return

    Returns:
        pl.LazyFrame: A lazily-loaded polars dataframe representing the stored h5 data
    """
    with h5py.File(filename) as f:
        load_column_data = (c for c in COLUMN_DATA if c.name in f.keys())
        if columns:
            load_column_data = filter(lambda c: c.name in columns, load_column_data)

        df = pl.LazyFrame({c.colname: f[c.name][()] for c in load_column_data})

    return df


def convert(df: pl.LazyFrame, columns: Iterable[str] | None = None) -> pl.LazyFrame:
    """Convert the column datatypes of a BSE Detailed Output file.

    This method uses the standard value defined in the MeasurementContext row descriptor, which
    is generally a standard numeric type except for columns representing a descriptive category.

    Args:
        df (pl.LazyFrame): The polars dataframe to convert
        columns (Iterable[str] | None): If provided, the columns to convert

    Returns:
        pl.LazyFrame: A polars LazyFrame with the specified columns type-converted
    """
    convert_column_data = (c for c in COLUMN_DATA if c.colname in df.columns)
    if columns:
        convert_column_data = filter(
            lambda c: c.name in columns or c.colname in columns, convert_column_data
        )

    cast_columns, enum_columns = [], {}
    for c in convert_column_data:
        if isinstance(c.type, type) and issubclass(c.type, StateEnum):
            enum_columns[c.colname] = {v.state: v for v in c.type}
        else:
            cast_columns.append(pl.col(c.colname).cast(c.type))

    cdf = df.with_columns(*cast_columns)
    for name, enum_map in enum_columns.items():
        cdf = cdf.with_columns(
            pl.coalesce(
                *(
                    pl.when(pl.col(name) == state)
                    .then(pl.lit(enum.state, dtype=enum.pl_enum()))
                    .otherwise(pl.lit(None, dtype=enum.pl_enum()))
                    for state, enum in enum_map.items()
                )
            ).alias(name)
        )

    return cdf


def select_events(
    df: pl.LazyFrame,
    columns: StateColumn | Iterable[StateColumn],
    suffix: str = "_final",
) -> pl.LazyFrame:
    """Filter the dataframe to select events that change a state column.

    This can select events from multiple columns, and returns a dataframe with the
    schema doubled, storing before and after values of each column.

    Args:
        df (pl.LazyFrame): The polars dataframe to filter
        columns (Iterable[StateColumnT]): The columns to use for identifying events
        suffix (str, optional): The suffix representing the final state

    Returns:
        pl.LazyFrame: A polars dataframe representing state-changing events
    """
    if isinstance(columns, str):
        columns = [columns]

    ddf = df.with_row_index("index").join(
        df.select(pl.all().shift(-1))
        .with_row_index("index")
        .fill_nan(-1)
        .cast(df.schema, strict=False),
        how="full",
        on="index",
        suffix=suffix,
    )
    selection: pl.Expr = reduce(
        lambda i, f: i | f,
        [pl.col(name) != pl.col(name + suffix) for name in columns],
    )
    return (
        ddf.filter(selection)
        .clone()
        .with_columns(
            event_types=pl.concat_list(
                [
                    pl.when(
                        (pl.col(name) != pl.col(name + suffix))
                        & (pl.col(name) != -1)
                        & (pl.col(name + suffix) != -1)
                    )
                    .then(pl.lit(name))
                    .otherwise(pl.lit(None, dtype=pl.String))
                    for name in columns
                ]
            ).list.drop_nulls()
        )
    )
