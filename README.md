# IIRS Internship Assessment - Track 3
## Reverse Geofencing API for Logistics

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14-orange.svg)
![License](https://img.shields.io/badge/License-Academic-red.svg)

**Submitted By:** SAKET KUMAR  
**Track:** Track 3 - Reverse Geofencing  
**Technology Stack:** Python, Flask, GeoPandas, Shapely  
**Date:** December 24, 2025

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Research & Theory](#research--theory)
3. [Technical Architecture](#technical-architecture)
4. [Installation & Setup](#installation--setup)
5. [API Documentation](#api-documentation)
6. [Testing the API](#testing-the-api)
7. [Project Structure](#project-structure)

---

## 🎯 Project Overview

This project implements a **Reverse Geofencing API** that determines the administrative zone (State/District) for any given GPS coordinates. This is critical for automated logistics companies that process millions of GPS pings to track their fleet across different administrative boundaries.

**Use Case:**  
A logistics company has trucks across India. When a truck sends its GPS coordinates (28.7041°N, 77.1025°E), the API instantly tells them the truck is in "Delhi, Central Delhi District" - enabling zone-based routing, regulatory compliance, and operational efficiency.

---

## 📚 Research & Theory

### 1. What is a Shapefile (.shp)?

A **Shapefile** is a geospatial vector data format developed by ESRI for storing geometric location and associated attribute information. It's the industry standard for representing geographic features.

**Components of a Shapefile:**
- `.shp` - Main file storing geometry (points, lines, polygons)
- `.shx` - Shape index file for quick spatial queries
- `.dbf` - Attribute data in dBASE format (state names, population, etc.)
- `.prj` - Projection information (Coordinate Reference System)

**Why Shapefiles?**
- Universal compatibility across GIS software
- Efficient storage of vector geometries
- Supports complex polygons (state/district boundaries)
- Contains both spatial and attribute data

**In This Project:**  
We use a shapefile containing polygon geometries of Indian states/districts. Each polygon represents a geographic boundary with attributes like state name, district name, etc.

---

### 2. Coordinate Reference System (CRS)

A **Coordinate Reference System (CRS)** defines how geographic coordinates relate to real locations on Earth's surface.

**Why CRS is Critical:**

1. **Earth is Not Flat:** The Earth is a 3D ellipsoid, but maps are 2D. CRS defines how to project 3D coordinates onto a 2D plane.

2. **Different Reference Points:** Different CRS use different reference ellipsoids and datums (reference points). Using mismatched CRS can cause errors of several hundred meters.

3. **Unit Consistency:** Some CRS use degrees (lat/lon), others use meters (projected coordinates).

**Common CRS:**
- **EPSG:4326 (WGS84):** Global standard, uses latitude/longitude in degrees. Used by GPS devices.
- **EPSG:3857 (Web Mercator):** Used by Google Maps, OpenStreetMap
- **EPSG:32643 (UTM Zone 43N):** Used for India, coordinates in meters

**In This Project:**  
We ensure all data uses **EPSG:4326 (WGS84)** because:
- GPS coordinates from trucks are in WGS84
- Consistent CRS prevents spatial mismatch errors
- Industry standard for global applications

**Code Implementation:**
```python
# Check and convert CRS
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
```

---

### 3. Spatial Join & Point-in-Polygon Logic

#### What is a Spatial Join?

A **Spatial Join** combines data from two spatial datasets based on their geometric relationship rather than common attribute fields.

**Types of Spatial Relationships:**
- Contains/Within
- Intersects
- Touches
- Crosses
- Overlaps

#### Point-in-Polygon (PIP) Algorithm

**Problem:** Given a point P and a polygon, determine if P lies inside the polygon.

**Common Algorithms:**

1. **Ray Casting Algorithm:**
   - Draw a horizontal ray from the point to infinity
   - Count how many times the ray crosses polygon edges
   - Odd count = inside, Even count = outside

2. **Winding Number Algorithm:**
   - Calculate the winding number (how many times polygon winds around the point)
   - Non-zero = inside, Zero = outside

**Computational Complexity:**  
O(n) where n is the number of polygon vertices

**In This Project:**

We use GeoPandas' optimized `contains()` method which:
1. Creates a **spatial index (R-tree)** for fast lookup
2. Uses efficient PIP algorithms under the hood
3. Handles edge cases (points on boundaries)

**Code Flow:**
```python
# 1. Create Point geometry
point = Point(longitude, latitude)  # Note: lon, lat order

# 2. Spatial query - find containing polygon
matches = gdf[gdf.contains(point)]

# 3. Return result
if not matches.empty:
    state = matches.iloc[0]['state_name']
```

**Why This is Efficient:**
- Spatial indexing reduces search space
- No need to check all polygons
- Typically O(log n) with spatial index

---

## 🏗️ Technical Architecture

### System Design

```
┌─────────────┐
│  GPS Device │ (Truck/Fleet)
└──────┬──────┘
       │ HTTP GET Request
       │ /locate?lat=28.7041&lon=77.1025
       ▼
┌──────────────────────────┐
│   Flask API Server       │
│  ┌────────────────────┐  │
│  │ 1. Validate Input  │  │
│  │ 2. Create Point    │  │
│  │ 3. Spatial Query   │  │
│  │ 4. Return Result   │  │
│  └────────────────────┘  │
└──────────┬───────────────┘
           │ Queries
           ▼
    ┌──────────────┐
    │ GeoPandas    │
    │ GeoDataFrame │ (Loaded in memory)
    │ ┌──────────┐ │
    │ │Shapefile │ │
    │ │  Data    │ │
    │ └──────────┘ │
    └──────────────┘
           │
           ▼
    ┌─────────────────┐
    │  JSON Response  │
    │ {               │
    │   state: "UP"   │
    │   district: "..." │
    │ }               │
    └─────────────────┘
```

### Technology Choices

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Backend Framework | Flask | Lightweight, perfect for APIs, easy to deploy |
| Spatial Operations | GeoPandas | Built on Pandas, optimized for geospatial data |
| Geometry Handling | Shapely | Industry standard for geometric operations |
| Data Format | Shapefile | Universal GIS format, widely available |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/iirs-geofencing.git
cd iirs-geofencing
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Shapefile

**Option 1 - Indian States (Recommended):**
1. Visit: https://www.igismap.com/download-india-boundary-shapefile/
2. Download "Indian States" shapefile
3. Extract the files
4. Create a `data/` folder in project root
5. Copy all shapefile components (.shp, .shx, .dbf, .prj) to `data/`
6. Rename main file to `indian_states.shp`

**Option 2 - Natural Earth Data:**
```bash
# Using Python
python -c "import geopandas as gpd; world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')); india = world[world.name == 'India']; india.to_file('data/indian_states.shp')"
```

### Step 5: Run the Server

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
✓ Columns: ['state', 'geometry']

🚀 Starting Flask server...
 * Running on http://0.0.0.0:5000
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Home - API Information
```http
GET /
```

**Response:**
```json
{
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
  "status": "active"
}
```

#### 2. Locate - Reverse Geofencing
```http
GET /locate?lat={latitude}&lon={longitude}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lat | float | Yes | Latitude (-90 to 90) |
| lon | float | Yes | Longitude (-180 to 180) |

**Success Response (200):**
```json
{
  "status": "success",
  "coordinates": {
    "latitude": 28.7041,
    "longitude": 77.1025
  },
  "state": "Delhi",
  "district": "Central Delhi"
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

#### 3. Health Check
```http
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

---

## 🧪 Testing the API

### Using Browser
```
http://localhost:5000/locate?lat=28.7041&lon=77.1025
```

### Using cURL
```bash
# Test Delhi
curl "http://localhost:5000/locate?lat=28.7041&lon=77.1025"

# Test Mumbai
curl "http://localhost:5000/locate?lat=19.0760&lon=72.8777"

# Test invalid coordinates
curl "http://localhost:5000/locate?lat=100&lon=200"
```

### Using Python
```python
import requests

response = requests.get(
    'http://localhost:5000/locate',
    params={'lat': 28.7041, 'lon': 77.1025}
)

print(response.json())
```

### Sample Test Coordinates

| Location | Latitude | Longitude | Expected State |
|----------|----------|-----------|----------------|
| Delhi | 28.7041 | 77.1025 | Delhi |
| Mumbai | 19.0760 | 72.8777 | Maharashtra |
| Bangalore | 12.9716 | 77.5946 | Karnataka |
| Kolkata | 22.5726 | 88.3639 | West Bengal |
| Chennai | 13.0827 | 80.2707 | Tamil Nadu |

---

## 📁 Project Structure

```
iirs-geofencing/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── data/                       # Shapefile directory
│   ├── indian_states.shp       # Main shapefile
│   ├── indian_states.shx       # Shape index
│   ├── indian_states.dbf       # Attribute data
│   └── indian_states.prj       # Projection info
│
├── utils/                      # Utility modules
│   └── geo_utils.py           # Geospatial helper functions
│
└── tests/                      # Test cases (optional)
    └── test_api.py            # API tests
```

---

## 🎓 Learning Outcomes

Through this project, you will understand:

1. **Geospatial Data Processing:**
   - Working with shapefiles
   - Coordinate system transformations
   - Spatial indexing and queries

2. **API Development:**
   - RESTful API design
   - Input validation
   - Error handling
   - JSON responses

3. **Real-world Applications:**
   - Fleet tracking systems
   - Location-based services
   - Administrative zone detection
   - Logistics optimization

---

## 🚀 Future Enhancements

1. **Performance Optimization:**
   - Add caching for frequent queries
   - Implement spatial indexing
   - Database integration for large datasets

2. **Feature Additions:**
   - Batch processing endpoint
   - Distance to boundary calculation
   - Multiple coordinate format support (DMS, UTM)
   - Historical location tracking

3. **Production Readiness:**
   - Authentication & API keys
   - Rate limiting
   - Docker containerization
   - Load balancing

---

## 📝 References

1. GeoPandas Documentation: https://geopandas.org/
2. Shapely Documentation: https://shapely.readthedocs.io/
3. Flask Documentation: https://flask.palletsprojects.com/
4. Coordinate Reference Systems: https://epsg.io/
5. Point-in-Polygon Algorithms: https://en.wikipedia.org/wiki/Point_in_polygon

---

## 👤 Author

**SAKET KUMAR**  
IIRS Internship Assessment - Track 3  
Email: computer.science@dsvv.ac.in

---

## 📄 License

This project is submitted as part of IIRS Internship Assessment and follows academic integrity guidelines.