// Normalize incoming events into a strict schema for downstream processing.
// NOTE: This is a template. Use only permissive sources and cite original URLs.

Agent.receive = function() {
  this.incomingEvents().forEach((event) => {
    const payload = event.payload || {};
    const title = payload.title || payload.name || "";
    const url = payload.url || payload.link || "";
    const text = payload.content || payload.summary || payload.description || "";
    const published = payload.published_at || payload.published || payload.date || new Date().toISOString();

    const normalized = {
      source: payload.source || payload.feed || "unknown",
      url,
      title,
      published_at: published,
      text,
      language: payload.language || "unknown",
      entities: payload.entities || [],
      hashtags: payload.hashtags || [],
      accounts: payload.accounts || [],
      media_urls: payload.media_urls || []
    };

    const dedupeHash = [normalized.url, normalized.title].join("|").toLowerCase();

    this.createEvent({
      payload: {
        ...normalized,
        dedupe_hash: dedupeHash
      }
    });
  });
};
