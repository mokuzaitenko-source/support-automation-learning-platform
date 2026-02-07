// Lesson page functionality
let currentTopicIndex = 0;

// Navigate between topics
function navigateTopic(index) {
    // Hide all topic panels
    document.querySelectorAll('.topic-panel').forEach(panel => {
        panel.classList.remove('active');
    });

    // Show selected topic panel
    const selectedPanel = document.querySelector(`.topic-panel[data-topic-index="${index}"]`);
    if (selectedPanel) {
        selectedPanel.classList.add('active');
    }

    // Update sidebar
    document.querySelectorAll('.topic-item').forEach(item => {
        item.classList.remove('active');
    });

    const selectedItem = document.querySelector(`.topic-item[data-topic-index="${index}"]`);
    if (selectedItem) {
        selectedItem.classList.add('active');
    }

    currentTopicIndex = index;

    // Scroll to top of content
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Run code for a specific topic
async function runCode(topicIndex) {
    const editor = document.getElementById(`code-editor-${topicIndex}`);
    const outputElement = document.getElementById(`output-${topicIndex}`);

    if (!editor) return;

    // Get code from CodeMirror or textarea
    let code;
    if (editor.codeMirrorInstance) {
        code = editor.codeMirrorInstance.getValue();
    } else {
        code = editor.value;
    }

    // Show loading state
    outputElement.textContent = 'Running code...';
    outputElement.classList.remove('error');

    // Execute code
    const result = await executeCode(code);

    // Display result
    formatOutput(outputElement, result);
}

// Add click handlers for topic items
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.topic-item').forEach(item => {
        item.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-topic-index'));
            navigateTopic(index);
        });
    });

    // Add keyboard shortcut for running code (Ctrl/Cmd + Enter)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            runCode(currentTopicIndex);
        }
    });
});
