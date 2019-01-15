# Re-exported imports
import pandas as pd
from numpy import nan

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
        del _df[name]
    else:
        raise ValueError("cannot drop variable '{}' because it is not currently loaded".format(name))

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

def read_csv(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_csv(filename, **kwargs)
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

def read_tsv(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_csv(filename, sep="\t", **kwargs)
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

def read_fwf(filename, **kwargs):
    global _df
    for name in _df.columns: _drop(name)
    _df = pd.read_fwf(filename, **kwargs)
    for name in _df.columns: _generate(name)
    print("read", len(_df.columns), "variables from", filename, file=_logfile)

import_delimited = read_csv

def write_csv(filename, index=False, **kwargs):
    _df.to_csv(filename, **kwargs)
    print("wrote", len(_df.columns), "variables to", filename, file=_logfile)

def write_tsv(filename, index=False, **kwargs):
    _df.to_csv(filename, delimiter="\t", **kwargs)
    print("wrote", len(_df.columns), "variables to", filename, file=_logfile)

export_delimited = write_csv

# Column Operations

def generate(name, value):
    global _df
    _df.loc[:, name] = value
    _generate(name)

def replace(variable, value):
    global _df
    _df.loc[:, variable.name] = value

def drop(variable):
    global _df
    _drop(variable.name)

def rename(variable, name):
    global _df
    if not variable.name == name:
        _df[name, :] = variable
        _drop(variable.name)
        _generate(name)

# Filtering

def list_if(condition):
    return _df[condition]

def keep(*variables):
    global _df
    kept = [variable.name for variable in variables]
    unkept = [name for name in _df.columns if name not in frozenset(kept)]
    _df = _df[kept]
    for name in unkept: _drop(name)
    print("kept", len(_df.columns), "variables", file=_logfile)

## Sorting by Values

def sort(*variables):
    global _df
    for name in _df.columns: _drop(name)
    _df = _df.sort_values([variable.name for variable in variables])
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
    return _df.groupby([variable.name for variable in variables])

# Dimensions

def nrow():
    return len(_df)

def ncol():
    return len(_df.columns)

def col_names():
    return _df.columns.tolist()

def col_types():
    return _df.dtypes
