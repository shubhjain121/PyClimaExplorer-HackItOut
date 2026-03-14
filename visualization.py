# visualization.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_spatial_map(ds, variable, time_value=None):
    """
    Create a smooth global scatter-geo heatmap for a spatial variable.
    Works with variables that have (lat, lon) dimensions.
    """
    var_data = ds[variable]

    # Slice by time if the variable has a time-like dimension
    for t_dim in ['time', 'TIME', 'year', 'YEAR']:
        if t_dim in var_data.dims and time_value is not None:
            var_data = var_data.sel({t_dim: time_value}, method='nearest')
            break

    # If variable still has more than 2 dims after slicing, take the first slice
    while len(var_data.dims) > 2:
        var_data = var_data.isel({var_data.dims[0]: 0})

    if 'lat' not in var_data.dims or 'lon' not in var_data.dims:
        raise ValueError(
            f"Variable '{variable}' does not have lat/lon dimensions. "
            f"Dims found: {list(var_data.dims)}"
        )

    df = var_data.to_dataframe().reset_index().dropna(subset=[variable])

    fig = px.scatter_geo(
        df,
        lat='lat',
        lon='lon',
        color=variable,
        color_continuous_scale='RdBu_r',
        projection='natural earth',
        title=f"{variable}",
        labels={variable: 'Value'},
        hover_data={'lat': ':.1f', 'lon': ':.1f', variable: ':.3f'}
    )
    fig.update_traces(marker=dict(size=10, opacity=1.0))
    fig.update_layout(
        height=480,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='#faf9f6',
        font=dict(color='#2c2c2c'),
        geo=dict(
            bgcolor='#faf9f6',
            showocean=True, oceancolor='#c9dff0',
            showland=True,  landcolor='#e6ddd0',
            showcoastlines=True, coastlinecolor='#7a6a56',
            showframe=False,
            projection_type='orthographic'
        )
    )
    return fig


def plot_time_series(ds, variable, lat, lon):
    """
    Create a time-series line plot for a single lat/lon location.
    Handles both standard 'time' and integer-year 'TIME' dimensions.
    """
    var = ds[variable]

    # Must have lat + lon to select a point
    if 'lat' not in var.dims or 'lon' not in var.dims:
        raise ValueError(
            f"Variable '{variable}' has no lat/lon dims — "
            "cannot extract a location time series."
        )

    point = var.sel(lat=lat, lon=lon, method='nearest')

    # Detect the time dimension
    time_dim = None
    for td in ['time', 'TIME', 'year', 'YEAR']:
        if td in point.dims:
            time_dim = td
            break

    if time_dim is None:
        raise ValueError(
            f"No time dimension found in variable '{variable}'. "
            f"Dims: {list(point.dims)}"
        )

    df = point.to_dataframe().reset_index()
    fig = px.line(
        df, x=time_dim, y=variable,
        title=f"{variable} at ({lat:.1f}°, {lon:.1f}°)",
        labels={time_dim: 'Year', variable: 'Value'},
        markers=True
    )
    fig.update_traces(line_color='#c0392b', marker=dict(size=4))
    fig.update_layout(
        height=380,
        paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
        font=dict(family='Georgia', color='#000000'),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0')
    )
    return fig
