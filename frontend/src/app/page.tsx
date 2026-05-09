"use client"

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from 'remark-gfm';
import rehypeRaw from "rehype-raw";

interface Message {
  role: "USER" | "SYSTEM";
  message: string;
}

export default function home() {
  const SESSION_KEY = 'session_id'
  function getSessionId() {
    if (!localStorage.getItem(SESSION_KEY)) {
      localStorage.setItem(SESSION_KEY, crypto.randomUUID())
    }

    return localStorage.getItem(SESSION_KEY)
  }

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  function onSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoading(true)
    const form = event.currentTarget;

    const formData = new FormData(form);
    const query = formData.get("query") as string;
    setMessages(prevMessage => [...prevMessage, {
      role: 'USER',
      message: query
    }])
    getResult(query);
  }

  async function getResult(query: string) {
    const response = await fetch(`http://localhost:8000`, {
      method: "POST",
      body: JSON.stringify({ message: query, session_id: getSessionId() }),
      headers: {
        'content-type': "application/json"
      }
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder();

    setMessages(prevMessage => [...prevMessage, {
      role: 'SYSTEM',
      message: ""
    }])

    if (!reader) return;
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value)
      setMessages(prevMessage => {
        const updated = [...prevMessage];

        const lastIndex = updated.length - 1;
        const lastMessage = updated[lastIndex];

        updated[lastIndex] = {
          ...lastMessage,
          message: lastMessage.message + chunk
        };

        return updated;
      })
    }

    setLoading(false)
  }

  return <main>
    <header className="chat-header">
      <h2 className="text-center">Chat app</h2>
      <form onSubmit={onSubmit}>
        <div className="chat-container">
          <div className="textarea-wrapper">
            <textarea
              className="chatgpt-textarea"
              placeholder="Message ChatGPT..."
              rows={1}
              name="query"
              disabled={loading}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();

                  e.currentTarget.form?.requestSubmit();
                }
              }}
            />
          </div>
        </div>
      </form>

      {/* <hr color="black" style={{ width: "100%" }} /> */}
    </header>
    {messages.length > 0 && (
      <div className="chat-wrapper">
        {messages.map(({ role, message }, index) => (
          <div
            key={index}
            className={`message ${role === "USER"
                ? "user-message"
                : "system-message"
              }`}
          >
            {role === "SYSTEM" ? (
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
              >
                {message}
              </ReactMarkdown>
            ) : (
              message
            )}
          </div>
        ))}
      </div>
    )}
  </main>
}