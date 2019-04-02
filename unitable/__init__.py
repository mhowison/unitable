# Re-exported imports
import pandas as pd
from numpy import nan, where
from re import sub

# Hidden imports
import builtins as _builtins
from inspect import stack as _stack
from keyword import iskeyword as _iskeyword
from pkg_resources import get_distribution as _get_distribution
from sys import stderr as _logfile

__version__ = _get_distribution("unitable").version

# Global data frame
_df = pd.DataFrame()

# Utility functions for manipulating caller's locals

_builtins = frozenset(dir(_builtins))

def _generate(name):
    """
    Generate a new variable in the caller's locals. Test if the variable name is valid.
    """
    _locals = _stack()[2][0].f_locals
    if _iskeyword(name):
        raise ValueError("cannot name variable '{}' because it is a Python keyword".format(name))
    if name in _builtins:
        raise ValueError("cannot name variable '{}' because it is a Python builtin".format(name))
    if name in _locals:
        raise ValueError("cannot name variable '{}' because that name is already in use".format(name))
    if not name.isidentifier():
        raise ValueError("cannot name variable '{}' because it is an invalid Python variable name".format(name))
    _locals[name] = _df[name]

def _drop(name):
    """
    Drop a variable from the caller's locals.
    """
    global _df
    _locals = _stack()[2][0].f_locals
    if name in _locals and name in _df.columns:
        _locals.pop(name)
    else:
        raise ValueError("cannot drop variable '{}' because it is not currently loaded".format(name))

def _get_name(obj):
    if isinstance(obj, str) or isinstance(obj, bytes):
        return str(obj)
    elif hasattr(obj, "name"):
        return obj.name
    else:
        raise ValueError("unknown variable '{}'".format(str(obj)))

# DataFrame

def input(values):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.DataFrame(values)
    for name in _df.columns: _generate(name)
    print("inputted", len(_df.columns), "variables and", len(_df), "observations", file=_logfile)

data_frame = input

def clear():
    global _df
    unkept = _df.columns.tolist()
    _df = pd.DataFrame()
    for name in unkept: _drop(name)
    print("dropped", len(unkept), "variables", file=_logfile)

# Input/Output

def _sanitize_name(name):
    return sub(r"[^A-Za-z0-9]", "_", name)

def read_csv(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_csv(filename, **kwargs)
    _df.columns = list(map(_sanitize_name, _df.columns))
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

def read_tsv(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_csv(filename, sep="\t", **kwargs)
    _df.columns = list(map(_sanitize_name, _df.columns))
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

def read_fwf(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_fwf(filename, **kwargs)
    _df.columns = list(map(_sanitize_name, _df.columns))
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

def read_excel(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_excel(filename, **kwargs)
    _df.columns = list(map(_sanitize_name, _df.columns))
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

import_delimited = read_csv

def write_csv(filename, index=False, **kwargs):
    _df.to_csv(filename, index=index, float_format="%g", **kwargs)
    print("wrote", len(_df.columns), "variables to", filename, file=_logfile)

def write_tsv(filename, index=False, **kwargs):
    _df.to_csv(filename, index=index, float_format="%g", sep="\t", **kwargs)
    print("wrote", len(_df.columns), "variables to", filename, file=_logfile)

export_delimited = write_csv

# Column Operations

def generate(name, value):
    global _df
    _df.loc[:, name] = value
    _generate(name)

def replace(variable, value):
    global _df
    name = _get_name(variable)
    _drop(name)
    _df.loc[:, name] = value
    _generate(name)

def drop(variable):
    global _df
    name = _get_name(variable)
    _drop(name)
    del _df[name]

def rename(variable, name):
    global _df
    old_name = _get_name(variable)
    if old_name != name:
        _drop(old_name)
        _df.rename(columns={old_name: name}, inplace=True)
        _generate(name)

# Filtering

def list_if(condition):
    return _df[condition]

def keep_if(condition):
    global _df
    n = len(_df)
    for name in _df.columns: _drop(name)
    _df = _df.loc[condition, :]
    for name in _df.columns: _generate(name)
    print("kept", len(_df), "of", n, "observations", file=_logfile)

filter = keep_if

def drop_if(condition):
    global _df
    n = len(_df)
    for name in _df.columns: _drop(name)
    _df = _df.loc[~condition, :]
    for name in _df.columns: _generate(name)
    print("kept", len(_df), "of", n, "observations", file=_logfile)

def drop_duplicates(*args, **kwargs):
    global _df
    n = len(_df)
    for name in _df.columns: _drop(name)
    _df = _df.drop_duplicates(*args, **kwargs)
    for name in _df.columns: _generate(name)
    print("kept", len(_df), "of", n, "observations", file=_logfile)

def keep(*variables):
    global _df
    kept = list(map(_get_name, variables))
    kept_set = frozenset(kept)
    for name in _df.columns:
        if name not in kept_set: _drop(name)
    _df = _df[kept]
    print("kept", len(_df.columns), "variables", file=_logfile)

## Sorting by Values

def sort(*variables):
    global _df
    for name in _df.columns: _drop(name)
    _df = _df.sort_values(list(map(_get_name, variables)))
    for name in _df.columns: _generate(name)

# String Functions

## Finding Length of String

def strlen(variable):
    return variable.str.len()

## Finding Position of Substring

def strpos(variable, substr):
    return variable.str.find(substr)

## Extracting Substring by Position

def substr(variable, start, end):
    return variable.str[start:end]

## Extracting nth Word

def word(variable, n):
    return variable.str.split(" ", expand=True)[n]

## Changing Case

def strupper(variable):
    return variable.str.upper()

def strlower(variable):
    return variable.str.lower()

def strproper(variable):
    return variable.str.title()

# Merging

def merge(df, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = _df.merge(df, **kwargs)
    for name in _df.columns: _generate(name)

def append(df, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = _df.append(df, ignore_index=True, **kwargs)
    for name in _df.columns: _generate(name)

# Missing Data

def dropna(**kwargs):
    global _df
    n = len(_df)
    for name in _df.columns: _drop(name)
    _df = _df.dropna(**kwargs)
    for name in _df.columns: _generate(name)
    print("dropped", n - len(_df), "of", n, "observrations", file=_logfile)

# Aggregation

def groupby(*variables):
    return _df.groupby(list(map(_get_name, variables)))

# Dimensions

def nrow():
    return len(_df)

def ncol():
    return len(_df.columns)

def col_names():
    return _df.columns.tolist()

def col_types():
    return _df.dtypes
