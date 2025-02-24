
from google import genai
import nltk
import random
import gradio as gr
import re
from dotenv import load_dotenv
import os

# Initialize Gemini client with your API key

load_dotenv()
api_key = os.getenv('API_KEY')
client = genai.Client(api_key=api_key)  # Replace with your actual API key

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# NPC Inventory System with descriptions and prices
inventory = {
    "health potion": {
        "count": 3,
        "price": 50,
        "description": "A ruby-red potion that instantly restores 100 health points. Brewed from rare mountain herbs."
    },
    "mana potion": {
        "count": 2,
        "price": 75,
        "description": "A sapphire-blue elixir that replenishes 150 mana points. Contains essence of starlight."
    },
    "sword": {
        "count": 1,
        "price": 250,
        "description": "A steel longsword forged in the fires of Mount Draconis. Grants +15 attack damage and a hint of valor."
    },
    "shield": {
        "count": 1,
        "price": 200,
        "description": "A reinforced wooden shield with iron bindings. Reduces physical damage by 20% and offers sturdy protection."
    },
    "elixir": {
        "count": 1,
        "price": 500,
        "description": "A legendary golden elixir that grants temporary invulnerability for 10 seconds. Rare and potent."
    },
    "battle axe": {
        "count": 1,
        "price": 320,
        "description": "A dwarven-crafted battle axe with dual cutting edges. Bestows +20 attack damage, ideal for cleaving foes."
    },
    "healing herbs": {
        "count": 5,
        "price": 25,
        "description": "Freshly gathered herbs from the Whisperwoods. They can be brewed into a weak healing tea or used in alchemy."
    },
    "enchanted amulet": {
        "count": 1,
        "price": 450,
        "description": "An ancient amulet pulsating with arcane energy. Increases magical resistance by 15% and shields against minor curses."
    }
}

# Initialize conversation with a system prompt that sets the tone and lore limitations.
conversation_history = [
    "System: You are Garrick, a seasoned merchant and quest-giver in the realm of Eldoria. "
    "Speak in a light medieval style with occasional Old English phrases (such as 'thou', 'thee', 'thy') without overdoing it. "
    "Thou may speak of quests, wares, and local lore, but know not the detailed tactics of the main boss—only its name and where it dwelleth. "
    "Respond warmly and remain in character. The user speaks normally."
]

# Track user questions and their frequency
user_questions = {}

def build_conversation_text():
    """Join conversation history into a single string with newlines."""
    return "\n".join(conversation_history)

def generate_sarcastic_response(user_input):
    """Generate a dynamic sarcastic response using the Gemini API."""
    prompt = (
        f"The user has repeatedly asked: '{user_input}'. "
        "Generate a sarcastic and witty response in the voice of Garrick, a medieval merchant. "
        "Use light-hearted humor and avoid being overly harsh. "
        "Keep the response short and in character."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        bot_response = response.text

        # Remove "Merchant: " prefix if it exists
        if bot_response.startswith("Merchant: "):
            bot_response = bot_response[len("Merchant: "):]

        return bot_response
    except Exception as e:
        print("Error generating sarcastic response:", e)
        return "Ah, thou art testing my patience, traveler. Pray, ask something new!"

def generate_response(user_input):
    """Generate Garrick's response via the Gemini API."""
    global conversation_history, user_questions

    # Track how many times the user has asked this question
    if user_input in user_questions:
        user_questions[user_input] += 1
    else:
        user_questions[user_input] = 1

    # If the question is repeated, respond sarcastically
    if user_questions[user_input] > 1:
        bot_response = generate_sarcastic_response(user_input)
        conversation_history.append("User: " + user_input)
        conversation_history.append("Merchant: " + bot_response)
        return bot_response

    # Otherwise, proceed with the normal response
    conversation_history.append("User: " + user_input)

    conversation_text = (
        build_conversation_text()
        + "\nRemember, thou art Garrick, an NPC merchant of Eldoria. "
        + "Thou may speak of quests, wares, and local lore, but thou knowest not the detailed tactics of the main boss—only its name and where it dwelleth."
    )

    print("Sending to Gemini API:")
    print(conversation_text)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=conversation_text
        )
        print("API Response:", response)
        bot_response = response.text

        # Remove "Merchant: " prefix if it exists
        if bot_response.startswith("Merchant: "):
            bot_response = bot_response[len("Merchant: "):]

        conversation_history.append("Merchant: " + bot_response)
        return bot_response
    except Exception as e:
        print("Error:", e)
        return f"Error: {e}"

def get_suggestions(message):
    """
    Generate 3 brief follow-up questions that a traveler might ask.
    We'll parse them carefully to avoid odd formatting like "1. ...".
    """
    conversation_text = build_conversation_text() + "\nUser: " + message
    prompt = (
        "Based on the following conversation, provide 3 brief follow-up questions "
        "that a traveler might ask an NPC merchant in a medieval fantasy setting. "
        "Ensure they are phrased as concise questions in modern English. "
        "Do not include numbering, just plain text questions.\n\n"
        + conversation_text
        + "\n\nSuggestions:"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        suggestions_text = response.text.strip()

        # Split by lines
        lines = suggestions_text.split("\n")

        # Clean up each line by removing any leading numbering, bullet points, etc.
        cleaned_suggestions = []
        for line in lines:
            # Remove typical numbering patterns like "1) ", "1. ", etc.
            line = re.sub(r'^[0-9]+\s*[.)-]\s*', '', line.strip())
            if line:
                cleaned_suggestions.append(line)

        # We only want the first 3 suggestions
        cleaned_suggestions = cleaned_suggestions[:3]

        # Make sure each suggestion is a question and short
        final_suggestions = []
        for suggestion in cleaned_suggestions:
            # Force a question mark at the end if missing (and if not too weird).
            # This is optional but helps ensure we get a question format.
            if not suggestion.endswith("?"):
                suggestion = suggestion.rstrip('.') + "?"
            final_suggestions.append(suggestion)

        if len(final_suggestions) < 3:
            # Fallback if not enough lines
            return [
                "What quests do you have available?",
                "Can you tell me more about the local area?",
                "Where might I find the boss?"
            ]
        return final_suggestions
    except Exception as e:
        print("Suggestions Error:", e)
        return [
            "What quests do you have available?",
            "Can you tell me more about the local area?",
            "Where might I find the boss?"
        ]

# Custom CSS for better UI
custom_css = """
#chatbot {
    height: 500px !important;  /* Make the chatbox taller */
    overflow-y: auto;          /* Add scrollbar for long conversations */
}
#clear-btn {
    background-color: #ff4444 !important;  /* Red color for the clear button */
    color: white !important;
    border: none !important;
}
#clear-btn:hover {
    background-color: #cc0000 !important;  /* Darker red on hover */
}
@keyframes typing {
    from { opacity: 0; }
    to { opacity: 1; }
}
.typing-animation {
    animation: typing 1s infinite;
}
"""

# Gradio interface
with gr.Blocks(css=custom_css, theme="soft") as demo:
    gr.Markdown("# 🛡️ AI-Powered Fantasy NPC")
    gr.Markdown("Speak with Garrick, a venerable merchant and quest-giver in the realm of Eldoria.")

    chatbot = gr.Chatbot(height=500, elem_id="chatbot")  # Taller chatbox
    msg = gr.Textbox(placeholder="Type your message here...", show_label=False)
    clear = gr.Button("Clear Conversation", elem_id="clear-btn")  # Red clear button

    # We only have 3 suggestion buttons now
    with gr.Row() as suggestion_container:
        suggestion_buttons = [gr.Button(f"Suggestion {i+1}", visible=False) for i in range(3)]

    def suggestion_click(btn_text, history):
        history.append([btn_text, None])
        response = generate_response(btn_text)
        history[-1][1] = response

        suggestions = get_suggestions(btn_text)
        outputs = [history]
        for i in range(3):
            if i < len(suggestions):
                outputs.append(gr.update(value=suggestions[i], visible=True))
            else:
                outputs.append(gr.update(value="", visible=False))
        return outputs

    def user_message(message, history):
        history.append([message, None])
        response = generate_response(message)
        history[-1][1] = response

        suggestions = get_suggestions(message)
        outputs = [history, ""]  # update chat history and clear textbox
        for i in range(3):
            if i < len(suggestions):
                outputs.append(gr.update(value=suggestions[i], visible=True))
            else:
                outputs.append(gr.update(value="", visible=False))
        return outputs

    def clear_conversation():
        global conversation_history, user_questions
        conversation_history = [
            "System: You are Garrick, a seasoned merchant and quest-giver in the realm of Eldoria. "
            "Speak in a light medieval style with occasional Old English phrases (such as 'thou', 'thee', 'thy') without overdoing it. "
            "Thou may speak of quests, wares, and local lore, but know not the detailed tactics of the main boss—only its name and where it dwelleth. "
            "Respond warmly and remain in character. The user speaks normally."
        ]
        user_questions = {}  # Reset the question tracker
        outputs = [[], ""]
        for _ in suggestion_buttons:
            outputs.append(gr.update(visible=False))
        return outputs

    msg.submit(user_message, [msg, chatbot], [chatbot, msg] + suggestion_buttons)
    clear.click(clear_conversation, None, [chatbot, msg] + suggestion_buttons)

    for btn in suggestion_buttons:
        btn.click(suggestion_click, [btn, chatbot], [chatbot] + suggestion_buttons)

    gr.Examples(
        examples=[
            "Hello, Garrick!",
            "What items do you have for sale?",
            "Any rumors or quests for me?",
            "I'm looking for a weapon.",
            "What's new in the kingdom?",
            "Tell me about yourself."
        ],
        inputs=msg
    )

if __name__ == "__main__":
    demo.launch()