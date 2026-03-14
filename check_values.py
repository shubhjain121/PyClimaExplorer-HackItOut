import xarray as xr
import os
import numpy as np

DATA_DIR = r"c:\Users\anujj\OneDrive\Desktop\project\data"
f = "uwnd.mon.mean.nc"
path = os.path.join(DATA_DIR, f)

ds = xr.open_dataset(path)
# Check 2026-01
try:
    data_2026 = ds['uwnd'].sel(time="2026-01-01", method="nearest")
    nan_count = np.isnan(data_2026.values).sum()
    total_count = data_2026.values.size
    print(f"uwnd 2026-01-01: NaNs={nan_count}, Total={total_count}")
    print(f"Sample values: {data_2026.values.flatten()[:10]}")
    
    # Check 2025-01 for comparison
    data_2025 = ds['uwnd'].sel(time="2025-01-01", method="nearest")
    nan_count_2025 = np.isnan(data_2025.values).sum()
    print(f"uwnd 2025-01-01: NaNs={nan_count_2025}, Total={total_count}")
except Exception as e:
    print(f"Error: {e}")

ds.close()
