// ==========================================
// 1. Ο "ΦΥΛΑΚΑΣ" (Ακούει πότε φορτώνει η σελίδα)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    
    // --- ΚΩΔΙΚΑΣ ΓΙΑ HOMEPAGE (Αλληλεπίδραση 3) ---
    const popularContainer = document.getElementById("popularBooksContainer");
    if (popularContainer) {
        loadPopularBooks(); 
    }

    // --- ΚΩΔΙΚΑΣ ΓΙΑ ITEMS PAGE (Αλληλεπίδραση 1) ---
    const searchBtn = document.getElementById("searchBtn");
    if (searchBtn) {
        searchBtn.addEventListener("click", performSearch);
        performSearch(); // Φορτώνουμε όλα τα βιβλία με το που ανοίγει η σελίδα
    }
});


// ==========================================
// 2. ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΤΗΝ ΑΡΧΙΚΗ (ΔΗΜΟΦΙΛΗ)
// ==========================================
async function loadPopularBooks() {
    try {
        const response = await fetch("http://127.0.0.1:5000/popular");
        const books = await response.json();
        renderPopularBooks(books);
    } catch (error) {
        console.error("Σφάλμα κατά τη φόρτωση των δημοφιλών:", error);
    }
}

function renderPopularBooks(books) {
    const container = document.getElementById("popularBooksContainer");
    container.innerHTML = ""; 

    books.forEach(book => {
        const bookCard = `
            <div class="book-card">
                <img src="${book.image}" alt="Εξώφυλλο Βιβλίου">
                <h3>${book.name}</h3>
                <div class="likes">❤️ ${book.likes} Likes</div>
            </div>
        `;
        container.innerHTML += bookCard;
    });
}


// ==========================================
// 3. ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΤΗΝ ΑΝΑΖΗΤΗΣΗ
// ==========================================
async function performSearch(event) {
    if (event) {
        event.preventDefault(); 
    }

    // ΠΡΟΣΑΡΜΟΓΗ: Διαβάζουμε το input μέσω της κλάσης ".search-bar"
    const searchInput = document.querySelector(".search-bar").value;

    try {
        const response = await fetch(`http://127.0.0.1:5000/search?name=${searchInput}`);
        const books = await response.json();
        renderSearchBooks(books);
    } catch (error) {
        console.error("Σφάλμα στην αναζήτηση:", error);
    }
}

function renderSearchBooks(books) {
    // ΠΡΟΣΑΡΜΟΓΗ: Το κουτί που θα μπουν τα βιβλία είναι το "search-container"
    const grid = document.getElementById("search-container");
    grid.innerHTML = ""; 

    if (books.length === 0) {
        grid.innerHTML = "<p>Δεν βρέθηκαν βιβλία με αυτόν τον τίτλο.</p>";
        return;
    }

    books.forEach(book => {
        const bookCard = `
            <div class="book-card">
                <img src="${book.image}" alt="Εξώφυλλο">
                <h3>${book.name}</h3>
                <div class="metadata">Τιμή: ${book.price}€</div>
                <p class="description">${book.description}</p>
                <div class="card-footer">
                    <div class="action-buttons">
                        <button type="button" class="like-btn" data-id="${book.id}">
                            ❤️ <span class="likes-count">${book.likes}</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
        grid.innerHTML += bookCard;
    });
}