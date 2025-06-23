from flask import Flask, request, jsonify
from run import compile_code
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (for frontend integration)

@app.route('/compile', methods=['POST'])
def compile_endpoint():
    data = request.get_json()
    code = data.get('code', '')
    try:
        assembly = compile_code(code)
        return jsonify({'success': True, 'assembly': assembly})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 