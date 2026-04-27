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

    // --- ΚΩΔΙΚΑΣ ΓΙΑ ITEMS PAGE (Αλληλεπίδραση 2) ---
    const searchContainer = document.getElementById("search-container");
    if (searchContainer) {
        searchContainer.addEventListener("click", handleLikeClick);
    }
    // --- ΚΩΔΙΚΑΣ ΓΙΑ ΚΑΤΗΓΟΡΙΕΣ ---
    const categoryButtons = document.querySelectorAll(".category-btn"); 

    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                categoryButtons.forEach(btn => btn.classList.remove("active"));
                
                event.target.classList.add("active");
                
                const selectedCategory = event.target.getAttribute("data-category");
                
                fetchBooksByCategory(selectedCategory);
            });
        });
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

// ==========================================
// 4. ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΤΑ LIKES 
// ==========================================
async function handleLikeClick(event) {
    const likeBtn = event.target.closest(".like-btn");
    if (!likeBtn) return; // Αν δεν πατήθηκε το κουμπί, αγνόησέ το

    const bookId = likeBtn.getAttribute("data-id");

    // 1. Ανοίγουμε το "σημειωματάριο" του browser (LocalStorage)
    let likedBooks = JSON.parse(localStorage.getItem('likedBooks') || "[]");
    
    // Ελέγχουμε αν έχουμε ήδη κάνει like σε αυτό το βιβλίο
    const isAlreadyLiked = likedBooks.includes(bookId);
    
    // Αποφασίζουμε τι θα γράφει η ετικέτα 'action' στο δέμα μας
    const action = isAlreadyLiked ? 'unlike' : 'like';

    try {
        // 2. Στέλνουμε το δέμα (fetch) στον server
        const response = await fetch("http://127.0.0.1:5000/like", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: bookId, action: action }),
        });

        // 3. Αν ο server απαντήσει "ΟΚ", αλλάζουμε την οθόνη και τη μνήμη
        if (response.ok) {
            const likesCountSpan = likeBtn.querySelector(".likes-count");
            let currentLikes = parseInt(likesCountSpan.innerText);

            if (isAlreadyLiked) {
                // ΑΦΑΙΡΕΣΗ LIKE
                likesCountSpan.innerText = currentLikes - 1;
                likeBtn.style.color = "inherit"; // Επαναφορά χρώματος
                likedBooks = likedBooks.filter(id => id !== bookId); // Το σβήνουμε από τη μνήμη
            } else {
                // ΠΡΟΣΘΗΚΗ LIKE
                likesCountSpan.innerText = currentLikes + 1;
                likeBtn.style.color = "#e74c3c"; // Κόκκινο χρώμα
                likedBooks.push(bookId); // Το γράφουμε στη μνήμη
            }

            // Σώζουμε το ενημερωμένο σημειωματάριο πίσω στον browser
            localStorage.setItem('likedBooks', JSON.stringify(likedBooks));
            
        }
    } catch (error) {
        console.error("Σφάλμα σύνδεσης με τον server:", error);
    }
}

// ==========================================
// 5. ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΦΙΛΤΡΑΡΙΣΜΑ ΚΑΤΗΓΟΡΙΑΣ
// ==========================================
async function fetchBooksByCategory(category) {
    try {
        // Στέλνουμε το αίτημα στο Python, περνώντας την κατηγορία στο URL
        const response = await fetch(`http://127.0.0.1:5000/category?type=${category}`);
        const books = await response.json();
        
        renderSearchBooks(books); 
    } catch (error) {
        console.error("Σφάλμα στη φόρτωση κατηγορίας:", error);
    }
}
