import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

function ChatPanel() {
  const navigate = useNavigate();

  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "STRATA AI CORE ONLINE. Awaiting command.",
    },
  ]);

  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const recognitionRef = useRef(null);

  // --------------------------------
  // STRATA VOICE OUTPUT
  // --------------------------------

  const speak = (text) => {
    if (!("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const cleanText = text.replace(/\n/g, ". ");

    const speech = new SpeechSynthesisUtterance(cleanText);

    speech.rate = 0.95;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);
  };

  // --------------------------------
  // VOICE INPUT
  // --------------------------------

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Voice recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge."
      );
      return;
    }

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    // Stop STRATA from speaking while you are giving a command.
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript =
        event.results[0][0].transcript.trim();

      setIsListening(false);

      // Cancel any previous STRATA speech before processing
      // the new voice command.
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }

      processCommand(transcript);
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition error:",
        event.error
      );

      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    recognition.start();
  };

  // --------------------------------
  // LOCAL NAVIGATION COMMANDS
  // --------------------------------

  const handleNavigationCommand = (text) => {
    if (
      text === "open leads" ||
      text === "go to leads" ||
      text === "open lead generator"
    ) {
      navigate("/leads");
      return "Opening Lead Generator.";
    }

    if (
      text === "open crm" ||
      text === "go to crm"
    ) {
      navigate("/crm");
      return "Opening CRM.";
    }

    if (
      text === "open analytics" ||
      text === "go to analytics"
    ) {
      navigate("/analytics");
      return "Opening Analytics.";
    }

    if (
      text === "open websites" ||
      text === "go to websites"
    ) {
      navigate("/websites");
      return "Opening Websites.";
    }

    if (
      text === "open browser" ||
      text === "go to browser"
    ) {
      navigate("/browser");
      return "Opening Browser.";
    }

    if (
      text === "open calls" ||
      text === "go to calls"
    ) {
      navigate("/calls");
      return "Opening Calls.";
    }

    if (
      text === "open settings" ||
      text === "go to settings"
    ) {
      navigate("/settings");
      return "Opening Settings.";
    }

    return null;
  };

  // --------------------------------
  // SEND COMMAND TO STRATA AI API
  // --------------------------------

  const processCommand = async (command) => {
    const text = command
      .trim()
      .toLowerCase()
      .replace(/[.,!?]/g, "")
      .replace(/\s+/g, " ");

    if (!text || isThinking) return;

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        text,
      },
    ]);

    setInput("");

    // --------------------------------
    // LOCAL NAVIGATION
    // --------------------------------

    const navigationResponse =
      handleNavigationCommand(text.toLowerCase());

    if (navigationResponse) {
      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: navigationResponse,
        },
      ]);

      speak(navigationResponse);

      return;
    }

    // --------------------------------
    // SEND TO GEMINI BACKEND
    // --------------------------------

    setIsThinking(true);

    try {
      const response = await fetch(
        "/api/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            message: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `API returned ${response.status}`
        );
      }

      const data = await response.json();

      const aiResponse =
        data.response ||
        "STRATA received the command but returned no response.";

      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: aiResponse,
        },
      ]);

      speak(aiResponse);
    } catch (error) {
      console.error(
        "STRATA API connection error:",
        error
      );

      const errorMessage =
        "STRATA API is not connected. Make sure the STRATA API is running on port 8000.";

      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: errorMessage,
        },
      ]);

      speak(errorMessage);
    } finally {
      setIsThinking(false);
    }
  };

  // --------------------------------
  // TEXT SUBMIT
  // --------------------------------

  const handleSubmit = (event) => {
    event.preventDefault();

    processCommand(input);
  };

  // --------------------------------
  // UI
  // --------------------------------

  return (
    <div className="strata-chat">

      <div className="strata-chat-header">

        <div>

          <div className="strata-chat-title">
            STRATA AI
          </div>

          <div className="strata-chat-status">

            <span className="strata-status-dot"></span>

            {isListening
              ? "LISTENING..."
              : isThinking
              ? "THINKING..."
              : "AI CORE ONLINE"}

          </div>

        </div>

      </div>

      <div className="strata-chat-messages">

        {messages.map((message, index) => (

          <div
            key={index}
            className={`strata-message ${message.role}`}
          >

            <div className="strata-message-label">

              {message.role === "ai"
                ? "STRATA"
                : "YOU"}

            </div>

            <div className="strata-message-text">
              {message.text}
            </div>

          </div>

        ))}

      </div>

      <form
        className="strata-command-bar"
        onSubmit={handleSubmit}
      >

        <span className="command-symbol">
          &gt;
        </span>

        <input
          value={input}
          onChange={(event) =>
            setInput(event.target.value)
          }
          placeholder={
            isListening
              ? "Listening..."
              : isThinking
              ? "STRATA is thinking..."
              : "Give STRATA a command..."
          }
          disabled={isThinking}
        />

        <button
          type="button"
          onClick={startListening}
          disabled={isThinking}
          title={
            isListening
              ? "Stop listening"
              : "Talk to STRATA"
          }
          style={{
            marginRight: "8px",
            minWidth: "45px",
          }}
        >
          {isListening ? "■" : "🎤"}
        </button>

        <button
          type="submit"
          disabled={isThinking}
        >
          {isThinking ? "..." : "SEND"}
        </button>

      </form>

    </div>
  );
}

export default ChatPanel;