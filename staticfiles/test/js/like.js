document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".like-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            
            const postId = this.getAttribute("data-id");

            fetch(`/like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {

                const heart = document.getElementById(`heart-${postId}`);
                const link = document.getElementById(`likes-link-${postId}`);
                
                // Update heart icon
                if (data.liked) {
                    heart.classList.remove("far");
                    heart.classList.add("fas", "liked");
                } else {
                    heart.classList.remove("fas", "liked");
                    heart.classList.add("far");
                }

                // Update the likes text dynamically
                if (link) {
                    if (data.count === 1) {
                        link.textContent = `${data.count} like`;   // singular
                    } else {
                        link.textContent = `${data.count} likes`;  // plural
                    }
                }

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
