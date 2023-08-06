$(document).ready(function() {
    setTimeout(function() {
        $('.flashed-messages').fadeOut('slow');
    }, 3000);
});

window.onload = () => {
    const chatGptTextArea = document.getElementById('chatGptTextArea');
    const chatGptSubmitBtn = document.getElementById('chatGptSubmitBtn');
    const loaderOverlay = document.getElementById('loader-overlay');

    chatGptSubmitBtn.addEventListener('click', function() {
        if (chatGptTextArea.value.trim() !== "") {
            console.log('loader overlay');
            loaderOverlay.style.display = "flex";
        }
    });
};

window.addEventListener('pageshow', (event) => {
    // If the page was loaded from the cache
    if (event.persisted) {
        // Hide the loader
        document.getElementById('loader-overlay').style.display = 'none';
    }
});

function updateButtonState() {
    const userInput = document.getElementById("userInput").value;
    const conversation = document.querySelector(".conversation");
    const sendButton = document.getElementById("sendBtn");
    const clearButton = document.getElementById("clearBtn");

    // Disable the Send button if the input is empty
    sendButton.disabled = userInput.trim() === "";

    // Disable the Clear Conversation button if the conversation is empty
    clearButton.disabled = conversation.innerHTML.trim() === "";
}

document.getElementById("sendBtn").addEventListener("click", function() {
    const sendButton = document.getElementById("sendBtn");
    const originalButtonText = sendButton.textContent;
    const userInput = document.getElementById("userInput").value;

    // Show loading text
    sendButton.textContent = "Loading...";
    sendButton.disabled = true;

    fetch('/task/gpt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({prompt: userInput})
    })
    .then(response => response.json())
    .then(data => {
        // Create a container for the user's question and the AI's answer
        const qaContainer = document.createElement("div");
        qaContainer.className = "qa-container";

        // Create and append the user's question
        const userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.innerHTML = "<strong>User: " + userInput + "</strong>";
        qaContainer.appendChild(userMessage);

        // Create and append the AI's answer
        const aiMessage = document.createElement("div");
        aiMessage.className = "assistant-message";
        aiMessage.innerHTML = "<strong>AI:</strong> " + data.response;
        qaContainer.appendChild(aiMessage);

        // Append the container to the conversation
        document.querySelector(".conversation").appendChild(qaContainer);

        // Restore button text
        sendButton.textContent = originalButtonText;
        sendButton.disabled = false;

        // Clear the user input
        document.getElementById("userInput").value = '';

        // Update button state
        updateButtonState();
    })
    .catch(error => {
        console.error('Error:', error);
        // Restore button text in case of error
        sendButton.textContent = originalButtonText;
        sendButton.disabled = false;
    });
});

document.getElementById("clearBtn").addEventListener("click", function() {
    // Display a confirmation dialog
    if (window.confirm("Are you sure you want to clear the conversation?")) {
        // Clear the conversation in the browser
        document.querySelector(".conversation").innerHTML = '';

        // Optionally, you can send a request to the server to clear the conversation in the session
        fetch('/task/clear_conversation', {
            method: 'POST',
        })
        .then(() => {
            console.log('Conversation cleared on the server.');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Update button state
    updateButtonState();
});

document.getElementById("userInput").addEventListener("input", function() {
    // Update button state whenever the user types something
    updateButtonState();
});

// Update button state when the page loads
updateButtonState();
