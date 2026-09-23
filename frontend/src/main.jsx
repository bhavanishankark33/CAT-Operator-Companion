import React from "react";
import { createRoot } from "react-dom/client";

function App() {
  return (
    <main style={{fontFamily: "sans-serif", padding: 32}}>
      <h1>CAT Operator Companion</h1>
      <p>Fresh project shell — ready for the team to build.</p>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
