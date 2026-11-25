function showTab(id) {
    document.querySelectorAll(".tab").forEach(tab =>
        tab.classList.add("hidden")
    );

    document.getElementById(id).classList.remove("hidden");
}


// Dashboard
async function loadStats() {
    const data = await fetch("/api/stats").then(r => r.json());

    document.getElementById("total-books").textContent = data.total_titles;
    document.getElementById("total-members").textContent = data.active_members;
    document.getElementById("total-borrowed").textContent = data.currently_issued;
    document.getElementById("available-copies").textContent = data.available_copies;
}


// Books
async function loadBooks(search = "") {
    const books = await fetch(`/api/books?search=${encodeURIComponent(search)}`)
        .then(r => r.json());

    document.getElementById("book-list").innerHTML = books.map(b => `
        <tr>
            <td>${b.book_id}</td>
            <td>${b.title}</td>
            <td>${b.author}</td>
            <td>${b.category ?? ""}</td>
            <td>${b.total_copies}</td>
            <td>${b.available_copies}</td>
            <td>
                <button class="delete-book" data-id="${b.book_id}">Delete</button>
            </td>
        </tr>
    `).join("");
}


document.getElementById("book-form").onsubmit = async function(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/books", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);

    if (res.ok) {
        e.target.reset();
        loadBooks();
        loadStats();
    }
};


document.getElementById("book-list").onclick = async function(e) {
    if (!e.target.classList.contains("delete-book")) return;

    const id = e.target.dataset.id;

    if (!confirm("Delete this book?")) return;

    const res = await fetch(`/api/books/${encodeURIComponent(id)}`, {
        method: "DELETE"
    });

    const result = await res.json();
    alert(result.message);

    loadBooks();
    loadStats();
};


// Members
async function loadMembers() {
    const members = await fetch("/api/members").then(r => r.json());

    document.getElementById("member-list").innerHTML = members.map(m => `
        <tr>
            <td>${m.member_id}</td>
            <td>${m.first_name} ${m.last_name ?? ""}</td>
            <td>${m.email}</td>
            <td>${m.membership_type}</td>
        </tr>
    `).join("");
}


document.getElementById("member-form").onsubmit = async function(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/members", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);

    if (res.ok) {
        e.target.reset();
        loadMembers();
        loadStats();
    }
};


// Issue book
document.getElementById("issue-form").onsubmit = async function(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/issue", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);

    if (res.ok) {
        e.target.reset();
        loadBorrowings();
        loadBooks();
        loadStats();
    }
};


// Return book
document.getElementById("return-form").onsubmit = async function(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/return", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);

    if (res.ok) {
        e.target.reset();
        loadBorrowings();
        loadFines();
        loadBooks();
        loadStats();
    }
};


// Borrowings
async function loadBorrowings() {
    const data = await fetch("/api/borrowings").then(r => r.json());

    document.getElementById("borrowing-list").innerHTML = data.map(b => `
        <tr>
            <td>${b.borrow_id}</td>
            <td>${b.book_title}</td>
            <td>${b.member_name}</td>
            <td>${b.borrow_date}</td>
            <td>${b.due_date}</td>
        </tr>
    `).join("");
}


// Fines
async function loadFines() {
    const fines = await fetch("/api/fines").then(r => r.json());

    document.getElementById("fine-list").innerHTML = fines.map(f => `
        <tr>
            <td>${f.fine_id}</td>
            <td>${f.member_name}</td>
            <td>${f.fine_amount}</td>
            <td>${f.payment_status}</td>
            <td>
                ${f.payment_status === "Unpaid"
                    ? `<button class="pay-fine" data-id="${f.fine_id}">Pay</button>`
                    : "Paid"}
            </td>
        </tr>
    `).join("");
}


document.getElementById("fine-list").onclick = async function(e) {
    if (!e.target.classList.contains("pay-fine")) return;

    const id = e.target.dataset.id;

    const res = await fetch(`/api/fines/${encodeURIComponent(id)}/pay`, {
        method: "POST"
    });

    const result = await res.json();
    alert(result.message);

    loadFines();
};


// Search books
document.getElementById("book-search").oninput = function(e) {
    loadBooks(e.target.value);
};


// Load data
loadStats();
loadBooks();
loadMembers();
loadBorrowings();
loadFines();
