const express = require("express");

const app = express();
const port = process.env.PORT || 8010;

app.get("/health", (_req, res) => {
  res.json({ status: "ok", time: new Date().toISOString() });
});

app.get("/", (_req, res) => {
  res.send("<h1>Admin UI (placeholder)</h1><p>Manage sources and subscribers.</p>");
});

app.listen(port, () => {
  console.log(`Admin UI listening on ${port}`);
});
