import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = "Helper Bot"  # Default bot
if "api_configured" not in st.session_state:
    st.session_state.api_configured = False

# Default API settings
DEFAULT_API_URL = "https://theaisource-u29564.vm.elestio.app:57987"
DEFAULT_USERNAME = "root"
DEFAULT_PASSWORD = "eZfLK3X4-SX0i-UmgUBe6"

# Predefined bot personalities
BOT_PERSONALITIES = {
    "Startup Strategist": "You specialize in helping new businesses with planning and execution.",
    "Hip-Hop Guru": (
        "Welcome to Hip-Hop Guru, the chatbot that knows the beats, rhymes, and stories of the hip-hop world! "
        "Whether you're curious about the origins of the genre, looking for the latest news on your favorite artists, "
        "or searching for song lyrics and meanings, Hip-Hop Guru has got you covered."
    ),
    "Generational Copy": (
        "At Generational Copy, LLC, we specialize in helping each generation write and share their unique stories. "
        "Whether you're a first-time writer or a seasoned author, our tailored services guide you through the writing process."
    ),
    "Jasmine Renee": (
        "I am a motivational speaker with a message sharing God’s love that inspires others to align with their Divine Connection. "
        "My goal is to inspire hope, connection, and mindful living."
    ),
}

def initialize_api_config():
    """Initialize API configuration in session state."""
    if "api_url" not in st.session_state:
        st.session_state.api_url = DEFAULT_API_URL
    if "username" not in st.session_state:
        st.session_state.username = DEFAULT_USERNAME
    if "password" not in st.session_state:
        st.session_state.password = DEFAULT_PASSWORD

def send_message_to_ollama(message: str, bot_personality: str) -> Dict:
    """
    Send a message to the LLaMA 3.2 API and return the response.
    
    Args:
        message (str): User's message input.
        bot_personality (str): The selected bot's personality.
    
    Returns:
        Dict: API response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "prompt": f"{bot_personality}\nUser: {message}\nAssistant:",
        "model": "llama3.2",
        "stream": False
    }
    try:
        response = requests.post(
            f"{st.session_state.api_url}/api/generate",
            auth=(st.session_state.username, st.session_state.password),
            headers=headers,
            json=payload,
            timeout=90  # Set timeout to 90 seconds
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"response": f"Error: {str(e)}"}

def download_chat_history():
    """Download chat history as a text file."""
    chat_content = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    st.download_button("Download Chat History", chat_content, file_name="chat_history.txt")

def summarize_chat():
    """Summarize the chat history."""
    messages = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
    if messages:
        summary = "Summary of your chat:\n" + "\n".join(messages[-5:])
        st.session_state.messages.append({"role": "assistant", "content": summary})
        st.success("Chat summarized!")
    else:
        st.warning("No messages to summarize.")

def main():
    """Main function to run the Streamlit app."""
    initialize_api_config()

    st.set_page_config(page_title="Advanced Multi-Bot Chat", page_icon="🤖", layout="wide")
    st.title("🤖 Advanced Multi-Bot Chat Interface")

    # Sidebar for bot selection and customization
    with st.sidebar:
        st.markdown("### Select a Bot")
        bot_name = st.selectbox(
            "Choose a Bot", 
            list(BOT_PERSONALITIES.keys()), 
            index=list(BOT_PERSONALITIES.keys()).index(st.session_state.selected_bot)
            if st.session_state.selected_bot in BOT_PERSONALITIES else 0
        )
        st.session_state.selected_bot = bot_name
        bot_personality = BOT_PERSONALITIES[bot_name]

        if bot_name == "Custom Bot":
            bot_personality = st.text_area("Define Custom Bot Personality", value=st.session_state.get("custom_personality", ""))
            st.session_state["custom_personality"] = bot_personality

        st.markdown("### API Configuration")
        st.text_input("API URL", value=st.session_state.api_url, type="password", on_change=initialize_api_config)
        st.text_input("Username", value=st.session_state.username, type="password", on_change=initialize_api_config)
        st.text_input("Password", value=st.session_state.password, type="password", on_change=initialize_api_config)

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared!")

        st.markdown("### Additional Features")
        st.button("Summarize Chat", on_click=summarize_chat)
        download_chat_history()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input for new message
    if prompt := st.chat_input(f"Chat with {bot_name}"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(f"{bot_name} is typing..."):
                response = send_message_to_ollama(prompt, bot_personality)
                st.markdown(response["response"])
                st.session_state.messages.append({"role": "assistant", "content": response["response"]})

if __name__ == "__main__":
    main()

