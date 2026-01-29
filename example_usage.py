#!/usr/bin/env python
"""
Example script demonstrating the neutron converter API.
"""

import requests
import json

# Base URL of the Flask app
BASE_URL = 'http://localhost:5000'

def print_response(title, response):
    """Pretty print a response."""
    print(f"\n{title}")
    print("-" * 50)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error {response.status_code}: {response.json()}")

# Example 1: Convert thermal neutron energy to velocity and wavelength
print("=" * 50)
print("Neutron Converter API Examples")
print("=" * 50)

# Energy conversion
response = requests.post(
    f'{BASE_URL}/convert/full',
    json={'energy': 0.025}  # 25 meV (thermal neutron)
)
print_response("Example 1: Convert 0.025 eV (thermal neutron)", response)

# High energy neutron
response = requests.post(
    f'{BASE_URL}/convert/full',
    json={'energy': 1.0}  # 1 eV
)
print_response("Example 2: Convert 1.0 eV (faster neutron)", response)

# Wavelength conversion
response = requests.post(
    f'{BASE_URL}/convert/full',
    json={'wavelength': 1.8}  # 1.8 Angstroms
)
print_response("Example 3: Convert 1.8 Angstrom wavelength", response)

# Velocity conversion
response = requests.post(
    f'{BASE_URL}/convert/full',
    json={'velocity': 2000}  # 2000 m/s
)
print_response("Example 4: Convert 2000 m/s velocity", response)

# Pairwise conversion
response = requests.post(
    f'{BASE_URL}/convert/energy-to-wavelength',
    json={'energy': 0.1}
)
print_response("Example 5: Convert 0.1 eV to wavelength", response)

print("\n" + "=" * 50)
print("Examples completed!")
print("=" * 50)
