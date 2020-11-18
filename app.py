from flask import Flask, request, json, Response
from list import get_wishlists
import json
app = Flask(__name__)


@app.route('/<int:wishlist_id>')
def hello_world(wishlist_id):
    adults = request.args.get('adults', '2')
    check_in = request.args.get('check_in', '2021-05-10')
    check_out = request.args.get('check_out', '2021-05-12')
    data = get_wishlists(wishlist_id, check_in, check_out, adults)
    json_string = json.dumps(data, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response
