<script>
// Like function - use your own variable names
function handleLike(postID) {
    const likeBtn = document.getElementById(`like-btn-${postID}`);
    const likeCount = document.getElementById(`like-count-${postID}`);
    const heartIcon = document.getElementById(`heart-${postID}`);
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Disable button during request
    likeBtn.disabled = true;
    
    // Send AJAX request
    fetch(`/ajax/like/${postID}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update like count
            likeCount.textContent = data.like_count;
            
            // Update heart color
            if (data.liked) {
                heartIcon.style.fill = '#ff0000';
                heartIcon.style.stroke = '#ff0000';
            } else {
                heartIcon.style.fill = 'var(--text-dark)';
                heartIcon.style.stroke = 'var(--text-dark)';
            }
            
            // Update button text if needed
            const likeText = document.getElementById(`like-text-${postID}`);
            if (likeText) {
                if (data.liked) {
                    likeText.innerHTML = `Liked by <a href="#">You</a> and <a href="#">${data.other_likers_count} others</a>`;
                } else {
                    likeText.innerHTML = `Liked by <a href="#">${data.like_count} others</a>`;
                }
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        likeBtn.disabled = false;
    });
}
</script>