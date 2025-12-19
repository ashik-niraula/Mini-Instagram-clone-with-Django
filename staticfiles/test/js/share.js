// JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Share button functionality
    document.addEventListener('click', function(e) {
        const shareBtn = e.target.closest('.share-btn');
        if (!shareBtn) return;
        
        e.preventDefault();
        
        // Get the post URL from data attribute
        const postUrl = shareBtn.getAttribute('data-post-url');
        
        // Create the full URL (with domain)
        const fullUrl = window.location.origin + postUrl;
        
        // Copy to clipboard
        navigator.clipboard.writeText(fullUrl)
            .then(() => {
                // Show success feedback
                showCopyFeedback(shareBtn, 'Link copied!');
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
                // Fallback for older browsers
                copyToClipboardFallback(fullUrl, shareBtn);
            });
    });
    
    function showCopyFeedback(button, message) {
        // Create or show a tooltip
        let tooltip = button.querySelector('.copy-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('span');
            tooltip.className = 'copy-tooltip';
            button.appendChild(tooltip);
        }
        
        tooltip.textContent = message;
        tooltip.style.display = 'block';
        
        // Hide tooltip after 2 seconds
        setTimeout(() => {
            tooltip.style.display = 'none';
        }, 2000);
    }
    
    // Fallback for older browsers
    function copyToClipboardFallback(text, button) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.top = '0';
        textArea.style.left = '0';
        textArea.style.width = '2em';
        textArea.style.height = '2em';
        textArea.style.padding = '0';
        textArea.style.border = 'none';
        textArea.style.outline = 'none';
        textArea.style.boxShadow = 'none';
        textArea.style.background = 'transparent';
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showCopyFeedback(button, 'Link copied!');
            } else {
                showCopyFeedback(button, 'Press Ctrl+C to copy');
            }
        } catch (err) {
            console.error('Fallback copy failed: ', err);
            showCopyFeedback(button, 'Failed to copy link');
        }
        
        document.body.removeChild(textArea);
    }
});