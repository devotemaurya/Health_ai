document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");

    input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const userInput = input.value.trim();
            if (userInput) {
                addMessage("You", userInput);
                const reply = getBotReply(userInput);
                addMessage("Bot", reply);
                input.value = "";
            }
        }
    });

    function addMessage(sender, message) {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${sender}:</strong> ${message}`;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function getBotReply(input) {
        const lower = input.toLowerCase();
        if (lower.includes("fever")) return "Drink fluids, take rest, and monitor your temperature. You might have a viral infection.";
        if (lower.includes("headache")) return "It might be due to stress or dehydration. Drink water and take rest.";
        if (lower.includes("stomach")) return "Consider light meals and stay hydrated. Avoid spicy food.";
        return "Sorry, I can't identify that symptom yet. Try checking the symptom checker.";
    }
});
