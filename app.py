from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId # Απαραίτητο για την αναζήτηση με βάση το μοναδικό ID
import numpy as np

# 1. Αρχικοποίηση Εφαρμογής & CORS
app = Flask(__name__)
# Το CORS επιτρέπει στο Frontend (HTML/JS) να κάνει αιτήματα στο Backend χωρίς να μπλοκάρεται
CORS(app)

# 2. Σύνδεση με τη Βάση Δεδομένων
# Ορίζουμε το τοπικό URI και το όνομα της βάσης (facebookworm_db)
app.config["MONGO_URI"] = "mongodb://localhost:27017/facebookworm_db"
mongo = PyMongo(app)

# --- ENDPOINT 1: Αναζήτηση Βιβλίων ---
@app.route('/search', methods=['GET'])
def search_products():
    # Διαβάζουμε την παράμετρο 'name' από το URL (π.χ. /search?name=Harry)
    search_name = request.args.get('name', '')

    # Αν η αναζήτηση είναι κενή φέρνουμε όλα τα βιβλία, αλλιώς χρησιμοποιούμε τον Text Index
    if search_name == '':
        query = {}
    else:
        query = {"$text": {"$search": search_name}}

    # Αναζήτηση και ταξινόμηση με βάση την τιμή (φθίνουσα σειρά: -1)
    results = mongo.db.books.find(query).sort("price", -1)

    # Μετατρέπουμε τα αποτελέσματα της βάσης σε λίστα για να σταλούν ως JSON
    output = []
    for book in results:
        output.append({
            "id": str(book["_id"]), # Το _id γίνεται string για να διαβάζεται από τη JavaScript
            "name": book["name"],
            "image": book["image"],
            "description": book["description"],
            "likes": book["likes"],
            "price": book["price"]
        })

    return jsonify(output)

# --- ENDPOINT 2: Προσθήκη Like ---
@app.route('/like', methods=['POST'])
def add_like():
    # Διαβάζουμε το JSON πακέτο που στάλθηκε στο body του request
    data = request.get_json()
    book_id = data.get('id')

    # Ενημερώνουμε το συγκεκριμένο βιβλίο αυξάνοντας τα likes κατά 1 ($inc)
    mongo.db.books.update_one(
        {"_id": ObjectId(book_id)}, 
        {"$inc": {"likes": 1}}      
    )
    
    return jsonify({"message": "Το like προστέθηκε επιτυχώς!"})

# --- ENDPOINT 3: Δημοφιλή Βιβλία ---
@app.route('/popular', methods=['GET'])
def get_popular():
    # Φέρνουμε όλα τα βιβλία, ταξινομημένα βάσει likes (φθίνουσα) και κρατάμε μόνο τα 5 πρώτα
    popular_books = mongo.db.books.find().sort("likes", -1).limit(5)

    output = []
    for book in popular_books:
        output.append({
            "id": str(book["_id"]),
            "name": book["name"],
            "image": book["image"],
            "description": book["description"],
            "likes": book["likes"],
            "price": book["price"]
        })
    
    return jsonify(output)

# 3. Εκκίνηση του Server
if __name__ == "__main__":
    # Τρέχει υποχρεωτικά στο localhost και στην πόρτα 5000 (απαίτηση εργασίας)
    app.run(host="127.0.0.1", port=5000, debug=True)