import React, { useEffect, useRef, useState } from "react";
import { w3cwebsocket as W3CWebSocket } from "websocket";

const WebSocketClient: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [filter, setFilter] = useState<string | null>(null); // État pour stocker le type d'erreur sélectionné
  const socketRef = useRef<W3CWebSocket | null>(null);

  useEffect(() => {
    // Create a new websocket connection
    socketRef.current = new W3CWebSocket("ws://localhost:8081/ws");

    // Listen for messages from the server
    socketRef.current.onmessage = (event) => {
      const message = event.data.toString();
      if (!filter || message.includes(filter)) {
        setMessages((prevMessage) => [...prevMessage, message]);
      }
    };

    // Handle websocket connection errors
    socketRef.current.onerror = (error) => {
      console.error("WebSocket connection error:", error);
    };

    // Clean up the websocket connection on component unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [filter]);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <h1>WebSocket Client React</h1>
      <div style={{ marginBottom: "10px" }}>
        <button onClick={() => setFilter(null)}>Tous</button>
        <button onClick={() => setFilter("KeyError")}>KeyError</button>
        <button onClick={() => setFilter("IndexError")}>IndexError</button>
        <button onClick={() => setFilter("TypeError")}>TypeError</button>
        <button onClick={() => setFilter("ValueError")}>ValueError</button>
      </div>
      {messages.map((message, index) => (
        <div key={index} style={{ marginBottom: "5px" }}>
          {message}
        </div>
      ))}
    </div>
  );
};

export default WebSocketClient;
