/**
 * scripts.js - Gestion globale des modales, formulaires AJAX et interactions
 * Compatible avec les templates Django pour rooms, categories, statuses, reservations
 * Utilise JWT pour l'authentification et CSRF pour la sécurité
 */

// === UTILITAIRES GÉNÉRAUX ===
/**
 * Ouvre une modale en ajoutant/removant la classe 'hidden' (Tailwind/Flowbite compatible)
 * @param {string} modalId - ID de la modale
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden'); // Empêche le scroll
    } else {
        console.warn(`Modale ${modalId} non trouvée`);
    }
}

/**
 * Ferme une modale
 * @param {string} modalId - ID de la modale
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    } else {
        console.warn(`Modale ${modalId} non trouvée`);
    }
}

/**
 * Toggle la sidebar (si présente)
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

/**
 * Récupère les en-têtes d'authentification (JWT + CSRF)
 * @returns {Object} Headers pour fetch
 */
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    return {
        'X-CSRFToken': csrfToken,
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json' // Par défaut ; override pour FormData
    };
}

/**
 * Affiche une notification (fallback sur alert si pas de système de toasts)
 * @param {string} type - 'success' ou 'error'
 * @param {string} message - Message à afficher
 */
function showNotification(type, message) {
    // Si notificationManager est disponible (de vos scripts communs)
    if (window.notificationManager) {
        if (type === 'success') {
            window.notificationManager.showSuccess(message);
        } else {
            window.notificationManager.showError(message);
        }
        return;
    }
    // Fallback sur alert
    alert(`${type.toUpperCase()}: ${message}`);
}

// === FONCTIONS PAR ENTITÉ ===
// Note: Les fonctions openEdit* attendent maintenant les données via data-attributes ou globales.
// Pour éviter les params globaux, on peut les passer en arguments ou fetcher via API si besoin.

// Chambres
function openEditRoomModal(modalId, roomId) {
    // Récupère les données de la ligne du tableau via data-attributes (recommandé)
    const row = document.querySelector(`[data-room-id="${roomId}"]`);
    if (!row) {
        showNotification('error', 'Chambre non trouvée');
        return;
    }

    const form = document.getElementById('editRoomForm');
    if (!form) {
        showNotification('error', 'Formulaire de modification non trouvé');
        return;
    }

    // Remplit le formulaire avec les data-attributes de la ligne (ajoutez-les dans le template)
    form.querySelector('[name="room_id"]').value = roomId;
    form.querySelector('[name="name"]').value = row.dataset.name || '';
    form.querySelector('[name="description"]').value = row.dataset.description || '';
    form.querySelector('[name="price"]').value = row.dataset.price || '';
    form.querySelector('[name="category"]').value = row.dataset.category || '';
    form.querySelector('[name="status"]').value = row.dataset.status || '';

    openModal(modalId);
}

function openDeleteRoomModal(modalId, roomId) {
    const form = document.getElementById('deleteRoomForm');
    if (form) {
        form.querySelector('[name="room_id"]').value = roomId;
    }
    openModal(modalId);
}

// Catégories
function openEditCategoryModal(modalId, categoryId) {
    const row = document.querySelector(`[data-category-id="${categoryId}"]`);
    if (!row) {
        showNotification('error', 'Catégorie non trouvée');
        return;
    }

    const form = document.getElementById('editCategoryForm');
    if (!form) {
        showNotification('error', 'Formulaire de modification non trouvé');
        return;
    }

    form.querySelector('[name="category_id"]').value = categoryId;
    form.querySelector('[name="name"]').value = row.dataset.name || '';
    form.querySelector('[name="description"]').value = row.dataset.description || '';

    openModal(modalId);
}

function openDeleteCategoryModal(modalId, categoryId) {
    const form = document.getElementById('deleteCategoryForm');
    if (form) {
        form.querySelector('[name="category_id"]').value = categoryId;
    }
    openModal(modalId);
}

// Statuts
function openEditStatusModal(modalId, statusId) {
    const row = document.querySelector(`[data-status-id="${statusId}"]`);
    if (!row) {
        showNotification('error', 'Statut non trouvé');
        return;
    }

    const form = document.getElementById('editStatusForm');
    if (!form) {
        showNotification('error', 'Formulaire de modification non trouvé');
        return;
    }

    form.querySelector('[name="status_id"]').value = statusId;
    form.querySelector('[name="name"]').value = row.dataset.name || '';

    openModal(modalId);
}

function openDeleteStatusModal(modalId, statusId) {
    const form = document.getElementById('deleteStatusForm');
    if (form) {
        form.querySelector('[name="status_id"]').value = statusId;
    }
    openModal(modalId);
}

// Réservations
function openEditReservationModal(modalId, reservationId) {
    const row = document.querySelector(`[data-reservation-id="${reservationId}"]`);
    if (!row) {
        showNotification('error', 'Réservation non trouvée');
        return;
    }

    const form = document.getElementById('editReservationForm');
    if (!form) {
        showNotification('error', 'Formulaire de modification non trouvé');
        return;
    }

    form.querySelector('[name="reservation_id"]').value = reservationId;
    form.querySelector('[name="room"]').value = row.dataset.room || '';
    form.querySelector('[name="check_in"]').value = row.dataset.checkIn || '';
    form.querySelector('[name="check_out"]').value = row.dataset.checkOut || '';

    openModal(modalId);
}

function openDeleteReservationModal(modalId, reservationId) {
    const form = document.getElementById('deleteReservationForm');
    if (form) {
        form.querySelector('[name="reservation_id"]').value = reservationId;
    }
    openModal(modalId);
}

// === GESTION DES ÉVÉNEMENTS (AJAX) ===
document.addEventListener('DOMContentLoaded', () => {
    // Fermeture des modales au clic extérieur ou Escape
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('fixed') && e.target.classList.contains('inset-0')) {
            const modalId = e.target.id;
            closeModal(modalId);
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.fixed:not(.hidden)');
            if (openModals.length > 0) {
                closeModal(openModals[openModals.length - 1].id);
            }
        }
    });

    // Login (spécifique à la page de connexion)
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };

            try {
                const response = await fetch('/api/token/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getAuthHeaders()['X-CSRFToken']
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();

                if (response.ok) {
                    localStorage.setItem('access_token', result.access);
                    localStorage.setItem('refresh_token', result.refresh);
                    showNotification('success', '{% trans "Connexion réussie !" %}');
                    // Redirection après délai pour UX
                    setTimeout(() => {
                        window.location.href = '/services/' || '/dashboard/';
                    }, 1000);
                } else {
                    showNotification('error', result.detail || '{% trans "Identifiants invalides" %}');
                }
            } catch (error) {
                console.error('Login error:', error);
                showNotification('error', '{% trans "Erreur de connexion" %}: ' + error.message);
            }
        });
    }

    // Fonction générique pour soumettre un formulaire AJAX (réutilisable)
    async function submitFormAjax(form, url, method = 'POST') {
        const formData = new FormData(form);
        const headers = { ...getAuthHeaders() };
        // Pas de Content-Type pour FormData (laisse le browser gérer multipart)

        try {
            const response = await fetch(url, {
                method,
                body: formData,
                headers: headers
            });
            const data = await response.json();

            if (data.success) {
                showNotification('success', data.message || '{% trans "Opération réussie" %}');
                closeModal(form.closest('.fixed')?.id || ''); // Ferme la modale parente si applicable
                setTimeout(() => window.location.reload(), 1500); // Recharge après succès
            } else {
                showNotification('error', data.message || '{% trans "Erreur lors de l\'opération" %}');
                if (data.errors) {
                    console.error('Form errors:', data.errors);
                    // Optionnel: Afficher les erreurs dans le formulaire
                    Object.keys(data.errors).forEach(field => {
                        const input = form.querySelector(`[name="${field}"]`);
                        if (input) {
                            input.classList.add('border-red-500');
                            // Ajoutez un span d'erreur si besoin
                        }
                    });
                }
            }
        } catch (error) {
            console.error('AJAX error:', error);
            showNotification('error', '{% trans "Erreur réseau" %}: ' + error.message);
        }
    }

    // Event listeners pour les formulaires (seulement si présents)
    const formHandlers = {
        // Chambres
        createRoomForm: { selector: '#createRoomForm', url: '/content/rooms/create_room/' },
        editRoomForm: { selector: '#editRoomForm', handler: (form) => {
            const roomId = form.querySelector('[name="room_id"]').value;
            return `/content/rooms/${roomId}/edit_room/`;
        }},
        deleteRoomForm: { selector: '#deleteRoomForm', handler: (form) => {
            const roomId = form.querySelector('[name="room_id"]').value;
            return `/content/rooms/${roomId}/delete_room/`;
        }},

        // Catégories
        createCategoryForm: { selector: '#createCategoryForm', url: '/content/categories/create_category/' },
        editCategoryForm: { selector: '#editCategoryForm', handler: (form) => {
            const categoryId = form.querySelector('[name="category_id"]').value;
            return `/content/categories/${categoryId}/edit_category/`;
        }},
        deleteCategoryForm: { selector: '#deleteCategoryForm', handler: (form) => {
            const categoryId = form.querySelector('[name="category_id"]').value;
            return `/content/categories/${categoryId}/delete_category/`;
        }},

        // Statuts
        createStatusForm: { selector: '#createStatusForm', url: '/content/statuses/create_status/' },
        editStatusForm: { selector: '#editStatusForm', handler: (form) => {
            const statusId = form.querySelector('[name="status_id"]').value;
            return `/content/statuses/${statusId}/edit_status/`;
        }},
        deleteStatusForm: { selector: '#deleteStatusForm', handler: (form) => {
            const statusId = form.querySelector('[name="status_id"]').value;
            return `/content/statuses/${statusId}/delete_status/`;
        }},

        // Réservations
        createReservationForm: { selector: '#createReservationForm', url: '/services/reservations/create_reservation/' },
        editReservationForm: { selector: '#editReservationForm', handler: (form) => {
            const reservationId = form.querySelector('[name="reservation_id"]').value;
            return `/services/reservations/${reservationId}/edit_reservation/`;
        }},
        deleteReservationForm: { selector: '#deleteReservationForm', handler: (form) => {
            const reservationId = form.querySelector('[name="reservation_id"]').value;
            return `/services/reservations/${reservationId}/delete_reservation/`;
        }}
    };

    // Attache les listeners
    Object.entries(formHandlers).forEach(([key, config]) => {
        const form = document.querySelector(config.selector);
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                let url = config.url;
                if (config.handler) {
                    url = config.handler(form);
                }
                await submitFormAjax(form, url);
            });
        }
    });
});