"""
Progress Tracking System
Handles lesson completion storage and retrieval
"""

import json
import os
from datetime import datetime

PROGRESS_FILE = 'progress_data.json'

def load_progress():
    """Load progress data from file"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_progress(data):
    """Save progress data to file"""
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving progress: {e}")
        return False

def mark_complete(path_id, lesson_id):
    """Mark a lesson as complete"""
    progress = load_progress()
    
    if path_id not in progress:
        progress[path_id] = {
            'completed': [],
            'last_updated': datetime.now().isoformat()
        }
    
    if lesson_id not in progress[path_id]['completed']:
        progress[path_id]['completed'].append(lesson_id)
        progress[path_id]['last_updated'] = datetime.now().isoformat()
    
    save_progress(progress)
    return progress

def get_completed(path_id):
    """Get all completed lessons for a path"""
    progress = load_progress()
    if path_id in progress:
        return progress[path_id]['completed']
    return []

def get_progress(path_id, total_lessons):
    """Get progress percentage for a path"""
    completed = get_completed(path_id)
    completed_count = len(completed)
    percentage = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
    
    return {
        'completed': completed_count,
        'total': total_lessons,
        'percentage': percentage,
        'lessons': completed
    }

def is_complete(path_id, lesson_id):
    """Check if a lesson is complete"""
    completed = get_completed(path_id)
    return lesson_id in completed

def get_all_progress():
    """Get all progress data"""
    return load_progress()

def clear_progress():
    """Clear all progress"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    return True
