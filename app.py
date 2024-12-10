import os
import streamlit as st
import google.generativeai as genai

# Configure the API Key
genai.configure(api_key="HELIX_API_KEY")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Generative AI model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Set page configuration
st.set_page_config(page_title="Zoom Transcript Assistant", page_icon="📜", layout="wide")

# Main Page Title and Description
st.title("📜 Zoominary - Transcript Chat Assistant")
st.markdown("""
Welcome to the **Zoominary**! This tool helps you analyze Zoom call transcripts and query details from them.
Simply provide the directory path to your transcript files in the sidebar, and you're good to go!
""")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("Use this section to upload and configure the transcript files.")

# Sidebar for Directory Input
uploaded_directory = st.sidebar.text_input("📂 Enter the directory path containing transcript files:")
start_chat = st.sidebar.button("🚀 Start Chat")

# Main chat interface logic
if start_chat and uploaded_directory:
    try:
        # List all transcript files in the directory
        transcript_files = [
            os.path.join(uploaded_directory, file)
            for file in os.listdir(uploaded_directory)
            if file.endswith('.txt')  # Accept transcript files in .txt format
        ]

        if not transcript_files:
            st.sidebar.error("❌ No transcript files found in the directory.")
        else:
            # Read all transcript files and concatenate the contents
            transcripts = ""
            for file_path in transcript_files:
                with open(file_path, "r", encoding="utf-8") as file:
                    transcripts += file.read() + "\n\n"

            # Create the initial chat session with transcripts
            history = [
                {
                    --- CONFIGURATION TRAINING LOGIC TO BE USED HERE ---
                    ],
                }
            ]

            # Add transcripts as input in the initial message
            initial_message = {
                "role": "user",
                "parts": [f"Here are the transcripts:\n{transcripts}"],
            }
            history.append(initial_message)

            # Start the chat session
            chat_session = model.start_chat(history=history)

            # Send the initial message with transcripts
            response = chat_session.send_message(initial_message["parts"][0])
            st.sidebar.success("✅ Transcripts processed. You can now start chatting!")

            # Enable chat interface
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = chat_session

    except Exception as e:
        st.sidebar.error(f"⚠️ Error processing transcript files: {e}")

# Main Chat Logic for Displaying Messages
if "chat_session" in st.session_state:
    chat_session = st.session_state.chat_session

    # Chat UI - Initialize messages if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to display chat bubbles
    def display_messages():
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(
                    f"""
                    <div style="background-color: #ff7070; color: white; padding: 10px; margin: 5px; 
                                border-radius: 10px; max-width: 75%; float: right; word-wrap: break-word; 
                                font-family: Arial, sans-serif;">
                        {message['text']}
                    
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="background-color: #2e2bb5; color: white; padding: 10px; margin: 5px; 
                                border-radius: 10px; max-width: 75%; float: left; word-wrap: break-word; 
                                font-family: Arial, sans-serif;">
                        {message['text']}
                    
                    """,
                    unsafe_allow_html=True,
                )

    # Display the messages in chat bubbles
    with st.container():
        st.markdown("### 💬 Chat History")
        display_messages()

    # User input box and send message functionality
    def on_user_input():
        user_input = st.session_state.user_input
        if user_input:
            try:
                # Send message to model and get response
                response = chat_session.send_message(user_input)

                # Add user message and assistant reply to history
                st.session_state.messages.append({"role": "user", "text": user_input})
                st.session_state.messages.append({"role": "assistant", "text": response.text})

                # Reset the input field after sending
                st.session_state.user_input = ""

            except Exception as e:
                st.error(f"⚠️ Error during chat: {e}")

    # User input field with on_change callback
    st.text_input(
        "📝 Ask a question about the transcripts:",
        key="user_input",
        placeholder="Type your message here...",
        on_change=on_user_input,
    )
