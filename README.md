
# NPC Dialogue - AI-Powered Fantasy NPC

## Overview

**NPC Dialogue** is an interactive AI-powered chatbot that simulates a conversation with Garrick, a seasoned merchant and quest-giver in the fantasy realm of Eldoria. The project leverages the Gemini API for natural language processing and Gradio for a user-friendly web interface. Garrick responds to user queries in a light medieval style, offering information about quests, wares, and local lore.

## Features

- **Interactive Chat Interface**: Engage in a dynamic conversation with Garrick, who responds in a medieval tone with occasional Old English phrases.
- **Inventory System**: Garrick has a detailed inventory of items, each with descriptions and prices, which he can discuss with the user.
- **Sarcastic Responses**: If the user repeats a question, Garrick responds with a witty and sarcastic remark.
- **Follow-up Suggestions**: The system generates three follow-up questions based on the conversation to keep the dialogue flowing.
- **Customizable UI**: The Gradio interface is styled with custom CSS for an immersive experience.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/NPC-Dialogue.git
   cd NPC-Dialogue
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Gemini API key to the `.env` file:
     ```plaintext
     API_KEY=your_api_key_here
     ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Web Interface**:
   - Open your web browser and navigate to `http://localhost:7860`.

## Usage

- **Start a Conversation**: Type your message in the textbox and press Enter to send it to Garrick.
- **Follow-up Questions**: The system will suggest three follow-up questions based on the conversation. Click on any suggestion to continue the dialogue.
- **Clear Conversation**: Use the "Clear Conversation" button to reset the chat and start fresh.

## Example Queries

- "Hello, Garrick!"
- "What items do you have for sale?"
- "Any rumors or quests for me?"
- "I'm looking for a weapon."
- "What's new in the kingdom?"
- "Tell me about yourself."

## Dependencies

- **Gradio**: For building the web interface.
- **Google Generative AI**: For generating responses using the Gemini API.
- **NLTK**: For natural language processing tasks.
- **Python-dotenv**: For managing environment variables.

## File Structure

- **app.py**: The main application script containing the chatbot logic and Gradio interface.
- **requirements.txt**: Lists all the Python dependencies required to run the project.
- **.env**: Stores the Gemini API key and other environment variables.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Gemini API**: For providing the natural language processing capabilities.
- **Gradio**: For the easy-to-use web interface framework.
- **NLTK**: For natural language processing support.

## Contact

For any questions or feedback, please open an issue on the GitHub repository or contact the project maintainer.
