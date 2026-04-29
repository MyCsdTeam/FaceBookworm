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
# --- Βοηθητική συνάρτηση για Ελληνικούς τόνους ---
def create_accent_insensitive_regex(search_term):
    # Χάρτης αντικατάστασης γραμμάτων με ή χωρίς τόνο
    accents_map = {
        'α': '[αά]', 'ά': '[αά]',
        'ε': '[εέ]', 'έ': '[εέ]',
        'η': '[ηή]', 'ή': '[ηή]',
        'ι': '[ιίϊΐ]', 'ί': '[ιίϊΐ]', 'ϊ': '[ιίϊΐ]', 'ΐ': '[ιίϊΐ]',
        'ο': '[οό]', 'ό': '[οό]',
        'υ': '[υύϋΰ]', 'ύ': '[υύϋΰ]', 'ϋ': '[υύϋΰ]', 'ΰ': '[υύϋΰ]',
        'ω': '[ωώ]', 'ώ': '[ωώ]'
    }
    pattern = ""
    for char in search_term.lower(): # Κάνουμε τα γράμματα μικρά για να τα ταιριάξουμε στο map
        # Αν το γράμμα υπάρχει στο map, βάζουμε το regex του, αλλιώς το αφήνουμε ως έχει
        pattern += accents_map.get(char, char) 
    return pattern

# --- ENDPOINT 1: Αναζήτηση Βιβλίων ---
@app.route('/search', methods=['GET'])
def search_products():
    search_name = request.args.get('name', '')

    if search_name == '':
        query = {}
    else:
        # Φτιάχνουμε το έξυπνο pattern που αγνοεί τους τόνους
        smart_regex_pattern = create_accent_insensitive_regex(search_name)
        
        query = {
            "$or": [
                {"name": {"$regex": smart_regex_pattern, "$options": "i"}}
            ]
        }

    results = mongo.db.books.find(query).sort("price", -1)

    output = []
    for book in results:
        output.append({
            "id": str(book["_id"]), 
            "name": book["name"],
            "image": book["image"],
            "description": book["description"],
            "likes": book["likes"],
            "price": book["price"]
        })

    return jsonify(output)

# --- ENDPOINT 2: Προσθήκη / Αφαίρεση Like ---
@app.route('/like', methods=['POST'])
def add_like():
    # Διαβάζουμε το "δέμα" (body) που μας έστειλε η JS
    data = request.get_json()
    book_id = data.get('id')
    action = data.get('action') # Διαβάζει αν είναι 'like' ή 'unlike'

    # Διακόπτης: Αν είναι like βάζει +1, αν είναι unlike βάζει -1
    increment = 1 if action == 'like' else -1

    # Ενημερώνουμε τη βάση (το $inc πλέον παίρνει το +1 ή το -1)
    mongo.db.books.update_one(
        {"_id": ObjectId(book_id)}, 
        {"$inc": {"likes": increment}}      
    )
    
    return jsonify({"message": f"Η ενέργεια {action} ολοκληρώθηκε!"})

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

# --- ENDPOINT 4(ΔΙΚΟ ΜΑΣ): Φιλτράρισμα ανά Κατηγορία ---
@app.route('/category', methods=['GET'])
def get_by_category():
    # Διαβάζουμε την κατηγορία που μας έστειλε το JS (αν δεν στείλει, θεωρούμε 'all')
    category_type = request.args.get('type', 'all')

    if category_type == 'all':
        # Αν η κατηγορία είναι "all", τα φέρνουμε όλα
        results = mongo.db.books.find().sort("price", -1)
    else:
        # Αλλιώς, ψάχνουμε στη MongoDB μόνο όσα έχουν το συγκεκριμένο πεδίο "category"
        results = mongo.db.books.find({"category": category_type}).sort("price", -1)

    output = []
    for book in results:
        output.append({
            "id": str(book["_id"]), 
            "name": book["name"],
            "image": book["image"],
            "description": book["description"],
            "likes": book["likes"],
            "price": book["price"]
        })

    return jsonify(output)

# --- ENDPOINT 5: Ανάκτηση Κριτικών ενός Βιβλίου ---
@app.route('/get_reviews/<book_id>', methods=['GET'])
def get_reviews(book_id):
    # Ψάχνουμε το βιβλίο με βάση το ID του
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    
    # Αν βρεθεί το βιβλίο και έχει το πεδίο reviews, τις επιστρέφουμε
    if book and "reviews" in book:
        return jsonify(book["reviews"])
    return jsonify([]) # Αν δεν έχει, επιστρέφουμε άδεια λίστα

# --- ENDPOINT 6: Προσθήκη Νέας Κριτικής ---
@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    book_id = data.get('id')
    
    # Φτιάχνουμε το αντικείμενο της νέας κριτικής
    new_review = {
        "user": data.get('user'),
        "rating": int(data.get('rating')),
        "comment": data.get('comment')
    }
    
    # Χρησιμοποιούμε το $push για να βάλουμε τη νέα κριτική στη λίστα (array) reviews της MongoDB
    mongo.db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$push": {"reviews": new_review}}
    )
    
    return jsonify({"message": "Η κριτική προστέθηκε επιτυχώς!"})    

# 3. Εκκίνηση του Server
if __name__ == "__main__":
    # Τρέχει υποχρεωτικά στο localhost και στην πόρτα 5000 (απαίτηση εργασίας)
    app.run(host="127.0.0.1", port=5000, debug=True)