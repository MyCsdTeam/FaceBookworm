from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/FaceBookWormDB"
mongo = PyMongo(app)

@app.route('/search', methods=['GET'])
def search_products():
    search_name = request.args.get('name', '')

    if search_name == '':
        query = {}
    else:
        query = {"$text": {"$search": search_name}}

    results = mongo.db.products.find(query).sort("price", -1)

    output = []
    for product in results:
        output.append({
            "id": str(product["_id"]), 
            "name": product["name"],
            "image": product["image"],
            "description": product["description"],
            "likes": product["likes"],
            "price": product["price"]
        })

    return jsonify(output)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)