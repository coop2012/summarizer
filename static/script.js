document.getElementById("summarizeBtn").addEventListener("click", async () => {
  const notes = document.getElementById("notes").value.trim();
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");

  if (!notes) {
    resultDiv.textContent = "⚠️ Please enter some text to summarize.";
    return;
  }

  resultDiv.textContent = "";
  loadingDiv.style.display = "block";

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ notes }),
    });

    const data = await response.json();
    loadingDiv.style.display = "none";

    if (data.summary) {
      resultDiv.textContent = data.summary;
    } else {
      resultDiv.textContent = "❌ Error: " + (data.error || "Unknown issue");
    }
  } catch (err) {
    loadingDiv.style.display = "none";
    resultDiv.textContent = "🚨 Failed to connect to backend.";
  }
});
