// chat.js - Simple version
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const imageInput = document.getElementById('imageInput');
    const chatMessages = document.getElementById('chatMessages');
    
    // Auto scroll to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Scroll on load
    setTimeout(scrollToBottom, 100);
    
    // Handle image upload
    imageInput.addEventListener('change', function() {
        if (this.files[0]) {
            // Submit form immediately when image is selected
            chatForm.submit();
        }
    });
    
    // Handle text message form submission
    chatForm.addEventListener('submit', function(e) {
        const text = messageInput.value.trim();
        
        if (!text && !imageInput.files[0]) {
            e.preventDefault();
            return;
        }
        
        // If there's text, let the form submit normally
        // The page will reload with the new message
    });
    
    // Auto-focus input
    messageInput.focus();
});