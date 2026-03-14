import xarray as xr
import os
import numpy as np

DATA_DIR = r"c:\Users\anujj\OneDrive\Desktop\project\data"
files = {
    "air.mon.mean.nc": "air",
    "uwnd.mon.mean.nc": "uwnd",
    "sample_data.nc": "prate"
}

for f, var in files.items():
    path = os.path.join(DATA_DIR, f)
    ds = xr.open_dataset(path)
    try:
        # Check latest non-NaN month
        data = ds[var]
        # Find index of first slice that is not all NaN (from the end)
        for i in range(len(ds.time)-1, -1, -1):
            t_slice = data.isel(time=i)
            if not np.isnan(t_slice.values).all():
                print(f"{f} ({var}): Latest valid data is {ds.time.values[i]}")
                break
    except Exception as e:
        print(f"Error {f}: {e}")
    ds.close()
