function showTab(id) {
    document.querySelectorAll(".tab").forEach(tab =>
        tab.classList.add("hidden")
    );

    document.getElementById(id).classList.remove("hidden");
}

// Dashboard
async function loadStats() {
    const data = await fetch("/api/stats").then(r => r.json());

    document.getElementById("total-books").textContent = data.total_books ?? 0;
    document.getElementById("total-members").textContent = data.total_members ?? 0;
    document.getElementById("total-borrowed").textContent = data.total_borrowed ?? 0;
}

// Books
async function loadBooks() {
    const books = await fetch("/api/books").then(r => r.json());

    document.getElementById("book-list").innerHTML = books.map(b => `
        <tr>
            <td>${b.id}</td>
            <td>${b.title}</td>
            <td>${b.author}</td>
            <td>${b.copies}</td>
            <td><button onclick="deleteBook(${b.id})">Delete</button></td>
        </tr>
    `).join("");
}

document.getElementById("book-form").onsubmit = async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/books", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        e.target.reset();
        loadBooks();
        loadStats();
    } else {
        alert("Unable to add book");
    }
};

async function deleteBook(id) {
    if (!confirm("Delete this book?")) return;

    await fetch(`/api/books/${id}`, {method: "DELETE"});
    loadBooks();
    loadStats();
}

// Members
async function loadMembers() {
    const members = await fetch("/api/members").then(r => r.json());

    document.getElementById("member-list").innerHTML = members.map(m => `
        <tr>
            <td>${m.id}</td>
            <td>${m.name}</td>
            <td>${m.email}</td>
        </tr>
    `).join("");
}

document.getElementById("member-form").onsubmit = async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/members", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        e.target.reset();
        loadMembers();
        loadStats();
    } else {
        alert("Unable to add member");
    }
};

// Issue Book
document.getElementById("issue-form").onsubmit = async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/issue", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Book issued successfully");
        e.target.reset();
        loadBorrowings();
        loadStats();
    } else {
        alert("Unable to issue book");
    }
};

// Return Book
document.getElementById("return-form").onsubmit = async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target));

    const res = await fetch("/api/return", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Book returned successfully");
        e.target.reset();
        loadBorrowings();
        loadFines();
        loadStats();
    } else {
        alert("Unable to return book");
    }
};

// Borrowings
async function loadBorrowings() {
    const data = await fetch("/api/borrowings").then(r => r.json());

    document.getElementById("borrowing-list").innerHTML = data.map(b => `
        <tr>
            <td>${b.id}</td>
            <td>${b.book_title ?? b.book_id}</td>
            <td>${b.member_name ?? b.member_id}</td>
            <td>${b.status ?? b.returned ?? ""}</td>
        </tr>
    `).join("");
}

// Fines
async function loadFines() {
    const fines = await fetch("/api/fines").then(r => r.json());

    document.getElementById("fine-list").innerHTML = fines.map(f => `
        <tr>
            <td>${f.id}</td>
            <td>${f.member_name ?? f.member_id}</td>
            <td>${f.amount}</td>
            <td>${f.status ?? f.paid ?? ""}</td>
            <td>
                <button onclick="payFine(${f.id})">Pay</button>
            </td>
        </tr>
    `).join("");
}

async function payFine(id) {
    const res = await fetch(`/api/fines/${id}/pay`, {method: "POST"});

    if (res.ok) {
        loadFines();
    } else {
        alert("Unable to pay fine");
    }
}

// Search Books
document.getElementById("book-search").oninput = async e => {
    const text = e.target.value.toLowerCase();

    const books = await fetch("/api/books").then(r => r.json());

    const filtered = books.filter(b =>
        b.title.toLowerCase().includes(text) ||
        b.author.toLowerCase().includes(text)
    );

    document.getElementById("book-list").innerHTML = filtered.map(b => `
        <tr>
            <td>${b.id}</td>
            <td>${b.title}</td>
            <td>${b.author}</td>
            <td>${b.copies}</td>
            <td><button onclick="deleteBook(${b.id})">Delete</button></td>
        </tr>
    `).join("");
};

// Load everything
loadStats();
loadBooks();
loadMembers();
loadBorrowings();
loadFines();
