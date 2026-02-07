// Playground functionality
let playgroundEditor;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize playground editor
    const editor = document.getElementById('playground-editor');
    
    if (editor && typeof CodeMirror !== 'undefined') {
        playgroundEditor = CodeMirror.fromTextArea(editor, {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            extraKeys: {
                'Ctrl-Enter': function(cm) {
                    runPlaygroundCode();
                },
                'Cmd-Enter': function(cm) {
                    runPlaygroundCode();
                }
            }
        });
    }
});

// Run code in playground
async function runPlaygroundCode() {
    const outputElement = document.getElementById('playground-output');
    
    if (!playgroundEditor) return;

    const code = playgroundEditor.getValue();

    // Show loading state
    outputElement.textContent = 'Running code...';
    outputElement.classList.remove('error');

    // Execute code
    const result = await executeCode(code);

    // Display result
    formatOutput(outputElement, result);
}

// Clear playground editor
function clearPlayground() {
    if (playgroundEditor) {
        playgroundEditor.setValue('# Write your Python code here\n');
    }
}

// Clear output
function clearOutput() {
    const outputElement = document.getElementById('playground-output');
    if (outputElement) {
        outputElement.textContent = 'Output will appear here...';
        outputElement.classList.remove('error');
    }
}
