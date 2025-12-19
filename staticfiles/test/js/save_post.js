document.addEventListener("DOMContentLoaded", () => {
    
    document.querySelectorAll(".save-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            
            const postId = this.getAttribute("data-id");

            fetch(`/save-post/${postId}/`, {  // With trailing slash
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                const saveIcon = document.getElementById(`save-icon-${postId}`);
                
                if (data.saved) {
                    saveIcon.classList.remove("far");
                    saveIcon.classList.add("fas");
                } else {
                    saveIcon.classList.remove("fas");
                    saveIcon.classList.add("far");
                }
            })
            .catch(err => console.log("Error:", err));
        });
    });

});

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