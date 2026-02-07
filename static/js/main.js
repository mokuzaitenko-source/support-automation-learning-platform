// Initialize CodeMirror editors on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize all code editors
    initializeCodeEditors();
});

function initializeCodeEditors() {
    const editors = document.querySelectorAll('.code-editor');
    editors.forEach(editor => {
        if (typeof CodeMirror !== 'undefined') {
            const cm = CodeMirror.fromTextArea(editor, {
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                indentUnit: 4,
                indentWithTabs: false,
                lineWrapping: true,
                matchBrackets: true,
                autoCloseBrackets: true
            });
            
            // Store CodeMirror instance for later use
            editor.codeMirrorInstance = cm;
        }
    });
}

// Utility function to execute code
async function executeCode(code) {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }
        
        const response = await fetch('/execute', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();
        return result;
    } catch (error) {
        return {
            success: false,
            output: `Error: ${error.message}`
        };
    }
}

// Format output for display
function formatOutput(outputElement, result) {
    outputElement.textContent = result.output || 'No output';
    
    if (result.success) {
        outputElement.classList.remove('error');
    } else {
        outputElement.classList.add('error');
    }
}
