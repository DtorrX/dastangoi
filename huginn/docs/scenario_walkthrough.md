# Huginn Scenario Walkthrough

This scenario follows a strict **signals-only** workflow:
1. **Sources** pull from permissive RSS/Atom and public APIs.
2. **Normalize** to a canonical schema.
3. **Deduplicate** on canonical URL + normalized title.
4. **Enrich** with lightweight keyword extraction.
5. **Classify** via LLM (BYO key) with strict schema.
6. **Coordination heuristics** score burstiness and repetition.
7. **Alert** only high-signal items to the reporter service.
8. **Daily trigger** rolls up the previous day’s window.

Review `huginn/templates/` for JavaScript templates used in agents.
