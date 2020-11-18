from flask import Flask, request, json, Response
from list import get_wishlists, get_total
import json
app = Flask(__name__)


@app.route('/<int:wishlist_id>')
def wishlist(wishlist_id):
    adults = request.args.get('adults', '')
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    total = request.args.get('total', None)
    data = get_wishlists(wishlist_id, check_in, check_out, adults, total)
    json_string = json.dumps(data, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response


@app.route('/total/<int:item_id>')
def total_item(item_id):
    adults = request.args.get('adults', '')
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    data = get_total(item_id, check_in, check_out, adults)
    json_string = json.dumps(data, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response
