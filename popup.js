document.addEventListener("DOMContentLoaded", () => {
  const checkButton = document.getElementById("checkBtn");

  checkButton.addEventListener("click", async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      // Inject content.js if not already injected
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
      }, () => {
        if (chrome.runtime.lastError) {
          console.error("❌ Injection failed:", chrome.runtime.lastError.message);
          alert("⚠️ Could not inject script. Try refreshing the page.");
          return;
        }

        // Now try sending the message
        chrome.tabs.sendMessage(tab.id, { action: "detectComments" }, (response) => {
          if (chrome.runtime.lastError) {
            console.error("❌ Could not connect to content script:", chrome.runtime.lastError.message);
            alert("⚠️ Content script not running on this page. Try refreshing.");
          } else {
            console.log("✅ Triggered comment detection:", response);
          }
        });
      });

    } catch (err) {
      console.error("❌ Unexpected error:", err);
      alert("Something went wrong. Try again.");
    }
  });

  // Load previous prediction data
  if (typeof chrome !== "undefined" && chrome.storage?.local) {
    chrome.storage.local.get(
      ["aiPercentage", "lastPrediction", "lastConfidence", "commentSelector"],
      (data) => {
        document.getElementById("ai-stats").innerHTML =
          `📊 AI-generated comments: <strong>${data.aiPercentage ?? "N/A"}%</strong>`;

        document.getElementById("result-label").innerHTML =
          `✅ Result: <strong>${data.lastPrediction ?? "Not available"}</strong>`;

        document.getElementById("confidence").innerHTML =
          `🔬 Confidence: <strong>${data.lastConfidence ? data.lastConfidence.toFixed(2) + "%" : "N/A"}</strong>`;

        document.getElementById("selector").textContent =
          data.commentSelector ?? "Auto";
      }
    );
  } else {
    console.error("❌ chrome.storage.local not available.");
  }
});
