# utils.py
import os

def get_data_directory():
    """
    Returns the project directory itself (where the .nc files live).
    Creates a 'data' sub-folder if it doesn't exist as a fallback.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return base_dir

def get_default_nc_path():
    """
    Returns the path to the sample BEST dataset included in the project.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "BEST.cvdp_data.1950-2024.nc")
