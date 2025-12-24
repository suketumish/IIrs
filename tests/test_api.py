"""
Unit Tests for IIRS Reverse Geofencing API
Tests all endpoints and edge cases
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import json


class TestReverseGeofencingAPI(unittest.TestCase):
    """Test cases for the Reverse Geofencing API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home/API info endpoint"""
        response = self.client.get('/api')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('author', data)
        self.assertEqual(data['author'], 'SAKET KUMAR')
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_locate_valid_coordinates(self):
        """Test locate endpoint with valid coordinates (Delhi)"""
        response = self.client.get('/locate?lat=28.7041&lon=77.1025')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('coordinates', data)
    
    def test_locate_missing_parameters(self):
        """Test locate endpoint with missing parameters"""
        response = self.client.get('/locate')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_locate_invalid_latitude(self):
        """Test locate endpoint with invalid latitude"""
        response = self.client.get('/locate?lat=100&lon=77.1025')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_locate_invalid_longitude(self):
        """Test locate endpoint with invalid longitude"""
        response = self.client.get('/locate?lat=28.7041&lon=200')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_locate_non_numeric_coordinates(self):
        """Test locate endpoint with non-numeric coordinates"""
        response = self.client.get('/locate?lat=abc&lon=xyz')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
    
    def test_locate_ocean_coordinates(self):
        """Test locate endpoint with coordinates in ocean (should not be found)"""
        # Coordinates in Indian Ocean
        response = self.client.get('/locate?lat=10.0&lon=70.0')
        
        # Should return 404 or success depending on shapefile coverage
        self.assertIn(response.status_code, [200, 404])
        
        data = json.loads(response.data)
        self.assertIn(data['status'], ['success', 'not_found'])
    
    def test_locate_multiple_cities(self):
        """Test locate endpoint with coordinates from multiple Indian cities"""
        test_cities = [
            {'name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
            {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
            {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
        ]
        
        for city in test_cities:
            response = self.client.get(f"/locate?lat={city['lat']}&lon={city['lon']}")
            self.assertIn(response.status_code, [200, 404])
            
            data = json.loads(response.data)
            self.assertIn('status', data)
    
    def test_locate_boundary_coordinates(self):
        """Test locate endpoint with coordinates at valid boundaries"""
        # Test extreme valid coordinates
        test_coords = [
            {'lat': 90, 'lon': 0},    # North Pole
            {'lat': -90, 'lon': 0},   # South Pole
            {'lat': 0, 'lon': 180},   # Date line
            {'lat': 0, 'lon': -180},  # Date line
        ]
        
        for coord in test_coords:
            response = self.client.get(f"/locate?lat={coord['lat']}&lon={coord['lon']}")
            # Should not error, but may not find location
            self.assertIn(response.status_code, [200, 404])


class TestGeoUtils(unittest.TestCase):
    """Test cases for geo utility functions"""
    
    def setUp(self):
        """Import geo_utils"""
        from utils.geo_utils import validate_coordinates
        self.validate_coordinates = validate_coordinates
    
    def test_validate_valid_coordinates(self):
        """Test validation with valid coordinates"""
        is_valid, error = self.validate_coordinates(28.7041, 77.1025)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_invalid_latitude(self):
        """Test validation with invalid latitude"""
        is_valid, error = self.validate_coordinates(100, 77.1025)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_invalid_longitude(self):
        """Test validation with invalid longitude"""
        is_valid, error = self.validate_coordinates(28.7041, 200)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_non_numeric(self):
        """Test validation with non-numeric values"""
        is_valid, error = self.validate_coordinates("abc", "xyz")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
