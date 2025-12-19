document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".follow-btn.following").forEach(btn => {
        btn.addEventListener("click", function() {
            const userId = this.getAttribute("data-id");
            const button = this; // current button

            fetch(`/follow/${userId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                // Update button text dynamically
                button.textContent = data.after_status;
            })
            .catch(err => console.log("Error:", err));
        });
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = c.substring(name.length + 1);
            break;
        }
    }
    return cookieValue;
}
