"""
Geospatial Utility Functions
Helper functions for geospatial operations
"""

import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

def validate_coordinates(lat, lon):
    """
    Validate if coordinates are within valid ranges
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False, "Coordinates must be numeric values"
    
    if not (-90 <= lat <= 90):
        return False, "Latitude must be between -90 and 90"
    
    if not (-180 <= lon <= 180):
        return False, "Longitude must be between -180 and 180"
    
    return True, None

def point_in_polygon(lat, lon, gdf):
    """
    Check if a point is inside any polygon in the GeoDataFrame
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        gdf (GeoDataFrame): GeoDataFrame containing polygons
    
    Returns:
        tuple: (found, result_dict)
    """
    # Create point (lon, lat order for Shapely)
    point = Point(lon, lat)
    
    # Find containing polygon
    matches = gdf[gdf.contains(point)]
    
    if matches.empty:
        return False, None
    
    result = matches.iloc[0]
    return True, result

def get_bounding_box(gdf):
    """
    Get the bounding box of the entire GeoDataFrame
    
    Args:
        gdf (GeoDataFrame): Input GeoDataFrame
    
    Returns:
        dict: Bounding box coordinates
    """
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    
    return {
        "min_lon": bounds[0],
        "min_lat": bounds[1],
        "max_lon": bounds[2],
        "max_lat": bounds[3]
    }

def convert_crs(gdf, target_crs="EPSG:4326"):
    """
    Convert GeoDataFrame to target CRS
    
    Args:
        gdf (GeoDataFrame): Input GeoDataFrame
        target_crs (str): Target CRS (default: WGS84)
    
    Returns:
        GeoDataFrame: Converted GeoDataFrame
    """
    if gdf.crs != target_crs:
        return gdf.to_crs(target_crs)
    return gdf

def get_shapefile_info(gdf):
    """
    Get detailed information about the shapefile
    
    Args:
        gdf (GeoDataFrame): Input GeoDataFrame
    
    Returns:
        dict: Shapefile information
    """
    return {
        "crs": str(gdf.crs),
        "total_regions": len(gdf),
        "columns": list(gdf.columns),
        "geometry_type": str(gdf.geometry.type.unique()),
        "bounding_box": get_bounding_box(gdf)
    }