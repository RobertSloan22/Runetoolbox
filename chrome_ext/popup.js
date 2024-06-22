// Display the flow chart of tracked activities in the popup
document.addEventListener('DOMContentLoaded', () => {
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'updateFlowChart') {
      updateFlowChart(request.visitedSites);
    }
  });

  chrome.storage.local.get({ visitedSites: [] }, (result) => {
    updateFlowChart(result.visitedSites);
  });
});

// Function to update the flow chart with the latest visited sites
function updateFlowChart(visitedSites) {
  const flowChart = document.getElementById('flowChart');
  flowChart.innerHTML = ''; // Clear the chart

  visitedSites.forEach((site, index) => {
    const node = document.createElement('div');
    node.className = 'node';
    node.textContent = index + 1;
    node.title = `Title: ${site.title}\nURL: ${site.url}\nVisit Time: ${site.visitTime}`;
    node.addEventListener('click', () => {
      alert(JSON.stringify(site, null, 2));
    });

    flowChart.appendChild(node);

    if (index < visitedSites.length - 1) {
      const line = document.createElement('div');
      line.className = 'line';
      flowChart.appendChild(line);
    }
  });
}
