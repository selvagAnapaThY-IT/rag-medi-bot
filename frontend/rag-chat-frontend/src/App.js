import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I am MediBot, your AI medical PDF assistant. Ask me any question based on your uploaded documents.",
      sources: []
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userText = input.trim();
    const userMsg = { sender: "user", text: userText };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // Determine API URL (relative '/query' when hosted in Docker/production, or explicit backend port for local dev)
      const isLocalDev = window.location.port === "3000";
      const apiUrl = isLocalDev ? "http://127.0.0.1:8000/query" : "/query";

      const res = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userText }),
      });


      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();

      const botText = data?.answer
        ? data.answer
        : data?.error
          ? `${data.error}: ${data.details || ""}`
          : "No answer returned.";

      const botSources = Array.isArray(data?.sources) ? data.sources : [];

      const botMsg = { sender: "bot", text: botText, sources: botSources };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Fetch error:", err);
      const errorMsg = {
        sender: "bot",
        text: "Error: Could not connect to backend (http://127.0.0.1:8000). Make sure FastAPI server is running.",
        sources: []
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="page">
      <header className="header">
        <h1 className="title">🩻 MediBot AI</h1>
        <p className="subtitle">Instant Intelligence from Medical & Clinical PDFs</p>
      </header>

      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, i) => (
            <div key={i} className={`msg-wrapper ${msg.sender}`}>
              <div className={`msg ${msg.sender}`}>
                <div className="msg-text">{msg.text}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="sources-container">
                    <span className="sources-label">Sources:</span>
                    {msg.sources.map((src, idx) => (
                      <span key={idx} className="source-chip">📄 {src}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="msg-wrapper bot">
              <div className="msg bot loading-dots">
                <span>.</span><span>.</span><span>.</span> Searching Medical Documents
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="input-box">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about medical documents..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

