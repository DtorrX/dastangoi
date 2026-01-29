// Enrichment step: basic keyword extraction and n-grams for signals.
// Keep it conservative: avoid inventing facts or entities.

function tokenize(text) {
  return (text || "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter(Boolean);
}

Agent.receive = function() {
  this.incomingEvents().forEach((event) => {
    const text = event.payload.text || "";
    const tokens = tokenize(text);
    const keywords = Array.from(new Set(tokens)).slice(0, 20);
    const bigrams = [];

    for (let i = 0; i < tokens.length - 1; i += 1) {
      bigrams.push(`${tokens[i]} ${tokens[i + 1]}`);
    }

    this.createEvent({
      payload: {
        ...event.payload,
        keywords,
        bigrams: bigrams.slice(0, 20)
      }
    });
  });
};
