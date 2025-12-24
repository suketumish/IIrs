# Quick Start Guide - IIRS Reverse Geofencing API

## 🚀 Run the Project in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

Expected output:
```
==================================================
IIRS Reverse Geofencing API
==================================================
✓ Shapefile loaded successfully!
✓ CRS: EPSG:4326
✓ Total regions: 36
✓ Columns: ['shape1', 'shapeiso', 'geometry']

🚀 Starting Flask server...
 * Running on http://0.0.0.0:5000
```

### Step 3: Test the API

**Option A: Web Browser**
1. Open: http://localhost:5000
2. Click anywhere on the map
3. See the location details instantly!

**Option B: Direct API Call**
```
http://localhost:5000/locate?lat=28.7041&lon=77.1025
```

**Option C: Using cURL**
```bash
curl "http://localhost:5000/locate?lat=28.7041&lon=77.1025"
```

**Option D: Using Python**
```python
import requests

response = requests.get(
    'http://localhost:5000/locate',
    params={'lat': 28.7041, 'lon': 77.1025}
)

print(response.json())
```

## 📍 Sample Test Coordinates

### Valid Indian Cities
```bash
# Delhi
curl "http://localhost:5000/locate?lat=28.7041&lon=77.1025"

# Mumbai
curl "http://localhost:5000/locate?lat=19.0760&lon=72.8777"

# Bangalore
curl "http://localhost:5000/locate?lat=12.9716&lon=77.5946"

# Kolkata
curl "http://localhost:5000/locate?lat=22.5726&lon=88.3639"

# Chennai
curl "http://localhost:5000/locate?lat=13.0827&lon=80.2707"
```

### Edge Cases (for testing error handling)
```bash
# Invalid latitude (out of range)
curl "http://localhost:5000/locate?lat=100&lon=77.1025"

# Invalid longitude (out of range)
curl "http://localhost:5000/locate?lat=28.7041&lon=200"

# Missing parameters
curl "http://localhost:5000/locate"

# Non-numeric values
curl "http://localhost:5000/locate?lat=abc&lon=xyz"

# Coordinates in ocean (not found)
curl "http://localhost:5000/locate?lat=10.0&lon=70.0"
```

## 🧪 Run Unit Tests

```bash
# Using pytest (recommended)
pytest tests/test_api.py -v

# Using unittest
python tests/test_api.py

# Run specific test
python -m pytest tests/test_api.py::TestReverseGeofencingAPI::test_locate_valid_coordinates -v
```

## 📡 API Endpoints

### 1. Home Page (Web UI)
```
GET /
```
Returns: Interactive web interface

### 2. API Information
```
GET /api
```
Returns: API documentation and usage info

### 3. Locate (Main Endpoint)
```
GET /locate?lat={latitude}&lon={longitude}
```

**Parameters:**
- `lat` (required): Latitude (-90 to 90)
- `lon` (required): Longitude (-180 to 180)

**Success Response (200):**
```json
{
  "status": "success",
  "coordinates": {
    "latitude": 28.7041,
    "longitude": 77.1025
  },
  "state": "Delhi",
  "shapeiso": "IN-DL"
}
```

**Not Found Response (404):**
```json
{
  "status": "not_found",
  "message": "Coordinates do not fall within any mapped region.",
  "lat": 28.7041,
  "lon": 77.1025
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "message": "Invalid or missing parameters. Provide 'lat' and 'lon' as numbers."
}
```

### 4. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "shapefile_loaded": true,
  "regions_count": 36
}
```

## 🔧 Troubleshooting

### Issue: "Shapefile not found"
**Solution:** Ensure the shapefile is in the correct location:
```
iirs-geofencing/
└── data/
    ├── india_States_level_1.shp
    ├── india_States_level_1.shx
    ├── india_States_level_1.dbf
    ├── india_States_level_1.prj
    └── india_States_level_1.cpg
```

### Issue: "Module not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Issue: "CRS mismatch"
**Solution:** The code automatically converts to EPSG:4326. If issues persist, check your shapefile's .prj file.

## 📚 Understanding the Code

### How It Works (Simple Explanation)

1. **Server Starts:**
   - Loads shapefile into memory (GeoPandas GeoDataFrame)
   - Converts to EPSG:4326 (GPS coordinate system)
   - Creates spatial index for fast queries

2. **Request Comes In:**
   - User sends: `/locate?lat=28.7041&lon=77.1025`
   - Server validates coordinates
   - Creates a Point geometry

3. **Point-in-Polygon Check:**
   - Checks which state/district polygon contains the point
   - Uses spatial indexing (R-tree) for efficiency
   - Returns the matching region

4. **Response Sent:**
   - JSON with state/district information
   - Or error message if not found

### Key Files

- **`app.py`**: Main Flask application with API endpoints
- **`utils/geo_utils.py`**: Helper functions for geospatial operations
- **`static/index.html`**: Interactive web interface
- **`tests/test_api.py`**: Unit tests for all endpoints
- **`data/`**: Shapefile directory

## 🎓 For Viva/Presentation

### Demo Script:

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Show the web interface:**
   - Open http://localhost:5000
   - Click on different locations on the map
   - Show real-time state/district detection

3. **Demonstrate API calls:**
   ```bash
   curl "http://localhost:5000/locate?lat=28.7041&lon=77.1025"
   ```

4. **Show error handling:**
   ```bash
   curl "http://localhost:5000/locate?lat=100&lon=200"
   ```

5. **Run tests:**
   ```bash
   python tests/test_api.py
   ```

6. **Explain the code:**
   - Open `app.py` and explain the Point-in-Polygon logic
   - Show the shapefile loading and CRS conversion
   - Explain the spatial query using GeoPandas

### Key Points to Mention:

- ✅ Uses industry-standard libraries (GeoPandas, Shapely)
- ✅ Proper CRS handling (EPSG:4326 for GPS)
- ✅ Efficient spatial indexing (R-tree)
- ✅ Comprehensive error handling
- ✅ RESTful API design
- ✅ Production-ready code structure
- ✅ Bonus: Interactive web UI
- ✅ Bonus: Complete test suite

---

**Ready to submit! 🎉**
