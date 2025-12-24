from flask import Flask, request, jsonify, send_from_directory
import geopandas as gpd
from shapely.geometry import Point
import os

app = Flask(__name__, static_folder='static')

# Global variable to store the geodataframe
gdf = None

def load_shapefile():
    """Load shapefile when server starts"""
    global gdf
    shapefile_path = 'data/india_States_level_1.shp'
    
    if not os.path.exists(shapefile_path):
        print(f"ERROR: Shapefile not found at {shapefile_path}")
        return False
    
    try:
        # Load the shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Ensure CRS is WGS84 (EPSG:4326) for lat/lon coordinates
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        print(f"✓ Shapefile loaded successfully!")
        print(f"✓ CRS: {gdf.crs}")
        print(f"✓ Total regions: {len(gdf)}")
        print(f"✓ Columns: {list(gdf.columns)}")
        return True
    
    except Exception as e:
        print(f"ERROR loading shapefile: {e}")
        return False

@app.route('/')
def home():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')

@app.route('/api')
def api_info():
    """API documentation endpoint"""
    return jsonify({
        "message": "IIRS Reverse Geofencing API",
        "author": "SAKET KUMAR",
        "track": "Track 3",
        "usage": {
            "endpoint": "/locate",
            "method": "GET",
            "parameters": {
                "lat": "Latitude (float)",
                "lon": "Longitude (float)"
            },
            "example": "/locate?lat=28.7041&lon=77.1025"
        },
        "status": "active" if gdf is not None else "shapefile not loaded"
    })

@app.route('/locate', methods=['GET'])
def locate():
    """
    Reverse Geofencing Endpoint
    Returns the state/district for given coordinates
    """
    global gdf
    
    # Check if shapefile is loaded
    if gdf is None:
        return jsonify({
            "status": "error",
            "message": "Shapefile not loaded. Server initialization failed."
        }), 500
    
    # Get latitude and longitude from query parameters
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "Invalid or missing parameters. Provide 'lat' and 'lon' as numbers."
        }), 400
    
    # Validate coordinate ranges
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return jsonify({
            "status": "error",
            "message": "Coordinates out of valid range. Lat: [-90, 90], Lon: [-180, 180]"
        }), 400
    
    try:
        # Create a Point geometry from the coordinates
        point = Point(lon, lat)  # Note: Shapely uses (lon, lat) order
        
        # Perform spatial join - find which polygon contains the point
        # This is the Point-in-Polygon operation
        matches = gdf[gdf.contains(point)]
        
        # Check if point is inside any polygon
        if matches.empty:
            # Get list of available states for better error message
            available_states = sorted(gdf['shape1'].unique().tolist()) if 'shape1' in gdf.columns else []
            
            return jsonify({
                "status": "not_found",
                "message": "Coordinates do not fall within any mapped region.",
                "lat": lat,
                "lon": lon,
                "note": f"This shapefile only contains {len(gdf)} states/regions.",
                "available_regions": available_states
            }), 404
        
        # Get the first match (should be only one)
        result = matches.iloc[0]
        
        # Build response based on available columns
        response = {
            "status": "success",
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            }
        }
        
        # Add available geographic information
        # Column names may vary in different shapefiles
        possible_names = {
            'state': ['state', 'ST_NM', 'NAME_1', 'STATE', 'State', 'shape1'],
            'district': ['district', 'DISTRICT', 'NAME_2', 'District'],
            'state_code': ['shapeiso', 'ISO', 'STATE_CODE']
        }
        
        for key, possible_cols in possible_names.items():
            for col in possible_cols:
                if col in result.index:
                    response[key] = str(result[col])
                    break
        
        # If no standard columns found, add all non-geometry columns
        if 'state' not in response:
            for col in result.index:
                if col != 'geometry':
                    response[col] = str(result[col])
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "shapefile_loaded": gdf is not None,
        "regions_count": len(gdf) if gdf is not None else 0
    }), 200

if __name__ == '__main__':
    print("=" * 50)
    print("IIRS Reverse Geofencing API")
    print("=" * 50)
    
    # Load shapefile before starting server
    if load_shapefile():
        print("\n🚀 Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n❌ Failed to start server: Shapefile loading failed")
        print("Please ensure the shapefile exists in the 'data/' directory")