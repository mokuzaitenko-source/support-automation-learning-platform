/**
 * Centralized Progress Storage Manager
 * Single source of truth for all localStorage operations
 */

const ProgressManager = {
    STORAGE_KEY: 'completedLessons',
    
    /**
     * Get all completed lessons
     * @returns {Object} Map of pathId to array of lessonIds
     */
    getAll() {
        try {
            const stored = localStorage.getItem(this.STORAGE_KEY);
            return stored ? JSON.parse(stored) : {};
        } catch (e) {
            console.error('Failed to load progress from storage:', e);
            return {};
        }
    },
    
    /**
     * Mark a lesson as complete
     * @param {string} pathId - The learning path ID
     * @param {string} lessonId - The lesson ID
     * @returns {boolean} True if newly completed, false if already completed
     */
    markComplete(pathId, lessonId) {
        try {
            if (!pathId || !lessonId) {
                console.error('Invalid pathId or lessonId:', { pathId, lessonId });
                return false;
            }
            
            const completed = this.getAll();
            
            if (!completed[pathId]) {
                completed[pathId] = [];
            }
            
            if (!completed[pathId].includes(lessonId)) {
                completed[pathId].push(lessonId);
                localStorage.setItem(this.STORAGE_KEY, JSON.stringify(completed));
                console.log(`Marked complete: ${pathId}/${lessonId}`);
                return true;
            }
            
            console.log(`Already complete: ${pathId}/${lessonId}`);
            return false;
        } catch (e) {
            console.error('Failed to mark lesson complete:', e);
            return false;
        }
    },
    
    /**
     * Check if a lesson is complete
     * @param {string} pathId - The learning path ID
     * @param {string} lessonId - The lesson ID
     * @returns {boolean} True if completed
     */
    isComplete(pathId, lessonId) {
        try {
            const completed = this.getAll();
            return completed[pathId] && completed[pathId].includes(lessonId);
        } catch (e) {
            console.error('Failed to check completion status:', e);
            return false;
        }
    },
    
    /**
     * Get progress for a specific path
     * @param {string} pathId - The learning path ID
     * @param {number} totalLessons - Total number of lessons in path
     * @returns {Object} { completed: number, total: number, percentage: number }
     */
    getPathProgress(pathId, totalLessons) {
        try {
            const completed = this.getAll();
            const completedCount = completed[pathId] ? completed[pathId].length : 0;
            const percentage = totalLessons > 0 ? Math.round((completedCount / totalLessons) * 100) : 0;
            
            return {
                completed: completedCount,
                total: totalLessons,
                percentage: percentage
            };
        } catch (e) {
            console.error('Failed to get path progress:', e);
            return { completed: 0, total: totalLessons, percentage: 0 };
        }
    },
    
    /**
     * Get completed lessons for a path
     * @param {string} pathId - The learning path ID
     * @returns {Array} Array of completed lesson IDs
     */
    getCompletedForPath(pathId) {
        try {
            const completed = this.getAll();
            return completed[pathId] || [];
        } catch (e) {
            console.error('Failed to get completed lessons:', e);
            return [];
        }
    },
    
    /**
     * Clear all progress data
     * @returns {boolean} True if successful
     */
    clearAll() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            console.log('All progress cleared');
            return true;
        } catch (e) {
            console.error('Failed to clear progress:', e);
            return false;
        }
    },
    
    /**
     * Export progress data as JSON
     * @returns {string} JSON string of all progress
     */
    export() {
        try {
            const data = this.getAll();
            return JSON.stringify(data, null, 2);
        } catch (e) {
            console.error('Failed to export progress:', e);
            return '{}';
        }
    },
    
    /**
     * Import progress data from JSON
     * @param {string} jsonString - JSON string to import
     * @returns {boolean} True if successful
     */
    import(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
            console.log('Progress imported successfully');
            return true;
        } catch (e) {
            console.error('Failed to import progress:', e);
            return false;
        }
    }
};

// Make available globally
window.ProgressManager = ProgressManager;
