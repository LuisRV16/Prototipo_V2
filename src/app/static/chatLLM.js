document.addEventListener("DOMContentLoaded", () => {
  
  const form = document.querySelector(".chat-form");   
  const input = document.querySelector(".user-input");
  const messages = document.querySelector(".chat-box");
  const fileInput = document.getElementById("file-input"); 

  const documentUploadInput = document.getElementById('document-upload-input');


  // Lógica de envío de MENSAJES DE TEXTO
  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const userText = input.value.trim();
    if (!userText) return; 

    const userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.innerText = userText;
    messages.appendChild(userMsg);

    const typingMsg = document.createElement("div");
    typingMsg.className = "message bot";
    typingMsg.innerText = "...";
    messages.appendChild(typingMsg);

    input.value = ""; 
    messages.scrollTop = messages.scrollHeight;

    try {
      // Este fetch va al endpoint /chat
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensaje: userText })
      });

      const data = await response.json();
      messages.removeChild(typingMsg); 

      const botMsg = document.createElement("div");
      botMsg.className = "message bot";
      botMsg.innerText = data.respuesta;
      messages.appendChild(botMsg);

    } catch (error) {
      console.error("Error al conectar con el servidor:", error);
      messages.removeChild(typingMsg);
      const errorMsg = document.createElement("div");
      errorMsg.className = "message bot";
      errorMsg.innerText = "Error al conectar con el servidor.";
      messages.appendChild(errorMsg);
    }

    messages.scrollTop = messages.scrollHeight;
  });

  fileInput.addEventListener("change", async () => {
    const files = fileInput.files;
    if (!files.length) return;

    // 1. Crear UNA sola instancia de FormData
    const formData = new FormData();
    const fileNames = [];

    // 2. Agregar TODOS los archivos al FormData
    for (let file of files) {
      formData.append("file", file);
      fileNames.push(file.name);
    }

    // 3. Mostrar un solo mensaje de usuario con todos los archivos
    const fileMsg = document.createElement("div");
    fileMsg.className = "message user";
    fileMsg.innerText = `Archivos seleccionados:\n${fileNames.join('\n')}`;
    messages.appendChild(fileMsg);

    // 4. Mostrar un solo mensaje de "subiendo..."
    const uploadingMsg = document.createElement("div");
    uploadingMsg.className = "message bot";
    uploadingMsg.innerText = `Subiendo ${files.length} archivo(s)...`;
    messages.appendChild(uploadingMsg);
    messages.scrollTop = messages.scrollHeight;

    try {
      // 5. Enviar UN SOLO request al endpoint de subida
      const response = await fetch("http://127.0.0.1:5000/upload_to_chat", {
        method: "POST",
        body: formData 
      });

      // 6. Procesar la respuesta única
      const data = await response.json();

      messages.removeChild(uploadingMsg);
      const botMsg = document.createElement("div");
      botMsg.className = "message bot";
      botMsg.innerText = data.respuesta || "Archivos recibidos";
      messages.appendChild(botMsg);

    } catch (error) {
      console.error("Error al subir archivos:", error);
      messages.removeChild(uploadingMsg);
      const errorMsg = document.createElement("div");
      errorMsg.className = "message bot";
      errorMsg.innerText = "Error al subir los archivos.";
      messages.appendChild(errorMsg);
    }

    messages.scrollTop = messages.scrollHeight; 
    fileInput.value = ""; // Limpiar el input
  });

  // Inyectar CSS para la notificación (en lugar de alert())
  const style = document.createElement('style');
  style.innerHTML = `
    .custom-notification {
      position: fixed;
      top: 20px;
      right: 20px;
      background-color: #333;
      color: white;
      padding: 16px;
      border-radius: 8px;
      z-index: 1001;
      opacity: 0;
      transition: opacity 0.5s, top 0.5s;
      font-family: Arial, sans-serif;
      font-size: 14px;
      white-space: pre-wrap; /* Para respetar los saltos de línea \n */
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      max-width: 300px;
    }
    .custom-notification.show {
      opacity: 1;
      top: 30px;
    }
  `;
  document.head.appendChild(style);

  function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'custom-notification';
    notification.innerText = message;
    document.body.appendChild(notification);

    // Forzar reflow para que la transición funcione
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);

    // Ocultar y eliminar después de 4 segundos
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification);
        }
      }, 500); // Esperar que termine la transición de salida
    }, 4000);
  }

  // Event Listener para el input de "Cargar Datos"
  documentUploadInput.addEventListener('change', async () => {
    const files = documentUploadInput.files;
    if (!files.length) return;

    const formData = new FormData();
    const fileNames = [];

    for (let file of files) {
      formData.append("file", file);
      fileNames.push(file.name);
    }

    showNotification(`Archivos seleccionados:\n${fileNames.join('\n')}`);
    
    // Limpiar el input
    documentUploadInput.value = "";
    
    try {
      // Mostrar notificación de subida
      showNotification(`Subiendo ${files.length} archivo(s)...`);

      // 5. Enviar UN SOLO request al endpoint de subida
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData 
      });

      // 6. Procesar la respuesta única
      const data = await response.json();

      // Mostrar notificación de éxito
      showNotification(data.respuesta || "Archivos recibidos");

    } catch (error) {
      console.error("Error al subir archivos:", error);
      // Mostrar notificación de error
      showNotification("Error al subir los archivos.");
    }
  });

  // Obtener los enlaces
  const linkLoadData = document.getElementById('link-load-data');
  const linkClients = document.getElementById('link-clients');
  
  // Obtener las vistas
  const viewLoadData = document.getElementById('load-data-view');
  const viewClients = document.getElementById('clients-view');

  // Función para cambiar de vista
  function showView(viewToShow, linkToActivate) {
    // Ocultar todas las vistas
    viewLoadData.classList.remove('active');
    viewClients.classList.remove('active');
    
    // Quitar 'active' de todos los enlaces
    linkLoadData.classList.remove('active');
    linkClients.classList.remove('active');
    
    // Mostrar la vista seleccionada
    viewToShow.classList.add('active');
    linkToActivate.classList.add('active');
  }

  // Asignar eventos de clic
  linkLoadData.addEventListener('click', function(e) {
    e.preventDefault(); // Evitar que el enlace '#' recargue la página
    showView(viewLoadData, linkLoadData);
  });
  
  linkClients.addEventListener('click', function(e) {
    e.preventDefault();
    showView(viewClients, linkClients);
  });

});

