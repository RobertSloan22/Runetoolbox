// Listener for keydown events to track keystrokes
document.addEventListener('keydown', (event) => {
  const keystroke = {
    key: event.key,
    code: event.code,
    timestamp: new Date().toISOString()
  };

  // Send keystroke data to background script for saving
  chrome.runtime.sendMessage({ type: 'saveKeystroke', keystroke: keystroke });
});

// Function to monitor an element for changes
function monitorElement(selector) {
  const element = document.querySelector(selector);
  if (!element) {
    console.error('Element not found:', selector);
    return;
  }

  // Create a MutationObserver to watch for changes in the element
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList' || mutation.type === 'attributes') {
        console.log('Element has changed:', mutation);
        alert('Element has changed');
      }
    }
  });

  // Configure the observer
  observer.observe(element, {
    attributes: true,
    childList: true,
    subtree: true
  });
}

// Example usage: monitor changes in an element with ID 'targetElement'
monitorElement('#targetElement');
