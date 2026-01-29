// Coordination + narrative scoring (lightweight heuristics).
// This template is intentionally conservative; it only emits signals.

function scoreSignal(payload) {
  const repetition = (payload.repetition_score || 0);
  const burst = (payload.burst_score || 0);
  const linkCluster = (payload.link_cluster_score || 0);
  return Math.min(1, (repetition + burst + linkCluster) / 3);
}

Agent.receive = function() {
  this.incomingEvents().forEach((event) => {
    const signalScore = scoreSignal(event.payload);

    this.createEvent({
      payload: {
        ...event.payload,
        signal_score: signalScore,
        signal_label: signalScore >= 0.7 ? "high" : "medium"
      }
    });
  });
};
