from flask import Flask, request, make_response

app = Flask(__name__)


# Healthcheck endpoint
@app.route('/v1/healthcheck', methods=['GET'])
def healthcheck():
    status_code = 400 if request.args else 200
    response = make_response('', status_code)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


# Handle unsupported endpoints and methods
@app.errorhandler(404)
@app.errorhandler(405)
def handle_unsupported(e):
    response = make_response('', 400)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
