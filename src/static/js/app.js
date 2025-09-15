/**
 * LabSync Phase 2 - Frontend JavaScript
 * Handles API integration with Flask backend
 */

// Global state
let resources = [];
let bookings = [];

// Utility functions
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function formatTime(timeStr) {
    if (timeStr.includes('T')) {
        // ISO format from backend
        const date = new Date(timeStr);
        return date.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    } else {
        // HH:MM format
        const [hours, minutes] = timeStr.split(':');
        const date = new Date();
        date.setHours(parseInt(hours), parseInt(minutes));
        return date.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }
}

function getResourceEmoji(resourceName) {
    const emojiMap = {
        'Microscope A': '🔬',
        'Microscope B': '🔬',
        'Cold Room 1': '❄️',
        'Centrifuge': '🌀',
        'PCR Machine': '🧬'
    };
    return emojiMap[resourceName] || '📦';
}

function calculateEndTime(startTime, duration) {
    if (startTime.includes('T')) {
        // ISO format from backend
        const start = new Date(startTime);
        const end = new Date(start.getTime() + duration * 60000);
        return end.toISOString();
    } else {
        // HH:MM format
        const [hours, minutes] = startTime.split(':').map(Number);
        const totalMinutes = hours * 60 + minutes + parseInt(duration);
        const endHours = Math.floor(totalMinutes / 60);
        const endMins = totalMinutes % 60;
        return `${endHours.toString().padStart(2, '0')}:${endMins.toString().padStart(2, '0')}`;
    }
}

// API functions
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

async function loadResources() {
    try {
        resources = await apiRequest('/api/resources');
        populateResourceDropdowns();
    } catch (error) {
        showAlert('Failed to load resources: ' + error.message, 'error');
    }
}

async function loadBookings() {
    try {
        const filterResource = document.getElementById('filterResource').value;
        const filterDate = document.getElementById('filterDate').value;
        
        let url = '/api/bookings';
        const params = new URLSearchParams();
        
        if (filterResource) params.append('resource', filterResource);
        if (filterDate) params.append('date', filterDate);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }

        bookings = await apiRequest(url);
        renderBookings();
    } catch (error) {
        showAlert('Failed to load bookings: ' + error.message, 'error');
    }
}

async function createBooking(bookingData) {
    try {
        const startDateTime = `${bookingData.date}T${bookingData.startTime}`;
        
        const result = await apiRequest('/api/bookings', {
            method: 'POST',
            body: JSON.stringify({
                user: bookingData.userName,
                resource_id: bookingData.resourceId,
                start_time: startDateTime,
                duration: parseInt(bookingData.duration)
            })
        });

        return { success: true, data: result };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

async function deleteBooking(bookingId) {
    try {
        await apiRequest(`/api/bookings/${bookingId}`, {
            method: 'DELETE'
        });
        return true;
    } catch (error) {
        showAlert('Failed to delete booking: ' + error.message, 'error');
        return false;
    }
}

async function loadStats() {
    try {
        const stats = await apiRequest('/api/stats');
        
        document.getElementById('totalBookings').textContent = stats.total_bookings;
        document.getElementById('todayBookings').textContent = stats.today_bookings;
        document.getElementById('availableResources').textContent = stats.available_resources;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}



// UI functions
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    
    alertContainer.innerHTML = `
        <div class="alert ${alertClass}">
            ${message}
        </div>
    `;

    setTimeout(() => {
        alertContainer.innerHTML = '';
    }, 5000);
}

function populateResourceDropdowns() {
    const resourceSelect = document.getElementById('resource');
    const filterResourceSelect = document.getElementById('filterResource');
    
    // Clear existing options (except first)
    resourceSelect.innerHTML = '<option value="">Select a resource...</option>';
    filterResourceSelect.innerHTML = '<option value="">All Resources</option>';
    
    resources.forEach(resource => {
        const emoji = getResourceEmoji(resource.name);
        const option = new Option(`${emoji} ${resource.name}`, resource.id);
        const filterOption = new Option(`${emoji} ${resource.name}`, resource.id);
        
        resourceSelect.appendChild(option);
        filterResourceSelect.appendChild(filterOption);
    });
}

function renderBookings() {
    const bookingsList = document.getElementById('bookingsList');

    if (bookings.length === 0) {
        bookingsList.innerHTML = `
            <div style="text-align: center; color: #6B7280; padding: 40px;">
                No bookings found. Create your first booking!
            </div>
        `;
        return;
    }

    bookingsList.innerHTML = bookings.map(booking => {
        const emoji = getResourceEmoji(booking.resource_name);
        const endTime = calculateEndTime(booking.start_time, booking.duration);
        const startDate = booking.start_time.includes('T') ? booking.start_time.split('T')[0] : booking.date;
        
        return `
            <div class="booking-item">
                <div class="booking-info">
                    <div class="booking-resource">${emoji} ${booking.resource_name}</div>
                    <div class="booking-details">
                        📅 ${formatDate(startDate)} | 
                        ⏰ ${formatTime(booking.start_time)} - ${formatTime(endTime)} 
                        (${booking.duration} min)
                    </div>
                    <div class="booking-user">👤 ${booking.user}</div>
                </div>
                <button class="btn btn-danger" onclick="handleDeleteBooking('${booking.id}')">
                    🗑️ Delete
                </button>
            </div>
        `;
    }).join('');
}

// Event handlers
async function handleDeleteBooking(bookingId) {
    if (confirm('Are you sure you want to delete this booking?')) {
        if (await deleteBooking(bookingId)) {
            showAlert('Booking deleted successfully');
            await loadBookings();
            await loadStats();
        }
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const submitButton = document.getElementById('submitButton');
    const originalText = submitButton.textContent;
    
    try {
        // Show loading state
        submitButton.textContent = '⏳ Creating Booking...';
        submitButton.disabled = true;
        
        const formData = new FormData(e.target);
        const bookingData = {
            userName: formData.get('userName'),
            resourceId: formData.get('resource'),
            date: formData.get('date'),
            startTime: formData.get('startTime'),
            duration: formData.get('duration')
        };

        // Validate required fields
        if (!bookingData.userName || !bookingData.resourceId || !bookingData.date || 
            !bookingData.startTime || !bookingData.duration) {
            showAlert('All fields are required', 'error');
            return;
        }

        const result = await createBooking(bookingData);
        
        if (result.success) {
            showAlert('Booking created successfully!');
            e.target.reset();
            
            // Reset date to today
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('date').value = today;
            
            // Reload data
            await loadBookings();
            await loadStats();
        } else {
            showAlert(result.message, 'error');
        }

    } catch (error) {
        showAlert('Error creating booking: ' + error.message, 'error');
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').setAttribute('min', today);
    document.getElementById('date').value = today;

    // Event listeners
    document.getElementById('bookingForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('filterResource').addEventListener('change', loadBookings);
    document.getElementById('filterDate').addEventListener('change', loadBookings);

    // Initial data load
    Promise.all([
        loadResources(),
        loadBookings(),
        loadStats()
    ]).catch(error => {
        console.error('Failed to initialize application:', error);
        showAlert('Failed to load application data. Please refresh the page.', 'error');
    });

    // Auto-refresh stats every minute
    setInterval(loadStats, 60000);
    
    // Auto-refresh bookings every 30 seconds
    setInterval(loadBookings, 30000);
});