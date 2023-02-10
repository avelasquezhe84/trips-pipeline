from flask import Flask, jsonify, request, Response

import json
import load_data

app = Flask(__name__)

@app.route('/api/health')
def health():
	status_code = Response(status=200)
	return status_code

@app.post('/api/load')
def load():
    content_type = request.mimetype
    if content_type == "application/json":
        body = json.loads(request.data.decode("utf8"))
        source = body["source"]
        url = body["url"]
        try:
            load_data.main(source, url)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'CSV file loading failed...',
                'error':  e
            })
        return jsonify({
            'status': 'success',
            'message': 'CSV file loaded into the database successfully.',
            'error': ""
        })
    return jsonify({
        'status': 'error',
        'message': 'Request Body is {}.'.format(content_type),
        'error': 'Request Body is not JSON.'
    })

@app.route('/api/trips', methods=['GET', 'POST'])
def trips():
    if request.method == 'GET':
        # code to handle GET requests
        pass
    elif request.method == 'POST':
        # code to handle POST requests
        pass

if __name__ == '__main__':
    app.run()
