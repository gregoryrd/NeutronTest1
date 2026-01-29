import unittest
import json
from app import app, NeutronConverter
import math


class TestNeutronConverter(unittest.TestCase):
    """Unit tests for the NeutronConverter class."""
    
    def test_energy_to_velocity(self):
        """Test energy to velocity conversion."""
        energy = 25  # meV (thermal neutron)
        velocity = NeutronConverter.energy_to_velocity(energy)
        self.assertAlmostEqual(velocity, 2186.967, places=1)
    
    def test_velocity_to_energy(self):
        """Test velocity to energy conversion."""
        velocity = 2187.928  # m/s
        energy = NeutronConverter.velocity_to_energy(velocity)
        self.assertAlmostEqual(energy, 25, places=1)
    
    def test_velocity_to_wavelength(self):
        """Test velocity to wavelength conversion."""
        velocity = 2187.928  # m/s
        wavelength = NeutronConverter.velocity_to_wavelength(velocity)
        self.assertAlmostEqual(wavelength, 1.8064, places=2)
    
    def test_wavelength_to_velocity(self):
        """Test wavelength to velocity conversion."""
        wavelength = 1.8064  # Angstroms
        velocity = NeutronConverter.wavelength_to_velocity(wavelength)
        self.assertAlmostEqual(velocity, 2190.010, places=1)
    
    def test_energy_to_wavelength(self):
        """Test energy to wavelength conversion."""
        energy = 25  # meV
        wavelength = NeutronConverter.energy_to_wavelength(energy)
        self.assertAlmostEqual(wavelength, 1.8064, places=2)
    
    def test_wavelength_to_energy(self):
        """Test wavelength to energy conversion."""
        wavelength = 1.8064  # Angstroms
        energy = NeutronConverter.wavelength_to_energy(wavelength)
        self.assertAlmostEqual(energy, 25.07, places=1)
    
    def test_round_trip_energy(self):
        """Test round-trip conversion starting with energy."""
        original_energy = 100  # meV
        velocity = NeutronConverter.energy_to_velocity(original_energy)
        recovered_energy = NeutronConverter.velocity_to_energy(velocity)
        self.assertAlmostEqual(original_energy, recovered_energy, places=5)
    
    def test_round_trip_velocity(self):
        """Test round-trip conversion starting with velocity."""
        original_velocity = 5000  # m/s
        wavelength = NeutronConverter.velocity_to_wavelength(original_velocity)
        recovered_velocity = NeutronConverter.wavelength_to_velocity(wavelength)
        self.assertAlmostEqual(original_velocity, recovered_velocity, places=5)


class TestFlaskAPI(unittest.TestCase):
    """Unit tests for the Flask API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_energy_to_velocity_endpoint(self):
        """Test energy to velocity endpoint."""
        response = self.client.post(
            '/convert/energy-to-velocity',
            data=json.dumps({'energy': 25}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['energy_meV'], 25)
        self.assertAlmostEqual(data['velocity_ms'], 2186.967, places=1)
    
    def test_velocity_to_energy_endpoint(self):
        """Test velocity to energy endpoint."""
        response = self.client.post(
            '/convert/velocity-to-energy',
            data=json.dumps({'velocity': 2187.928}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['velocity_ms'], 2187.928)
        self.assertAlmostEqual(data['energy_meV'], 25, places=1)
    
    def test_full_conversion_energy(self):
        """Test full conversion endpoint with energy."""
        response = self.client.post(
            '/convert/full',
            data=json.dumps({'energy': 25}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['energy_meV'], 25)
        self.assertIn('velocity_ms', data)
        self.assertIn('wavelength_angstrom', data)
    
    def test_full_conversion_velocity(self):
        """Test full conversion endpoint with velocity."""
        response = self.client.post(
            '/convert/full',
            data=json.dumps({'velocity': 2187.928}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['velocity_ms'], 2187.928)
        self.assertIn('energy_meV', data)
        self.assertIn('wavelength_angstrom', data)
    
    def test_full_conversion_wavelength(self):
        """Test full conversion endpoint with wavelength."""
        response = self.client.post(
            '/convert/full',
            data=json.dumps({'wavelength': 1.8064}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(data['wavelength_angstrom'], 1.8064, places=4)
        self.assertIn('energy_meV', data)
        self.assertIn('velocity_ms', data)
    
    def test_missing_parameter(self):
        """Test endpoint with missing parameter."""
        response = self.client.post(
            '/convert/energy-to-velocity',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_negative_energy(self):
        """Test endpoint with negative energy."""
        response = self.client.post(
            '/convert/energy-to-velocity',
            data=json.dumps({'energy': -0.1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_negative_velocity(self):
        """Test endpoint with negative velocity."""
        response = self.client.post(
            '/convert/velocity-to-energy',
            data=json.dumps({'velocity': -100}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_multiple_parameters_full(self):
        """Test full endpoint with multiple parameters."""
        response = self.client.post(
            '/convert/full',
            data=json.dumps({'energy': 0.025, 'velocity': 2187.928}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_not_found(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
