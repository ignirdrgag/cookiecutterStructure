document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const checkIn = document.querySelector('#id_check_in').value;
            const checkOut = document.querySelector('#id_check_out').value;
            if (new Date(checkIn) >= new Date(checkOut)) {
                alert("La date de départ doit être après la date d'arrivée.");
                event.preventDefault();
            }
        });
    }
});