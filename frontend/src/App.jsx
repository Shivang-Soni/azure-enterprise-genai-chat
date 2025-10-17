import React from "react";
import ChatBot from "./ChatBot";

function App() {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        backgroundImage: "url('/background.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <h1
        style={{
          color: "black",
          textShadow: "1px 1px 4px rgba(0,0,0,0.7)",
          fontSize: "2rem",
          marginBottom: "20px",
        }}
      >
        Azure Generative KI Assistent
      </h1>
      <div style={{ width: "400px", flex: 1 }}>
        <ChatBot />
      </div>
    </div>
  );
}

export default App;
