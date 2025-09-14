// Listen for message from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "detectComments") {
    const selectedText = window.getSelection().toString().trim();

    if (!selectedText) {
      alert("⚠️ Please select a comment before clicking the extension.");
      sendResponse({ status: "No text selected" });
      return;
    }

    classifySelectedText(selectedText);
    sendResponse({ status: "Classification started" });
  }
});

// Call API and highlight selected text
async function classifySelectedText(text) {
  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) return;

    const data = await response.json();
    const prediction = data.prediction;
    const confidence = data.confidence ?? 0;

    const span = document.createElement("span");
    span.textContent = text;
    span.style.backgroundColor = prediction === "AI" ? "#ffdddd" : "#ddffdd";
    span.title = `${prediction} (Confidence: ${confidence.toFixed(2)}%)`;
    span.style.borderRadius = "4px";
    span.style.padding = "2px 4px";
    span.style.fontWeight = "bold";

    const range = window.getSelection().getRangeAt(0);
    range.deleteContents();
    range.insertNode(span);

    chrome.storage.local.set({
      lastPrediction: prediction,
      lastConfidence: confidence,
      aiPercentage: prediction === "AI" ? 100 : 0
    });

  } catch (err) {
    console.error("❌ API error:", err);
  }
}
