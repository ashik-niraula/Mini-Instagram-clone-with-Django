
// Profile tabs switching
const tabs = document.querySelectorAll('.tab');
if (tabs.length > 0) {
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active from all tabs
      tabs.forEach(t => t.classList.remove('active'));
      // Add active to clicked tab
      tab.classList.add('active');
    });
  });
}

// Search suggestions
const searchInput = document.querySelector('#searchSuggestions');
if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.suggestion-card');
    
    cards.forEach(card => {
      const username = card.querySelector('h3').textContent.toLowerCase();
      const name = card.querySelector('p').textContent.toLowerCase();
      
      if (username.includes(searchTerm) || name.includes(searchTerm)) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Image upload preview
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector('#fileInput');
    const previewImg = document.querySelector('#previewImage');
    const uploadArea = document.querySelector('.upload-area');
    const selectBtn = document.querySelector('#selectBtn');
    const uploadPreview = document.querySelector('.upload-preview');

    if (!fileInput || !previewImg || !uploadArea || !selectBtn) return;

    // "Select from Computer" button
    selectBtn.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    // Upload area (ignore clicks on the button inside it)
    uploadArea.addEventListener('click', (e) => {
        if (e.target === selectBtn) return;  // <-- prevents double click
        fileInput.click();
    });

    // When selecting an image
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;

            uploadPreview.classList.remove('hidden');
            uploadArea.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    });
});


// Password show/hide
const showPasswordBtns = document.querySelectorAll('.show-password');
showPasswordBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.previousElementSibling;
    const icon = btn.querySelector('i');
    
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  });  
document.addEventListener('click', function(e) {
    // Click three dots
    if (e.target.closest('.dots-btn')) {
        e.preventDefault();
        e.stopPropagation();
        
        const btn = e.target.closest('.dots-btn');
        const menu = btn.nextElementSibling;
        
        // Close other menus
        document.querySelectorAll('.mini-menu.show').forEach(m => {
            if (m !== menu) m.classList.remove('show');
        });
        
        // Toggle current menu
        menu.classList.toggle('show');
    }
    
    // Click pencil icon
    if (e.target.closest('.edit-btn')) {
        e.preventDefault();
        const commentId = e.target.closest('.edit-btn').getAttribute('data-comment-id');
        console.log('Edit:', commentId);
        // Your edit code here
    }
    
    // Click trash icon
    if (e.target.closest('.delete-btn')) {
        e.preventDefault();
        const commentId = e.target.closest('.delete-btn').getAttribute('data-comment-id');
        console.log('Delete:', commentId);
        // Your delete code here
    }
    
    // Click outside to close
    if (!e.target.closest('.comment-options')) {
        document.querySelectorAll('.mini-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

});
