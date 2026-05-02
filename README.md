# FaceBookworm 📚

The ultimate digital destination for book lovers. FaceBookworm is a Web Application that allows users to explore books, filter them by category, and add them to their "Want to Read" list.

## 🚀 Features
*   **Accent-Insensitive Search:** A smart title search that ignores Greek accents using custom Regular Expressions.
*   **Category Filtering:** Instantly display books based on genres like Romance, Fantasy, Classics, Thriller, Mystery, and Crime/Action.
*   **Popular Books:** Displays the top 5 books with the most likes on the homepage.
*   **"Want to Read" Feature:** Add or remove likes on books. The choice is saved both in the backend database and locally in the user's browser using LocalStorage.

## 🛠️ Tech Stack
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript
*   **Backend:** Python, Flask, Flask-CORS
*   **Database:** MongoDB (PyMongo)

## ⚙️ Installation and Execution (Local Development)

### 1. Prerequisites
*   [Python 3.x](https://www.python.org/) installed
*   [MongoDB Community Server](https://www.mongodb.com/try/download/community) installed and running

### 2. Backend Setup
1. Open your terminal in the project directory.
2. Install the required Python libraries:
   pip install Flask Flask-PyMongo Flask-CORS
3. Import the data into MongoDB. Make sure you create a database named `facebookworm_db` with a collection named `books`, and import the provided JSON file containing the book data.
4. Start the Flask server:
   python app.py
   *(The server will run on `http://127.0.0.1:5000`)*

### 3. Frontend Setup
Simply open the `homepage.html` file in your favorite web browser. No separate frontend server is required.

## 👥 Our Team
*   **Vitkou Maria:** Frontend Developer (HTML/CSS)
*   **Tsimerikas Alexios:** Backend Developer (Python/Flask)
*   **Nikolaou Michail:** Database Admin (MongoDB)

© 2026 FaceBookworm
