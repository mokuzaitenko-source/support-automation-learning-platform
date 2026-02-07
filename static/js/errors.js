/**
 * Error Handler and Logger
 * Centralized error handling with user-friendly messages
 */

const ErrorHandler = {
    // Log levels
    ERROR: 'error',
    WARN: 'warn',
    INFO: 'info',
    
    /**
     * Log error to console with context
     */
    log(level, message, context) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [${level.toUpperCase()}] ${message}`;
        
        if (context) {
            console[level](logMessage, context);
        } else {
            console[level](logMessage);
        }
    },
    
    /**
     * Show user-friendly error notification
     */
    notify(message, type = 'error') {
        try {
            // Create notification element if it doesn't exist
            let notification = document.getElementById('error-notification');
            
            if (!notification) {
                notification = document.createElement('div');
                notification.id = 'error-notification';
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    max-width: 400px;
                    padding: 15px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    z-index: 10000;
                    display: none;
                    animation: slideIn 0.3s ease-out;
                `;
                document.body.appendChild(notification);
            }
            
            // Set styling based on type
            const colors = {
                error: { bg: '#f44336', text: '#fff' },
                warn: { bg: '#ff9800', text: '#fff' },
                success: { bg: '#4CAF50', text: '#fff' },
                info: { bg: '#2196F3', text: '#fff' }
            };
            
            const color = colors[type] || colors.error;
            notification.style.backgroundColor = color.bg;
            notification.style.color = color.text;
            notification.textContent = message;
            notification.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                notification.style.display = 'none';
            }, 5000);
        } catch (e) {
            console.error('Failed to show notification:', e);
        }
    },
    
    /**
     * Handle fetch errors with user-friendly messages
     */
    handleFetchError(error, context = '') {
        let message = 'Network error occurred';
        
        if (error.message.includes('Failed to fetch')) {
            message = 'Cannot connect to server. Please check if the server is running.';
        } else if (error.message.includes('NetworkError')) {
            message = 'Network connection lost. Please check your internet.';
        } else if (error.message.includes('timeout')) {
            message = 'Request timed out. Please try again.';
        }
        
        if (context) {
            message += ' (' + context + ')';
        }
        
        this.log(this.ERROR, message, error);
        this.notify(message, 'error');
    },
    
    /**
     * Wrap function with error boundary
     */
    wrap(fn, context = 'Unknown operation') {
        return function(...args) {
            try {
                const result = fn.apply(this, args);
                
                // Handle promises
                if (result && typeof result.catch === 'function') {
                    return result.catch(e => {
                        ErrorHandler.log(ErrorHandler.ERROR, `Promise rejection in ${context}`, e);
                        ErrorHandler.notify(`Failed: ${context}`);
                        throw e;
                    });
                }
                
                return result;
            } catch (e) {
                ErrorHandler.log(ErrorHandler.ERROR, `Error in ${context}`, e);
                ErrorHandler.notify(`Failed: ${context}`);
                throw e;
            }
        };
    },
    
    /**
     * Check if all required dependencies are loaded
     */
    checkDependencies() {
        const missing = [];
        
        if (!window.ProgressManager) missing.push('ProgressManager');
        if (!window.UIManager) missing.push('UIManager');
        if (typeof CodeMirror === 'undefined') {
            this.log(this.WARN, 'CodeMirror not loaded - using fallback editor');
        }
        
        if (missing.length > 0) {
            const message = 'Missing dependencies: ' + missing.join(', ');
            this.log(this.ERROR, message);
            this.notify(message + '. Some features may not work.', 'warn');
            return false;
        }
        
        this.log(this.INFO, 'All dependencies loaded successfully');
        return true;
    }
};

// Add CSS for notification animation
const style = document.createElement('style');
style.textContent = `
@keyframes slideIn {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;
document.head.appendChild(style);

// Global error handler
window.addEventListener('error', function(event) {
    ErrorHandler.log(ErrorHandler.ERROR, 'Uncaught error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
});

// Global promise rejection handler
window.addEventListener('unhandledrejection', function(event) {
    ErrorHandler.log(ErrorHandler.ERROR, 'Unhandled promise rejection', event.reason);
});

// Make available globally
window.ErrorHandler = ErrorHandler;

// Check dependencies on load
window.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        ErrorHandler.checkDependencies();
    }, 100);
});
