import "./index.css";
import React from "react";
import ReactDOM from "react-dom/client";

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <h1 className="text-4xl font-bold text-blue-600">
        Hello Tailwind + React!
      </h1>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
