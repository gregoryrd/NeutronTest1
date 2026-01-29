from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
NEUTRON_MASS = 1.67492749804e-27  # kg
ANGSTROM_TO_METERS = 1e-10

class NeutronConverter:
    """Convert between neutron energy, velocity, and wavelength."""
    
    @staticmethod
    def energy_to_velocity(energy_mev):
        """Convert energy (meV) to velocity (m/s)."""
        energy_joules = energy_mev * 1.602176634e-22  # Convert meV to Joules (1e-3 eV)
        velocity = math.sqrt(2 * energy_joules / NEUTRON_MASS)
        return velocity
    
    @staticmethod
    def velocity_to_energy(velocity_ms):
        """Convert velocity (m/s) to energy (meV)."""
        kinetic_energy_joules = 0.5 * NEUTRON_MASS * velocity_ms ** 2
        energy_mev = kinetic_energy_joules / 1.602176634e-22  # Convert Joules to meV
        return energy_mev
    
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
    def energy_to_wavelength(energy_mev):
        """Convert energy (meV) to wavelength (Angstroms)."""
        velocity = NeutronConverter.energy_to_velocity(energy_mev)
        return NeutronConverter.velocity_to_wavelength(velocity)
    
    @staticmethod
    def wavelength_to_energy(wavelength_angstrom):
        """Convert wavelength (Angstroms) to energy (meV)."""
        velocity = NeutronConverter.wavelength_to_velocity(wavelength_angstrom)
        return NeutronConverter.velocity_to_energy(velocity)


# HTML Dashboard Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neutron Converter</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        .input-group input {
            flex: 1;
        }
        .input-group select {
            flex: 0.4;
        }
        button {
            width: 100%;
            padding: 13px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        button:active {
            transform: translateY(0);
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .results.show {
            display: block;
        }
        .result-item {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        .result-item:last-child {
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }
        .result-label {
            color: #666;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .result-value {
            color: #333;
            font-size: 20px;
            font-weight: 700;
            margin-top: 5px;
            font-family: 'Courier New', monospace;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            display: none;
            border-left: 4px solid #c33;
        }
        .error.show {
            display: block;
        }
        .info {
            background: #f0f4ff;
            color: #667eea;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 25px;
            font-size: 13px;
            line-height: 1.6;
            border-left: 4px solid #667eea;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚛️ Neutron Converter</h1>
        <p class="subtitle">Convert between energy, velocity, and wavelength</p>
        
        <div class="info">
            Enter a value in any field and click Convert. Results will show all three properties.
        </div>
        
        <form id="converterForm">
            <div class="form-group">
                <label for="energy">Energy</label>
                <div class="input-group">
                    <input type="number" id="energy" placeholder="e.g., 25" step="any">
                    <select disabled>
                        <option>meV</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="velocity">Velocity</label>
                <div class="input-group">
                    <input type="number" id="velocity" placeholder="e.g., 2187.9" step="any">
                    <select disabled>
                        <option>m/s</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label for="wavelength">Wavelength</label>
                <div class="input-group">
                    <input type="number" id="wavelength" placeholder="e.g., 1.8064" step="any">
                    <select disabled>
                        <option>Å</option>
                    </select>
                </div>
            </div>
            
            <button type="submit">Convert</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <div class="result-item">
                <div class="result-label">Energy</div>
                <div class="result-value"><span id="resultEnergy">-</span> meV</div>
            </div>
            <div class="result-item">
                <div class="result-label">Velocity</div>
                <div class="result-value"><span id="resultVelocity">-</span> m/s</div>
            </div>
            <div class="result-item">
                <div class="result-label">Wavelength</div>
                <div class="result-value"><span id="resultWavelength">-</span> Å</div>
            </div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('converterForm');
        const energyInput = document.getElementById('energy');
        const velocityInput = document.getElementById('velocity');
        const wavelengthInput = document.getElementById('wavelength');
        const resultsDiv = document.getElementById('results');
        const errorDiv = document.getElementById('error');
        const loading = document.getElementById('loading');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await convert();
        });
        
        // Clear other inputs when one is focused
        energyInput.addEventListener('input', () => {
            velocityInput.value = '';
            wavelengthInput.value = '';
        });
        velocityInput.addEventListener('input', () => {
            energyInput.value = '';
            wavelengthInput.value = '';
        });
        wavelengthInput.addEventListener('input', () => {
            energyInput.value = '';
            velocityInput.value = '';
        });
        
        async function convert() {
            const energy = energyInput.value;
            const velocity = velocityInput.value;
            const wavelength = wavelengthInput.value;
            
            if (!energy && !velocity && !wavelength) {
                showError('Please enter a value');
                return;
            }
            
            loading.style.display = 'block';
            errorDiv.classList.remove('show');
            resultsDiv.classList.remove('show');
            
            try {
                const endpoint = energy ? '/convert/full' : 
                                velocity ? '/convert/full' : '/convert/full';
                
                const payload = energy ? {energy: parseFloat(energy)} :
                               velocity ? {velocity: parseFloat(velocity)} :
                               {wavelength: parseFloat(wavelength)};
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                
                if (!response.ok) {
                    const data = await response.json();
                    showError(data.error || 'Conversion failed');
                    return;
                }
                
                const data = await response.json();
                displayResults(data);
            } catch (err) {
                showError('Network error: ' + err.message);
            } finally {
                loading.style.display = 'none';
            }
        }
        
        function displayResults(data) {
            document.getElementById('resultEnergy').textContent = 
                data.energy_eV.toFixed(6);
            document.getElementById('resultVelocity').textContent = 
                data.velocity_ms.toFixed(2);
            document.getElementById('resultWavelength').textContent = 
                data.wavelength_angstrom.toFixed(6);
            resultsDiv.classList.add('show');
        }
        
        function showError(message) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }
    </script>
</body>
</html>
'''


@app.route('/', methods=['GET'])
def dashboard():
    """Serve the web dashboard."""
    return render_template_string(DASHBOARD_HTML)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/convert/energy-to-velocity', methods=['POST'])
def energy_to_velocity():
    """Convert energy (meV) to velocity (m/s)."""
    try:
        data = request.get_json()
        energy = data.get('energy')
        
        if energy is None:
            return jsonify({'error': 'Missing energy parameter'}), 400
        
        if energy < 0:
            return jsonify({'error': 'Energy must be non-negative'}), 400
        
        velocity = NeutronConverter.energy_to_velocity(energy)
        return jsonify({
            'energy_meV': energy,
            'velocity_ms': velocity
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/velocity-to-energy', methods=['POST'])
def velocity_to_energy():
    """Convert velocity (m/s) to energy (meV)."""
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
            'energy_meV': energy
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
    """Convert energy (meV) to wavelength (Angstroms)."""
    try:
        data = request.get_json()
        energy = data.get('energy')
        
        if energy is None:
            return jsonify({'error': 'Missing energy parameter'}), 400
        
        if energy < 0:
            return jsonify({'error': 'Energy must be non-negative'}), 400
        
        wavelength = NeutronConverter.energy_to_wavelength(energy)
        return jsonify({
            'energy_meV': energy,
            'wavelength_angstrom': wavelength
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/wavelength-to-energy', methods=['POST'])
def wavelength_to_energy():
    """Convert wavelength (Angstroms) to energy (meV)."""
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
            'energy_meV': energy
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
            result['energy_meV'] = energy
            result['velocity_ms'] = NeutronConverter.energy_to_velocity(energy)
            result['wavelength_angstrom'] = NeutronConverter.energy_to_wavelength(energy)
        
        elif velocity is not None:
            if velocity < 0:
                return jsonify({'error': 'Velocity must be non-negative'}), 400
            result['velocity_ms'] = velocity
            result['energy_meV'] = NeutronConverter.velocity_to_energy(velocity)
            result['wavelength_angstrom'] = NeutronConverter.velocity_to_wavelength(velocity)
        
        elif wavelength is not None:
            if wavelength <= 0:
                return jsonify({'error': 'Wavelength must be positive'}), 400
            result['wavelength_angstrom'] = wavelength
            result['velocity_ms'] = NeutronConverter.wavelength_to_velocity(wavelength)
            result['energy_meV'] = NeutronConverter.wavelength_to_energy(wavelength)
        
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
