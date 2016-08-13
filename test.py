import os
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

genres = [
    {
        'id': 1,
        'name': u'Trash Metal',
        'bands': u'Metallica, Megadeth'
    },
    {
        'id': 2,
        'name': u'Death Metal',
        'bands': u'Dark Tranquility, Inflames'
    }
]

# Get genres
@app.route('/todo/api/v1.0/genres', methods=['GET'])
def get_genres():
    return jsonify({'genres': genres})

# 404 not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)