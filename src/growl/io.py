from functools import reduce
from typing import Iterable

import h5py
import pandas as pd

from .constants import COLUMN_DATA, StateColumn, StateEnum


def load(filename: str, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Load a BSE Detailed Output h5 file as a pandas dataframe.

    Args:
        filename (str): Path to the h5 file to load
        columns (Iterable[str] | None): If provided, the columns to return

    Returns:
        pd.DataFrame: A pandas dataframe representing the stored h5 data
    """
    with h5py.File(filename) as f:
        load_column_data = (c for c in COLUMN_DATA if c.name in f.keys())
        if columns:
            load_column_data = filter(lambda c: c.name in columns, load_column_data)

        df = pd.DataFrame({c.colname: f[c.name][()] for c in load_column_data})  # type: ignore

    return df


def convert(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Convert the column datatypes of a BSE Detailed Output file.

    This method uses the standard value defined in the MeasurementContext row descriptor, which
    is generally a standard numeric type except for columns representing a descriptive category.

    Args:
        df (pd.DataFrame): The pandas dataframe to convert
        columns (Iterable[str] | None): If provided, the columns to convert

    Returns:
        pd.DataFrame: A pandas dataframe with the specified columns type-converted
    """
    convert_column_data = (c for c in COLUMN_DATA if c.colname in df.columns)
    if columns:
        convert_column_data = filter(
            lambda c: c.name in columns or c.colname in columns, convert_column_data
        )

    astype_columns, enum_columns = {}, {}
    for c in convert_column_data:
        if issubclass(c.type, StateEnum):
            enum_columns[c.colname] = {v.state: v for v in c.type}
        else:
            astype_columns[c.colname] = c.type

    cdf = df.astype({c.colname: c.type for c in convert_column_data})
    for name, enum_map in enum_columns.items():
        cdf[name] = cdf[name].map(enum_map)

    return cdf


def select_events(
    df: pd.DataFrame,
    columns: StateColumn | Iterable[StateColumn],
    lsuffix: str = "_i",
    rsuffix: str = "_f",
) -> pd.DataFrame:
    """Filter the dataframe to select events that change a state column.

    This can select events from multiple columns, and returns a dataframe with the
    schema doubled, storing before and after values of each column.

    Args:
        df (pd.DataFrame): The pandas dataframe to filter
        columns (Iterable[StateColumnT]): The columns to use for identifying events
        lsuffix (str, optional): The suffix representing the state before the event
        lsuffix (str, optional): The suffix representing the state after the event

    Returns:
        pd.DataFrame: A pandas dataframe representing state-changing events
    """
    if isinstance(columns, str):
        columns = [columns]
    ddf = df.join(
        df.shift(-1).fillna(-1).astype(df.dtypes, errors="ignore"),
        how="outer",
        lsuffix=lsuffix,
        rsuffix=rsuffix,
    )
    selection: pd.Series[bool] = reduce(
        lambda i, f: i | f,
        [ddf[name + lsuffix] != ddf[name + rsuffix] for name in columns],
    )
    return (
        ddf[selection]
        .copy()
        .assign(
            event_types=lambda x: x.apply(
                lambda y: (
                    [
                        name
                        for name in columns
                        if y[name + lsuffix] != y[name + rsuffix]
                        and all((y[name + suff] != -1 for suff in (lsuffix, rsuffix)))
                    ]
                ),
                axis=1,
            )
        )
    )
