// BodyTune AI JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Fix text visibility issues
    fixTextVisibility();

    // Initialize file upload functionality
    initializeFileUpload();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize health score animation
    animateHealthScore();
    
    // Initialize progress bars
    animateProgressBars();
});

function fixTextVisibility() {
    // Fix white text on light backgrounds
    const whiteTextElements = document.querySelectorAll('.text-white');
    whiteTextElements.forEach(element => {
        const parent = element.closest('.bg-white, .bg-light, .card-body');
        if (parent && !element.closest('.bg-primary, .bg-success, .bg-danger, .bg-warning, .bg-info, .bg-dark, .bg-secondary')) {
            element.classList.remove('text-white');
            element.classList.add('text-dark');
        }
    });

    // Ensure card body text is visible
    const cardBodies = document.querySelectorAll('.card-body');
    cardBodies.forEach(cardBody => {
        if (!cardBody.style.color) {
            cardBody.style.color = '#212529';
        }
    });

    // Fix any remaining visibility issues
    const allTextElements = document.querySelectorAll('p, div, span, li, h1, h2, h3, h4, h5, h6');
    allTextElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        const backgroundColor = computedStyle.backgroundColor;
        const color = computedStyle.color;
        
        // If text is white/light and background is white/light, fix it
        if ((color === 'rgb(255, 255, 255)' || color === 'rgba(255, 255, 255, 1)') && 
            (backgroundColor === 'rgb(255, 255, 255)' || backgroundColor === 'rgba(255, 255, 255, 1)' || 
             backgroundColor === 'rgba(0, 0, 0, 0)')) {
            element.style.color = '#212529';
        }
    });
}

function initializeFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('file');

    if (!uploadArea || !fileInput) return;

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        uploadArea.classList.add('dragover');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('dragover');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            displayFileInfo(files[0]);
        }
    }

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            displayFileInfo(e.target.files[0]);
        }
    });

    function displayFileInfo(file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        const fileInfo = document.createElement('div');
        fileInfo.className = 'alert alert-success mt-3';
        fileInfo.innerHTML = `
            <i class="fas fa-file-check me-2"></i>
            <strong>File Selected:</strong> ${file.name} (${fileSize} MB)
        `;
        
        // Remove existing file info
        const existingInfo = uploadArea.parentNode.querySelector('.alert-success');
        if (existingInfo) {
            existingInfo.remove();
        }
        
        uploadArea.parentNode.appendChild(fileInfo);
    }
}

function initializeFormValidation() {
    // Custom form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // BMI auto-calculation
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiInput = document.getElementById('bmi');

    if (heightInput && weightInput && bmiInput) {
        function calculateBMI() {
            const height = parseFloat(heightInput.value);
            const weight = parseFloat(weightInput.value);
            
            if (height && weight) {
                const heightInMeters = height / 100;
                const bmi = weight / (heightInMeters * heightInMeters);
                bmiInput.value = bmi.toFixed(1);
                
                // Add BMI category indication
                let category = '';
                let categoryClass = '';
                
                if (bmi < 18.5) {
                    category = 'Underweight';
                    categoryClass = 'text-info';
                } else if (bmi < 25) {
                    category = 'Normal weight';
                    categoryClass = 'text-success';
                } else if (bmi < 30) {
                    category = 'Overweight';
                    categoryClass = 'text-warning';
                } else {
                    category = 'Obese';
                    categoryClass = 'text-danger';
                }
                
                // Update or create BMI indicator
                let bmiIndicator = document.getElementById('bmi-indicator');
                if (!bmiIndicator) {
                    bmiIndicator = document.createElement('div');
                    bmiIndicator.id = 'bmi-indicator';
                    bmiIndicator.className = 'form-text';
                    bmiInput.parentNode.appendChild(bmiIndicator);
                }
                
                bmiIndicator.innerHTML = `BMI Category: <span class="${categoryClass}">${category}</span>`;
            }
        }

        heightInput.addEventListener('input', calculateBMI);
        weightInput.addEventListener('input', calculateBMI);
    }
}

function animateHealthScore() {
    const scoreElements = document.querySelectorAll('.health-score-value');
    
    scoreElements.forEach(element => {
        const targetValue = parseInt(element.textContent);
        let currentValue = 0;
        const increment = targetValue / 50; // Animation duration
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                element.textContent = targetValue;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue);
            }
        }, 20);
    });
}

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Utility functions
function showLoadingSpinner(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
    button.disabled = true;
    
    return originalText;
}

function hideLoadingSpinner(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Form submission handlers
function handleFormSubmission(formId, endpoint) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = showLoadingSpinner(submitButton);
        
        try {
            const formData = new FormData(form);
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Handle successful response
                const result = await response.text();
                document.body.innerHTML = result;
            } else {
                throw new Error('Failed to process request');
            }
        } catch (error) {
            showAlert('An error occurred while processing your request. Please try again.', 'danger');
            console.error('Form submission error:', error);
        } finally {
            hideLoadingSpinner(submitButton, originalText);
        }
    });
}

// Initialize smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Print functionality
function printResults() {
    window.print();
}

// Export results as PDF (placeholder function)
function exportToPDF() {
    showAlert('PDF export functionality will be available in a future update.', 'info');
}

// Share results (placeholder function)
function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'My BodyTune AI Health Analysis',
            text: 'Check out my personalized health recommendations from BodyTune AI!',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        });
    }
}

// Initialize all functionality
initializeSmoothScrolling();
