document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const nameInput = document.querySelector('#id_name');
            if (nameInput && !nameInput.value.trim()) {
                alert("Le nom est requis.");
                event.preventDefault();
            }
        });
    }
});