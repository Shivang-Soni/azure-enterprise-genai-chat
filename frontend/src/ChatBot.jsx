import React, { useState, useRef, useEffect } from "react";

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Automatisches Scrollen
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const API_URL =
    process.env.REACT_APP_API_URL || "http://localhost:8000/api/chat";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: "user1", question: input }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { sender: "bot", text: data.answer }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Fehler beim Senden." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "500px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "10px",
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          marginBottom: "10px",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              padding: "8px",
              borderRadius: "8px",
              margin: "4px 0",
              textAlign: msg.sender === "user" ? "right" : "left",
              backgroundColor: msg.sender === "user" ? "#bfdbfe" : "#e5e7eb",
              color: "#1f2937",
            }}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div style={{ color: "#4b5563", fontStyle: "italic" }}>Bot denkt…</div>
        )}
        <div ref={messagesEndRef}></div>
      </div>

      <div style={{ display: "flex" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Nachricht eingeben..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: 1,
            padding: "8px",
            borderRadius: "8px 0 0 8px",
            border: "1px solid #ccc",
            outline: "none",
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            padding: "8px 12px",
            borderRadius: "0 8px 8px 0",
            border: "none",
            backgroundColor: "#3b82f6",
            color: "white",
            cursor: "pointer",
          }}
        >
          Senden
        </button>
      </div>
    </div>
  );
}
