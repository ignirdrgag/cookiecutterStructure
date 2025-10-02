function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

function openEditRoomModal(modalId, rooms, roomId) {
    const room = rooms.find(r => r.id === roomId);
    if (room) {
        const form = document.getElementById('editRoomForm');
        form.querySelector('[name="room_id"]').value = room.id;
        form.querySelector('[name="name"]').value = room.name;
        form.querySelector('[name="description"]').value = room.description;
        form.querySelector('[name="price"]').value = room.price;
        form.querySelector('[name="category"]').value = room.category ? room.category : '';
        form.querySelector('[name="status"]').value = room.status ? room.status : '';
        openModal(modalId);
    }
}

function openDeleteRoomModal(modalId, id) {
    document.getElementById('deleteRoomForm').querySelector('[name="room_id"]').value = id;
    openModal(modalId);
}

function openEditCategoryModal(modalId, categories, categoryId) {
    const category = categories.find(c => c.id === categoryId);
    if (category) {
        const form = document.getElementById('editCategoryForm');
        form.querySelector('[name="category_id"]').value = category.id;
        form.querySelector('[name="name"]').value = category.name;
        form.querySelector('[name="description"]').value = category.description;
        openModal(modalId);
    }
}

function openDeleteCategoryModal(modalId, id) {
    document.getElementById('deleteCategoryForm').querySelector('[name="category_id"]').value = id;
    openModal(modalId);
}

function openEditStatusModal(modalId, statuses, statusId) {
    const status = statuses.find(s => s.id === statusId);
    if (status) {
        const form = document.getElementById('editStatusForm');
        form.querySelector('[name="status_id"]').value = status.id;
        form.querySelector('[name="name"]').value = status.name;
        openModal(modalId);
    }
}

function openDeleteStatusModal(modalId, id) {
    document.getElementById('deleteStatusForm').querySelector('[name="status_id"]').value = id;
    openModal(modalId);
}

function openEditReservationModal(modalId, reservations, reservationId) {
    const reservation = reservations.find(r => r.id === reservationId);
    if (reservation) {
        const form = document.getElementById('editReservationForm');
        form.querySelector('[name="reservation_id"]').value = reservation.id;
        form.querySelector('[name="room"]').value = reservation.room ? reservation.room : '';
        form.querySelector('[name="check_in"]').value = reservation.check_in;
        form.querySelector('[name="check_out"]').value = reservation.check_out;
        openModal(modalId);
    }
}

function openDeleteReservationModal(modalId, id) {
    document.getElementById('deleteReservationForm').querySelector('[name="reservation_id"]').value = id;
    openModal(modalId);
}

document.addEventListener('DOMContentLoaded', () => {
    // Gestion du formulaire de création de chambre
    document.getElementById('createRoomForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/rooms/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de modification de chambre
    document.getElementById('editRoomForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/rooms/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de suppression de chambre
    document.getElementById('deleteRoomForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/rooms/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de création de catégorie
    document.getElementById('createCategoryForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/categories/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de modification de catégorie
    document.getElementById('editCategoryForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/categories/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de suppression de catégorie
    document.getElementById('deleteCategoryForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/categories/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de création de statut
    document.getElementById('createStatusForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/statuses/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de modification de statut
    document.getElementById('editStatusForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/statuses/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de suppression de statut
    document.getElementById('deleteStatusForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/content/statuses/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de création de réservation
    document.getElementById('createReservationForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/services/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de modification de réservation
    document.getElementById('editReservationForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/services/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message + '\n' + JSON.stringify(data.errors));
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });

    // Gestion du formulaire de suppression de réservation
    document.getElementById('deleteReservationForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/services/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Erreur : ' + error.message);
        }
    });
});