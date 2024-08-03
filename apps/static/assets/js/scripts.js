const notificationsPerPage = 5;
let currentPage = 1;
let notifications = [];

// Function to fetch notifications and display them
async function loadNotifications() {
    try {
        document.getElementById('loading-spinner').style.display = 'block';
        console.log('Fetching notifications...');
        const response = await fetch('/api/notifications');
        console.log('Response received:', response);
        const data = await response.json();
        console.log('Data received:', data);
        notifications = data.alerts;
        notifications.reverse(); // Reverse notifications to show latest first
        renderNotifications();
    } catch (error) {
        console.error('Error fetching notifications:', error);
    } finally {
        document.getElementById('loading-spinner').style.display = 'none';
    }
}

// Function to render notifications for the current page
function renderNotifications() {
    const container = document.getElementById('notifications-container');
    const pageInfo = document.getElementById('page-info');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    container.innerHTML = ''; // Clear previous content

    const startIndex = (currentPage - 1) * notificationsPerPage;
    const endIndex = Math.min(startIndex + notificationsPerPage, notifications.length);
    const pageNotifications = notifications.slice(startIndex, endIndex);

    pageNotifications.forEach(alert => {
        // Create notification element
        const alertDiv = document.createElement('div');
        alertDiv.className = 'notification';

        // Add disease and recommendation
        const disease = document.createElement('h3');
        disease.innerText = alert.disease;
        alertDiv.appendChild(disease);

        const recommendation = document.createElement('p');
        recommendation.innerText = alert.recommendation;
        alertDiv.appendChild(recommendation);

        // Add image if available
        if (alert.image) {
            const img = document.createElement('img');
            img.dataset.src = `data:image/jpeg;base64,${alert.image}`;
            img.alt = alert.disease;
            img.className = 'notification-image lazy-load';
            img.addEventListener('click', () => img.classList.toggle('show')); // Toggle image visibility
            
            // Add image link
            const link = document.createElement('a');
            link.href = `data:image/jpeg;base64,${alert.image}`;
            link.target = '_blank'; // Open in a new tab
            link.innerText = 'View Image';
            link.className = 'image-link';

            alertDiv.appendChild(img);
            alertDiv.appendChild(link);
        }

        // Append to container
        container.appendChild(alertDiv);
    });

    // Lazy load images
    lazyLoadImages();

    // Update pagination buttons
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = endIndex >= notifications.length;
    pageInfo.innerText = `Page ${currentPage}`;
}

// Function to lazy load images
function lazyLoadImages() {
    const lazyImages = document.querySelectorAll('.lazy-load');
    const config = {
        rootMargin: '0px 0px 50px 0px',
        threshold: 0
    };

    let observer = new IntersectionObserver((entries, self) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                preloadImage(entry.target);
                self.unobserve(entry.target);
            }
        });
    }, config);

    lazyImages.forEach(image => {
        observer.observe(image);
    });
}

function preloadImage(img) {
    const src = img.dataset.src;
    if (!src) {
        return;
    }
    img.src = src;
}

// Event listeners for pagination buttons
document.getElementById('prev-page').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderNotifications();
    }
});

document.getElementById('next-page').addEventListener('click', () => {
    if (currentPage * notificationsPerPage < notifications.length) {
        currentPage++;
        renderNotifications();
    }
});

// Load notifications on page load
window.onload = loadNotifications;
