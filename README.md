# Neutron Converter API

[![CI](https://github.com/gregoryrd/NeutronTest1/actions/workflows/ci.yml/badge.svg)](https://github.com/gregoryrd/NeutronTest1/actions/workflows/ci.yml)

A RESTful Flask web application for converting between neutron energy, velocity, and wavelength.

## Features

- 🎨 **Interactive Web Dashboard** - Beautiful, responsive UI for easy conversions
- Convert between neutron energy (meV), velocity (m/s), and wavelength (Angstroms)
- Six dedicated conversion endpoints for pairwise conversions
- One comprehensive endpoint that converts to all three properties from any input
- Input validation and error handling
- Based on neutron physics using Planck's constant and neutron mass

## Physics Formulas

The conversions are based on:
- **De Broglie wavelength**: λ = h / (m·v)
- **Kinetic energy**: E = ½·m·v²

Where:
- h = Planck's constant (6.62607015×10⁻³⁴ J·s)
- m = neutron mass (1.67492749804×10⁻²⁷ kg)
- v = velocity (m/s)
- λ = wavelength (Angstroms)
- E = energy (eV)

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python app.py
   ```

The server will start at `http://localhost:5000`

## Quick Start

### Web Dashboard
Simply open your browser to `http://localhost:5000/` to access the interactive dashboard. Enter any value and click "Convert" to see all three properties.

### API Endpoints

### Health Check
- **GET** `/health`
  - Returns: `{"status": "healthy"}`

### Pairwise Conversions

1. **POST** `/convert/energy-to-velocity`
   - Input: `{"energy": 25}`
   - Returns: `{"energy_meV": 25, "velocity_ms": 2187.928...}`

2. **POST** `/convert/velocity-to-energy`
   - Input: `{"velocity": 2187.928}`
   - Returns: `{"velocity_ms": 2187.928, "energy_meV": 25}`

3. **POST** `/convert/velocity-to-wavelength`
   - Input: `{"velocity": 2187.928}`
   - Returns: `{"velocity_ms": 2187.928, "wavelength_angstrom": 1.8064...}`

4. **POST** `/convert/wavelength-to-velocity`
   - Input: `{"wavelength": 1.8064}`
   - Returns: `{"wavelength_angstrom": 1.8064, "velocity_ms": 2187.928...}`

5. **POST** `/convert/energy-to-wavelength`
   - Input: `{"energy": 25}`
   - Returns: `{"energy_meV": 25, "wavelength_angstrom": 1.8064...}`

6. **POST** `/convert/wavelength-to-energy`
   - Input: `{"wavelength": 1.8064}`
   - Returns: `{"wavelength_angstrom": 1.8064, "energy_eV": 0.025}`

### Full Conversion (All Three Properties)

- **POST** `/convert/full`
  - Input (any one): `{"energy": 25}` or `{"velocity": 2187.928}` or `{"wavelength": 1.8064}`
  - Returns all three:
    ```json
    {
      "energy_meV": 25,
      "velocity_ms": 2187.928,
      "wavelength_angstrom": 1.8064
    }
    ```

## Example Usage

Using `curl`:

```bash
# Convert energy to all properties
curl -X POST http://localhost:5000/convert/full \
  -H "Content-Type: application/json" \
  -d '{"energy": 25}'

# Convert wavelength to velocity
curl -X POST http://localhost:5000/convert/wavelength-to-velocity \
  -H "Content-Type: application/json" \
  -d '{"wavelength": 1.8064}'
```

Using Python `requests`:

```python
import requests

response = requests.post(
    'http://localhost:5000/convert/full',
    json={'energy': 25}
)
)
print(response.json())
```

## Error Handling

The API returns appropriate HTTP status codes:
- **200**: Successful conversion
- **400**: Invalid input (missing parameter, negative energy/velocity, etc.)
- **404**: Endpoint not found
- **405**: Method not allowed
- **500**: Server error

Error responses include a descriptive error message:
```json
{"error": "Energy must be non-negative"}
```
