// Listener for runtime messages to manage keystroke storage
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'saveKeystroke') {
    // Retrieve saved keystrokes from storage
    chrome.storage.local.get(['keystrokes'], (result) => {
      let keystrokes = result.keystrokes || [];
      keystrokes.push(request.keystroke);

      // Save updated keystrokes to storage
      chrome.storage.local.set({ keystrokes: keystrokes }, () => {
        sendResponse({ status: 'Keystroke saved' });
      });
    });
    return true; // Indicate response will be sent asynchronously
  }
});

// Initialize the tracking process when the extension is installed
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed.');
  // Clear storage on installation for debugging purposes
  chrome.storage.local.clear();
  // Add a listener for when the user visits a new page
  chrome.history.onVisited.addListener(trackWebsite);
});

// Function to track the visited website
function trackWebsite(historyItem) {
  console.log('Visited site:', historyItem);
  // Retrieve existing history from storage
  chrome.storage.local.get({ visitedSites: [] }, (result) => {
    const visitedSites = result.visitedSites;

    // Add the new website to the history
    visitedSites.push({
      url: historyItem.url,
      title: historyItem.title,
      visitTime: new Date().toISOString()
    });

    // Save the updated history back to storage
    chrome.storage.local.set({ visitedSites: visitedSites }, () => {
      console.log('Visited sites updated:', visitedSites);
      // Send a message to the content script to update the flow chart
      chrome.runtime.sendMessage({ type: 'updateFlowChart', visitedSites: visitedSites });
    });
  });
}
