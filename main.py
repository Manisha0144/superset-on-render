from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    data = request.json
    result = subprocess.run(
        ['python3', 'superset_fetcher.py',
         data['base_url'], data['username'],
         data['password'], str(data['chart_id'])],
        capture_output=True, text=True
    )
    return jsonify({
        "status": "success",
        "output": result.stdout,
        "error": result.stderr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
