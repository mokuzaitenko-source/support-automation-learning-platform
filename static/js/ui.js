/**
 * UI Update Manager
 * Handles all DOM updates with defensive programming
 */

const UIManager = {
    /**
     * Safely update element text content
     */
    setText(selector, text) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.textContent = text;
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to set text:', selector, e);
            return false;
        }
    },
    
    /**
     * Safely update element HTML
     */
    setHTML(selector, html) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.innerHTML = html;
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to set HTML:', selector, e);
            return false;
        }
    },
    
    /**
     * Safely update element style
     */
    setStyle(selector, property, value) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.style[property] = value;
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to set style:', selector, e);
            return false;
        }
    },
    
    /**
     * Safely show/hide element
     */
    toggle(selector, show) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.style.display = show ? 'block' : 'none';
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to toggle element:', selector, e);
            return false;
        }
    },
    
    /**
     * Safely add class
     */
    addClass(selector, className) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.classList.add(className);
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to add class:', selector, e);
            return false;
        }
    },
    
    /**
     * Safely remove class
     */
    removeClass(selector, className) {
        try {
            const element = document.querySelector(selector);
            if (element) {
                element.classList.remove(className);
                return true;
            } else {
                console.warn('Element not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to remove class:', selector, e);
            return false;
        }
    },
    
    /**
     * Update progress bar
     */
    updateProgressBar(barSelector, textSelector, percentage, completedCount, totalCount) {
        try {
            const bar = document.querySelector(barSelector);
            const text = document.querySelector(textSelector);
            
            if (bar) {
                bar.style.width = percentage + '%';
            } else {
                console.warn('Progress bar not found:', barSelector);
            }
            
            if (text) {
                if (completedCount !== undefined && totalCount !== undefined) {
                    text.textContent = `${percentage}% Complete (${completedCount}/${totalCount})`;
                } else {
                    text.textContent = `${percentage}% Complete`;
                }
            } else {
                console.warn('Progress text not found:', textSelector);
            }
            
            return bar !== null || text !== null;
        } catch (e) {
            console.error('Failed to update progress bar:', e);
            return false;
        }
    },
    
    /**
     * Show completion badge
     */
    showCompletionBadge(selector) {
        try {
            const badge = document.querySelector(selector);
            if (badge) {
                badge.style.display = 'inline-block';
                badge.classList.add('animate-in');
                return true;
            } else {
                console.warn('Badge not found:', selector);
                return false;
            }
        } catch (e) {
            console.error('Failed to show badge:', e);
            return false;
        }
    },
    
    /**
     * Mark lesson card as complete
     */
    markLessonCardComplete(lessonId) {
        try {
            const card = document.querySelector(`[data-lesson-id="${lessonId}"]`);
            if (card) {
                card.style.borderLeft = '4px solid #4CAF50';
                card.style.opacity = '0.9';
                
                const badge = card.querySelector('.lesson-completed-badge');
                if (badge) {
                    badge.style.display = 'inline-block';
                }
                return true;
            } else {
                console.warn('Lesson card not found:', lessonId);
                return false;
            }
        } catch (e) {
            console.error('Failed to mark lesson card:', e);
            return false;
        }
    }
};

window.UIManager = UIManager;
