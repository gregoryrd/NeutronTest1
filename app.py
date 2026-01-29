from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
NEUTRON_MASS = 1.67492749804e-27  # kg
ANGSTROM_TO_METERS = 1e-10

class NeutronConverter:
    """Convert between neutron energy, velocity, and wavelength."""
    
    @staticmethod
    def energy_to_velocity(energy_ev):
        """Convert energy (eV) to velocity (m/s)."""
        energy_joules = energy_ev * 1.602176634e-19  # Convert eV to Joules
        velocity = math.sqrt(2 * energy_joules / NEUTRON_MASS)
        return velocity
    
    @staticmethod
    def velocity_to_energy(velocity_ms):
        """Convert velocity (m/s) to energy (eV)."""
        kinetic_energy_joules = 0.5 * NEUTRON_MASS * velocity_ms ** 2
        energy_ev = kinetic_energy_joules / 1.602176634e-19
        return energy_ev
    
    @staticmethod
    def velocity_to_wavelength(velocity_ms):
        """Convert velocity (m/s) to wavelength (Angstroms)."""
        wavelength_m = PLANCK_CONSTANT / (NEUTRON_MASS * velocity_ms)
        wavelength_angstrom = wavelength_m / ANGSTROM_TO_METERS
        return wavelength_angstrom
    
    @staticmethod
    def wavelength_to_velocity(wavelength_angstrom):
        """Convert wavelength (Angstroms) to velocity (m/s)."""
        wavelength_m = wavelength_angstrom * ANGSTROM_TO_METERS
        velocity = PLANCK_CONSTANT / (NEUTRON_MASS * wavelength_m)
        return velocity
    
    @staticmethod
    def energy_to_wavelength(energy_ev):
        """Convert energy (eV) to wavelength (Angstroms)."""
        velocity = NeutronConverter.energy_to_velocity(energy_ev)
        return NeutronConverter.velocity_to_wavelength(velocity)
    
    @staticmethod
    def wavelength_to_energy(wavelength_angstrom):
        """Convert wavelength (Angstroms) to energy (eV)."""
        velocity = NeutronConverter.wavelength_to_velocity(wavelength_angstrom)
        return NeutronConverter.velocity_to_energy(velocity)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/convert/energy-to-velocity', methods=['POST'])
def energy_to_velocity():
    """Convert energy (eV) to velocity (m/s)."""
    try:
        data = request.get_json()
        energy = data.get('energy')
        
        if energy is None:
            return jsonify({'error': 'Missing energy parameter'}), 400
        
        if energy < 0:
            return jsonify({'error': 'Energy must be non-negative'}), 400
        
        velocity = NeutronConverter.energy_to_velocity(energy)
        return jsonify({
            'energy_eV': energy,
            'velocity_ms': velocity
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/velocity-to-energy', methods=['POST'])
def velocity_to_energy():
    """Convert velocity (m/s) to energy (eV)."""
    try:
        data = request.get_json()
        velocity = data.get('velocity')
        
        if velocity is None:
            return jsonify({'error': 'Missing velocity parameter'}), 400
        
        if velocity < 0:
            return jsonify({'error': 'Velocity must be non-negative'}), 400
        
        energy = NeutronConverter.velocity_to_energy(velocity)
        return jsonify({
            'velocity_ms': velocity,
            'energy_eV': energy
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/velocity-to-wavelength', methods=['POST'])
def velocity_to_wavelength():
    """Convert velocity (m/s) to wavelength (Angstroms)."""
    try:
        data = request.get_json()
        velocity = data.get('velocity')
        
        if velocity is None:
            return jsonify({'error': 'Missing velocity parameter'}), 400
        
        if velocity <= 0:
            return jsonify({'error': 'Velocity must be positive'}), 400
        
        wavelength = NeutronConverter.velocity_to_wavelength(velocity)
        return jsonify({
            'velocity_ms': velocity,
            'wavelength_angstrom': wavelength
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/wavelength-to-velocity', methods=['POST'])
def wavelength_to_velocity():
    """Convert wavelength (Angstroms) to velocity (m/s)."""
    try:
        data = request.get_json()
        wavelength = data.get('wavelength')
        
        if wavelength is None:
            return jsonify({'error': 'Missing wavelength parameter'}), 400
        
        if wavelength <= 0:
            return jsonify({'error': 'Wavelength must be positive'}), 400
        
        velocity = NeutronConverter.wavelength_to_velocity(wavelength)
        return jsonify({
            'wavelength_angstrom': wavelength,
            'velocity_ms': velocity
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/energy-to-wavelength', methods=['POST'])
def energy_to_wavelength():
    """Convert energy (eV) to wavelength (Angstroms)."""
    try:
        data = request.get_json()
        energy = data.get('energy')
        
        if energy is None:
            return jsonify({'error': 'Missing energy parameter'}), 400
        
        if energy < 0:
            return jsonify({'error': 'Energy must be non-negative'}), 400
        
        wavelength = NeutronConverter.energy_to_wavelength(energy)
        return jsonify({
            'energy_eV': energy,
            'wavelength_angstrom': wavelength
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/wavelength-to-energy', methods=['POST'])
def wavelength_to_energy():
    """Convert wavelength (Angstroms) to energy (eV)."""
    try:
        data = request.get_json()
        wavelength = data.get('wavelength')
        
        if wavelength is None:
            return jsonify({'error': 'Missing wavelength parameter'}), 400
        
        if wavelength <= 0:
            return jsonify({'error': 'Wavelength must be positive'}), 400
        
        energy = NeutronConverter.wavelength_to_energy(wavelength)
        return jsonify({
            'wavelength_angstrom': wavelength,
            'energy_eV': energy
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/full', methods=['POST'])
def full_conversion():
    """Convert any parameter to all others. Provide one of: energy, velocity, or wavelength."""
    try:
        data = request.get_json()
        energy = data.get('energy')
        velocity = data.get('velocity')
        wavelength = data.get('wavelength')
        
        # Validate that exactly one parameter is provided
        params = sum([energy is not None, velocity is not None, wavelength is not None])
        if params != 1:
            return jsonify({'error': 'Provide exactly one parameter: energy, velocity, or wavelength'}), 400
        
        result = {}
        
        if energy is not None:
            if energy < 0:
                return jsonify({'error': 'Energy must be non-negative'}), 400
            result['energy_eV'] = energy
            result['velocity_ms'] = NeutronConverter.energy_to_velocity(energy)
            result['wavelength_angstrom'] = NeutronConverter.energy_to_wavelength(energy)
        
        elif velocity is not None:
            if velocity < 0:
                return jsonify({'error': 'Velocity must be non-negative'}), 400
            result['velocity_ms'] = velocity
            result['energy_eV'] = NeutronConverter.velocity_to_energy(velocity)
            result['wavelength_angstrom'] = NeutronConverter.velocity_to_wavelength(velocity)
        
        elif wavelength is not None:
            if wavelength <= 0:
                return jsonify({'error': 'Wavelength must be positive'}), 400
            result['wavelength_angstrom'] = wavelength
            result['velocity_ms'] = NeutronConverter.wavelength_to_velocity(wavelength)
            result['energy_eV'] = NeutronConverter.wavelength_to_energy(wavelength)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
