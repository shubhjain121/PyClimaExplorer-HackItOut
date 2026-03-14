import xarray as xr
import os

DATA_DIR = r"c:\Users\anujj\OneDrive\Desktop\project\data"
files = ["air.mon.mean.nc", "uwnd.mon.mean.nc", "sample_data.nc"]

for f in files:
    path = os.path.join(DATA_DIR, f)
    if os.path.exists(path):
        print(f"--- Metadata for {f} ---")
        try:
            ds = xr.open_dataset(path)
            print(f"Dimensions: {list(ds.dims)}")
            print(f"Variables: {list(ds.data_vars)}")
            if 'time' in ds.coords:
                print(f"Time range: {ds.time.values[0]} to {ds.time.values[-1]}")
                print(f"Total time steps: {len(ds.time)}")
            elif 'TIME' in ds.coords:
                print(f"Time range (TIME): {ds.TIME.values[0]} to {ds.TIME.values[-1]}")
            ds.close()
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"File not found: {f}")
    print("\n")
