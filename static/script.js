// Tab Switching Logic
function switchTab(tabName) {
    document.querySelectorAll(".tab-pane").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".nav-pill").forEach(el => el.classList.remove("active"));

    const targetTab = document.getElementById(`tab-${tabName}`);
    if (targetTab) {
        targetTab.classList.add("active");
    }

    // Highlight active pill
    const pills = document.querySelectorAll(".nav-pill");
    pills.forEach(pill => {
        if (pill.getAttribute("onclick") && pill.getAttribute("onclick").includes(tabName)) {
            pill.classList.add("active");
        }
    });

    // Refresh content for active tab
    if (tabName === "dashboard") loadDashboard();
    if (tabName === "books") loadBooks();
    if (tabName === "members") loadMembers();
    if (tabName === "circulation") {
        loadCirculation();
        loadFines();
    }
}

// Global Alert Notification Toast
function showAlert(message, type = "success") {
    const alertBox = document.getElementById("alertBox");
    alertBox.textContent = message;
    alertBox.className = `alert-box alert-${type}`;
    alertBox.style.display = "block";

    setTimeout(() => {
        alertBox.style.display = "none";
    }, 4500);
}

// ---------------- 1. Dashboard ----------------

async function loadDashboard() {
    try {
        const res = await fetch("/api/stats");
        const stats = await res.json();

        document.getElementById("statTotalTitles").textContent = stats.total_titles;
        document.getElementById("statAvailableCopies").textContent = stats.available_copies;
        document.getElementById("statActiveMembers").textContent = stats.active_members;
        document.getElementById("statCurrentlyIssued").textContent = stats.currently_issued;
        document.getElementById("statUnpaidFines").textContent = `$${stats.unpaid_fines.toFixed(2)}`;

        // Dynamic Hero Badge Synchronization
        const badgeSub = document.getElementById("heroBadgeSub");
        if (badgeSub) {
            badgeSub.textContent = `${stats.total_titles} TITLES • ${stats.total_copies} COPIES IN CATALOG`;
        }

        // Active loans preview
        const borrowRes = await fetch("/api/borrowings");
        const loans = await borrowRes.json();
        const tbody = document.querySelector("#dashboardIssuedTable tbody");
        tbody.innerHTML = "";

        if (loans.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:1.5rem; color:#877b9f; font-weight:600;">All books are on shelves. No active loans right now.</td></tr>`;
        } else {
            loans.forEach(loan => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${loan.borrow_id}</strong></td>
                    <td><strong>${loan.book_title}</strong></td>
                    <td>${loan.member_name}</td>
                    <td>${loan.borrow_date}</td>
                    <td><span class="badge-pill badge-due">${loan.due_date}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.error("Dashboard load error:", err);
    }
}

// ---------------- 2. Books ----------------

let searchTimer = null;
function handleBookSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
        const query = document.getElementById("bookSearchInput").value;
        loadBooks(query);
    }, 250);
}

async function loadBooks(search = "") {
    try {
        const url = search ? `/api/books?search=${encodeURIComponent(search)}` : "/api/books";
        const res = await fetch(url);
        const books = await res.json();

        const tbody = document.querySelector("#booksTable tbody");
        tbody.innerHTML = "";

        if (books.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:1.5rem; color:#877b9f;">No books found matching your search.</td></tr>`;
            return;
        }

        books.forEach(b => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${b.book_id}</strong></td>
                <td><strong>${b.title}</strong></td>
                <td>${b.author}</td>
                <td><span class="badge-pill badge-category">${b.category}</span></td>
                <td>${b.total_copies}</td>
                <td>
                    <span class="badge-pill ${b.available_copies > 0 ? 'badge-in-stock' : 'badge-no-stock'}">
                        ${b.available_copies} Left
                    </span>
                </td>
                <td>$${Number(b.price).toFixed(2)}</td>
                <td>
                    <button class="pop-btn btn-danger btn-sm" onclick="handleDeleteBook('${b.book_id}')">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Books load error:", err);
    }
}

async function handleAddBook(e) {
    e.preventDefault();
    const payload = {
        book_id: document.getElementById("b_id").value,
        title: document.getElementById("b_title").value,
        author: document.getElementById("b_author").value,
        category: document.getElementById("b_category").value,
        isbn: document.getElementById("b_isbn").value,
        publication_year: document.getElementById("b_year").value,
        total_copies: document.getElementById("b_copies").value,
        price: document.getElementById("b_price").value
    };

    try {
        const res = await fetch("/api/books", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.ok) {
            showAlert(result.message, "success");
            document.getElementById("addBookForm").reset();
            loadBooks();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Server connection error.", "error");
    }
}

async function handleDeleteBook(bookId) {
    if (!confirm(`Are you sure you want to delete book ${bookId}?`)) return;

    try {
        const res = await fetch(`/api/books/${bookId}`, { method: "DELETE" });
        const result = await res.json();
        if (res.ok) {
            showAlert(result.message, "success");
            loadBooks();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Failed to delete book.", "error");
    }
}

// ---------------- 3. Members ----------------

async function loadMembers() {
    try {
        const res = await fetch("/api/members");
        const members = await res.json();

        const tbody = document.querySelector("#membersTable tbody");
        tbody.innerHTML = "";

        members.forEach(m => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${m.member_id}</strong></td>
                <td><strong>${m.first_name} ${m.last_name}</strong></td>
                <td><span class="badge-pill badge-category">${m.membership_type}</span></td>
                <td>${m.email}</td>
                <td>${m.phone || '-'}</td>
                <td>${m.registration_date}</td>
                <td><span class="badge-pill badge-in-stock">${m.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Members load error:", err);
    }
}

async function handleAddMember(e) {
    e.preventDefault();
    const payload = {
        member_id: document.getElementById("m_id").value,
        first_name: document.getElementById("m_fname").value,
        last_name: document.getElementById("m_lname").value,
        membership_type: document.getElementById("m_type").value,
        email: document.getElementById("m_email").value,
        phone: document.getElementById("m_phone").value
    };

    try {
        const res = await fetch("/api/members", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.ok) {
            showAlert(result.message, "success");
            document.getElementById("addMemberForm").reset();
            loadMembers();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Server connection error.", "error");
    }
}

// ---------------- 4. Circulation ----------------

async function loadCirculation() {
    try {
        const today = new Date();
        const dueDate = new Date();
        dueDate.setDate(today.getDate() + 14);

        const issueDueDateEl = document.getElementById("issueDueDate");
        // Expanded date range: today up to 365 days (1 full year)
        issueDueDateEl.min = today.toISOString().split("T")[0];
        issueDueDateEl.max = new Date(Date.now() + 365 * 86400000).toISOString().split("T")[0];
        issueDueDateEl.value = dueDate.toISOString().split("T")[0];

        const returnActualDateEl = document.getElementById("returnActualDate");
        returnActualDateEl.min = "2020-01-01";
        returnActualDateEl.max = "2030-12-31";
        returnActualDateEl.value = today.toISOString().split("T")[0];

        // Populate Members
        const mRes = await fetch("/api/members");
        const members = await mRes.json();
        const memberSelect = document.getElementById("issueMemberSelect");
        memberSelect.innerHTML = members.map(m => `
            <option value="${m.member_id}">${m.member_id} - ${m.first_name} ${m.last_name} (${m.membership_type})</option>
        `).join("");

        // Populate Books
        const bRes = await fetch("/api/books");
        const books = await bRes.json();
        const inStock = books.filter(b => b.available_copies > 0);
        const bookSelect = document.getElementById("issueBookSelect");

        if (inStock.length === 0) {
            bookSelect.innerHTML = `<option disabled selected>No books currently in stock</option>`;
        } else {
            bookSelect.innerHTML = inStock.map(b => `
                <option value="${b.book_id}">${b.book_id} - ${b.title} (Stock: ${b.available_copies})</option>
            `).join("");
        }

        // Populate Active Loans & Return Select
        const loansRes = await fetch("/api/borrowings");
        const loans = await loansRes.json();

        const returnSelect = document.getElementById("returnBorrowSelect");
        const activeTable = document.querySelector("#activeBorrowingTable tbody");
        activeTable.innerHTML = "";

        if (loans.length === 0) {
            returnSelect.innerHTML = `<option disabled selected>No books currently out</option>`;
            activeTable.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:1.5rem; color:#877b9f;">All books are on shelves.</td></tr>`;
            updateReturnFinePreview();
        } else {
            returnSelect.innerHTML = loans.map(l => `
                <option value="${l.borrow_id}" data-due="${l.due_date}" data-borrow="${l.borrow_date}" data-title="${l.book_title}">
                    ${l.borrow_id} - ${l.book_title} (Due: ${l.due_date} | Patron: ${l.member_name})
                </option>
            `).join("");

            loans.forEach(l => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${l.borrow_id}</strong></td>
                    <td><strong>${l.book_title}</strong></td>
                    <td>${l.member_name}</td>
                    <td>${l.borrow_date}</td>
                    <td><span class="badge-pill badge-due">${l.due_date}</span></td>
                    <td><span class="badge-pill badge-category">Issued</span></td>
                `;
                activeTable.appendChild(tr);
            });

            // Automatically trigger live penalty calculation preview
            updateReturnFinePreview();
        }

        // Keep integrated fines table synced
        loadFines();
    } catch (err) {
        console.error("Circulation load error:", err);
    }
}

// Real-Time Overdue Days & Fine Auto-Calculation Engine
function updateReturnFinePreview() {
    const select = document.getElementById("returnBorrowSelect");
    const previewBox = document.getElementById("returnFinePreviewBox");
    if (!select || select.options.length === 0 || !select.value || select.value === "No books currently out") {
        if (previewBox) previewBox.style.display = "none";
        return;
    }
    if (previewBox) previewBox.style.display = "block";

    const selectedOpt = select.options[select.selectedIndex];
    if (!selectedOpt) return;

    const dueDateStr = selectedOpt.getAttribute("data-due");
    const returnDateStr = document.getElementById("returnActualDate").value;
    const rate = parseFloat(document.getElementById("returnFineRate").value) || 2.0;

    const previewDueDate = document.getElementById("previewDueDate");
    if (previewDueDate) previewDueDate.textContent = dueDateStr || "N/A";

    if (!dueDateStr || !returnDateStr) return;

    const dueDate = new Date(dueDateStr + "T00:00:00");
    const returnDate = new Date(returnDateStr + "T00:00:00");

    const diffMs = returnDate - dueDate;
    const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

    const badge = document.getElementById("previewDaysLateBadge");
    const daysText = document.getElementById("previewOverdueDays");
    const fineText = document.getElementById("previewFineAmount");

    if (diffDays > 0) {
        const fine = (diffDays * rate).toFixed(2);
        if (badge) {
            badge.textContent = `OVERDUE (${diffDays} DAYS)`;
            badge.className = "badge-pill badge-due";
        }
        if (daysText) {
            daysText.innerHTML = `<span style="color:#e02424; font-weight:800;">${diffDays} Day(s) Late</span>`;
        }
        if (fineText) {
            fineText.textContent = `$${fine}`;
            fineText.style.color = "#e02424";
        }
    } else {
        if (badge) {
            badge.textContent = "ON TIME";
            badge.className = "badge-pill badge-in-stock";
        }
        if (daysText) {
            daysText.innerHTML = `<span style="color:#059669; font-weight:700;">0 Days (On Schedule)</span>`;
        }
        if (fineText) {
            fineText.textContent = "$0.00";
            fineText.style.color = "#059669";
        }
    }
}

async function handleIssueBook(e) {
    e.preventDefault();
    const payload = {
        member_id: document.getElementById("issueMemberSelect").value,
        book_id: document.getElementById("issueBookSelect").value,
        due_date: document.getElementById("issueDueDate").value
    };

    try {
        const res = await fetch("/api/issue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.ok) {
            showAlert(result.message, "success");
            loadCirculation();
            loadFines();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Failed to issue book.", "error");
    }
}

async function handleReturnBook(e) {
    e.preventDefault();
    const payload = {
        borrow_id: document.getElementById("returnBorrowSelect").value,
        return_date: document.getElementById("returnActualDate").value,
        daily_fine: document.getElementById("returnFineRate").value
    };

    try {
        const res = await fetch("/api/return", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();

        if (res.ok) {
            showAlert(result.message, "success");
            loadCirculation();
            loadFines();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Failed to process return.", "error");
    }
}

// ---------------- 5. Fines ----------------

async function loadFines() {
    try {
        const res = await fetch("/api/fines");
        const fines = await res.json();

        const tbody = document.querySelector("#finesTable tbody");
        tbody.innerHTML = "";

        if (fines.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:1.75rem; color:#877b9f; font-weight:700;">No penalty records. All patron accounts are clean and in good standing!</td></tr>`;
            return;
        }

        fines.forEach(f => {
            const isUnpaid = f.payment_status === "Unpaid";
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${f.fine_id}</strong></td>
                <td>${f.borrow_id}</td>
                <td><strong>${f.member_name}</strong></td>
                <td><strong style="color:${isUnpaid ? '#e11d48' : '#166534'}">$${Number(f.fine_amount).toFixed(2)}</strong></td>
                <td>${f.fine_date}</td>
                <td>
                    <span class="badge-pill ${isUnpaid ? 'badge-unpaid' : 'badge-paid'}">
                        ${f.payment_status}
                    </span>
                </td>
                <td>${f.payment_date || '-'}</td>
                <td>
                    ${isUnpaid ? `<button class="pop-btn btn-green btn-sm" onclick="handlePayFine('${f.fine_id}')">Pay Fine</button>` : `<span style="color:#059669; font-weight:700;">Settled</span>`}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Fines load error:", err);
    }
}

async function handlePayFine(fineId) {
    try {
        const res = await fetch(`/api/fines/${fineId}/pay`, { method: "POST" });
        const result = await res.json();
        if (res.ok) {
            showAlert(result.message, "success");
            loadFines();
            loadDashboard();
        } else {
            showAlert(result.message, "error");
        }
    } catch (err) {
        showAlert("Failed to settle fine.", "error");
    }
}

// ---------------- Theme Management (Light / Dark) ----------------

function initTheme() {
    const saved = localStorage.getItem("lbrary_theme") || "light";
    applyTheme(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    applyTheme(next);
}

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("lbrary_theme", theme);

    const textEl = document.getElementById("themeToggleText");
    const iconEl = document.getElementById("themeToggleIcon");

    if (theme === "dark") {
        if (textEl) textEl.textContent = "LIGHT MODE";
        if (iconEl) {
            iconEl.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"/>
                    <line x1="12" y1="1" x2="12" y2="3"/>
                    <line x1="12" y1="21" x2="12" y2="23"/>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                    <line x1="1" y1="12" x2="3" y2="12"/>
                    <line x1="21" y1="12" x2="23" y2="12"/>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
            `;
        }
    } else {
        if (textEl) textEl.textContent = "DARK MODE";
        if (iconEl) {
            iconEl.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
            `;
        }
    }
}

// Initial Launch
document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    loadDashboard();
});
