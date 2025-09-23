// Macro recording system
let macroRecording = false;
let macroActions = [];

window.startMacroRecording = function() {
    macroRecording = true;
    macroActions = [];
    alert('Macro recording started.');
};

window.stopMacroRecording = function() {
    macroRecording = false;
    alert('Macro recording stopped.');
};

window.playMacro = function() {
    for (const action of macroActions) {
        setTimeout(() => window.performAgentAction(action), 500);
    }
};

// Patch performAgentAction to record actions
const origPerformAgentAction = window.performAgentAction;
window.performAgentAction = function(actionString) {
    if (macroRecording) macroActions.push(actionString);
    origPerformAgentAction(actionString);
};

// main.js - Agent overlay and screen interaction logic
let agentMode = false;
let lastHighlighted = null;

function enableAgentMode() {
    agentMode = true;
    document.body.style.cursor = 'crosshair';
    document.addEventListener('mouseover', highlightElement);
    document.addEventListener('mouseout', unhighlightElement);
    document.addEventListener('click', agentClickHandler, true);
}

function disableAgentMode() {
    agentMode = false;
    document.body.style.cursor = '';
    if (lastHighlighted) lastHighlighted.style.outline = '';
    document.removeEventListener('mouseover', highlightElement);
    document.removeEventListener('mouseout', unhighlightElement);
    document.removeEventListener('click', agentClickHandler, true);
}

function highlightElement(e) {
    if (!agentMode) return;
    if (lastHighlighted) lastHighlighted.style.outline = '';
    lastHighlighted = e.target;
    lastHighlighted.style.outline = '2px solid #ff0066';
}

function unhighlightElement(e) {
    if (!agentMode) return;
    e.target.style.outline = '';
}

function agentClickHandler(e) {
    if (!agentMode) return;
    e.preventDefault();
    e.stopPropagation();
    const selector = getUniqueSelector(e.target);
    window.prompt('Element selector for agent:', selector);
    // Optionally, send selector to backend or agent for action
    disableAgentMode();
}

// Utility: get a unique selector for an element
function getUniqueSelector(el) {
    if (el.id) return `#${el.id}`;
    let path = [];
    while (el && el.nodeType === 1 && el !== document.body) {
        let selector = el.nodeName.toLowerCase();
        if (el.className) selector += '.' + el.className.trim().replace(/\s+/g, '.');
        path.unshift(selector);
        el = el.parentNode;
    }
    return path.join(' > ');
}

// Expose agent mode toggle for chat integration
window.enableAgentMode = enableAgentMode;
window.disableAgentMode = disableAgentMode;

// Listen for ACTION: CLICK <selector> from assistant and perform the click
window.performAgentAction = function(actionString) {
    // Example: ACTION: CLICK #myButton
    if (!actionString.startsWith('ACTION:')) return;
    const parts = actionString.split(' ');
    const action = parts[1];
    if (action === 'CLICK' && parts[2]) {
        const selector = parts.slice(2).join(' ');
        try {
            const el = document.querySelector(selector);
            if (el) {
                el.click();
                alert('Agent clicked: ' + selector);
            } else {
                alert('Agent could not find: ' + selector);
            }
        } catch (e) {
            alert('Agent error: ' + e);
        }
    } else if (action === 'TYPE' && parts[2] && parts[3]) {
        // TYPE <selector> <text>
        const selector = parts[2];
        const text = parts.slice(3).join(' ');
        try {
            const el = document.querySelector(selector);
            if (el) {
                el.value = text;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                alert('Agent typed in ' + selector + ': ' + text);
            } else {
                alert('Agent could not find: ' + selector);
            }
        } catch (e) {
            alert('Agent error: ' + e);
        }
    } else if (action === 'SCROLL' && parts[2]) {
        // SCROLL <direction>
        const direction = parts[2].toLowerCase();
        if (direction === 'down') window.scrollBy(0, 200);
        else if (direction === 'up') window.scrollBy(0, -200);
        else if (direction === 'left') window.scrollBy(-200, 0);
        else if (direction === 'right') window.scrollBy(200, 0);
        alert('Agent scrolled ' + direction);
    } else if (action === 'OPEN' && parts[2]) {
        // OPEN <url>
        const url = parts.slice(2).join(' ');
        window.open(url, '_blank');
        alert('Agent opened: ' + url);
    } else if (action === 'HIGHLIGHT' && parts[2]) {
        // HIGHLIGHT <selector>
        const selector = parts.slice(2).join(' ');
        try {
            const el = document.querySelector(selector);
            if (el) {
                el.style.background = '#fffa8b';
                el.style.transition = 'background 0.5s';
                alert('Agent highlighted: ' + selector);
            } else {
                alert('Agent could not find: ' + selector);
            }
        } catch (e) {
            alert('Agent error: ' + e);
        }
    }
};
