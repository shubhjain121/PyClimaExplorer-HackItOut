# data_loader.py
import xarray as xr
import os

def load_dataset(file_path: str):
    """
    Load a NetCDF dataset using Xarray.
    Tries standard loading first; falls back with decode_times=False
    for datasets with unusual time encodings (e.g. 'months since').
    """
    try:
        ds = xr.open_dataset(file_path)
    except Exception:
        ds = xr.open_dataset(file_path, decode_times=False)
    return ds

def list_variables(ds):
    """
    Return only variables that have lat+lon dimensions (plottable on a map)
    or a single time-like dimension (plottable as a time series).
    """
    plottable = []
    for v in ds.data_vars:
        dims = set(ds[v].dims)
        has_spatial = {'lat', 'lon'}.issubset(dims)
        has_time_1d = len(dims) == 1  # 1-D time series variable
        if has_spatial or has_time_1d:
            plottable.append(v)
    # Fall back: return all vars if nothing matched
    return plottable if plottable else list(ds.data_vars)

def get_time_dim(ds, variable):
    """
    Detect the name of the time dimension in this dataset/variable.
    Returns None if no time dimension is found.
    """
    dims = list(ds[variable].dims)
    for candidate in ['time', 'TIME', 'year', 'YEAR', 't']:
        if candidate in dims:
            return candidate
    return None
