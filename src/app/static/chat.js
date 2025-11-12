const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  addMessage("Tú", message);
  userInput.value = "";

  try {
    const reply = await queryTuServidor(message);
    addMessage("Gemini", reply);
  } catch (error) {
    addMessage("Sistema", "Error al obtener respuesta del bot.");
    console.error(error);
  }
});

function addMessage(sender, text) {
  const message = document.createElement("div");
  message.classList.add("message");

  if (sender === "Tú") {
    message.classList.add("user");
  } else {
    message.classList.add("bot");
  }

  message.textContent = text;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function queryTuServidor(promptText) {
  const url = "http://127.0.0.1:5000/chat_inmobiliario"; 

  const body = {
    mensaje: promptText
  };

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.json();
    console.error("Error en la respuesta de tu servidor:", error);
    throw new Error(error.respuesta);
  }

  const data = await res.json();
  return data.respuesta || "No entendí eso.";
}
