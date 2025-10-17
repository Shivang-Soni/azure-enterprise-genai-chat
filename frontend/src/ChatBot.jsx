import React, { useState, useRef, useEffect } from "react";

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(""); // String statt Array
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Automatisches Scrollen nach unten
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  // Dynamische API-URL
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/chat";

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
        body: JSON.stringify({ user_id: "anon", question: input }), // angepasst
      });
      const data = await res.json();
      setMessages([...newMessages, { sender: "bot", text: data.answer }]); // angepasst
    } catch (err) {
      setMessages([...newMessages, { sender: "bot", text: "Fehler beim Senden." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto border rounded shadow p-4 flex flex-col h-[500px]">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded my-1 ${
              msg.sender === "user" ? "bg-blue-100 text-right" : "bg-gray-200 text-left"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="text-gray-500">Bot denkt…</div>}
        <div ref={messagesEndRef}></div>
      </div>

      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border p-2 rounded-l"
          placeholder="Nachricht eingeben..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white p-2 rounded-r hover:bg-blue-600 disabled:opacity-50"
          disabled={loading}
        >
          Abschicken
        </button>
      </div>
    </div>
  );
}
