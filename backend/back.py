from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()  # Get the JSON data from the request
    if data is None:
        return jsonify({'error': 'No data provided'}), 400

    con_values = data.get('conValues', [])
    pro_values = data.get('proValues', [])
    
    # Process your values here (e.g., save to database or perform calculations)
    print('Contribute Values:', con_values)
    print('Profit Values:', pro_values)

    rootes = solveIRR(con_values,pro_values)

    return jsonify({'message': 'Data received successfully!','answer':rootes}), 200

def solveIRR(cons, pros):
    coeffs = []
    for i in range(len(cons)):
        coeffs.append(pros[i]-cons[i])
    coeffs = coeffs[::-1]
    n = len(coeffs)-1
    matrex = np.zeros((n,n))
    matrex[0,-1] = -coeffs[0]/coeffs[-1]
    for i in range(1,n):
        matrex[i,i-1] = 1
        matrex[i,-1] = -coeffs[i]/coeffs[-1]
    roots = np.linalg.eigvals(matrex)
    positive_real_roots = [root.real for root in roots if root.imag == 0 and root.real > 0]
    print(positive_real_roots)
    return positive_real_roots

if __name__ == '__main__':
    app.run(debug=True)