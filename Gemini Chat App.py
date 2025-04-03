import os
import streamlit as st
import google.generativeai as genai

# Securely store API Key (DO NOT SHARE PUBLICLY)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "0AIzaSyBL17AgvMOn4RtGkJ0_9kSmSR4aNngFPQSubA9")  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

if GEMINI_API_KEY == "your_api_key_here":
    st.warning("⚠️ Replace 'your_api_key_here' with a valid API key in a secure way!")


genai.configure(api_key=GEMINI_API_KEY)

# Set up page config
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="centered"
)

# List of available Gemini models
models = [
    "models/gemini-2.0-pro-exp",
    "models/gemini-2.0-flash-exp",
    "models/gemini-1.5-pro-latest",
    "models/gemini-1.5-pro-002",
    "models/gemini-1.5-pro-001",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-flash-002",
    "models/gemini-1.5-flash-001",
    "models/gemma-3-27b-it",
]

st.markdown("<br>", unsafe_allow_html=True)  # Adjusts spacing before title
# Streamlit UI
st.title("🔮 Gemini AI Chatbot")
st.write("")
st.write("")
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_model" not in st.session_state:
    st.session_state.current_model = models[0]

# Sidebar for model selection
with st.sidebar:
    st.title("⚙️ Chat Settings")

    # Model selection
    selected_model = st.selectbox(
        "Choose a model",
        models,
        index=models.index(st.session_state.current_model)
    )

    # Update model if changed
    if selected_model != st.session_state.current_model:
        st.session_state.current_model = selected_model
        st.session_state.messages = []  # Clear chat history when model changes
        st.rerun()

    # # Clear chat history button
    # if st.button("Clear Chat History"):
    #     st.session_state.messages = []
    #     st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.caption(f"Model: {message['model']}")

# Chat input and processing
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        try:
            # Initialize model
            model = genai.GenerativeModel(st.session_state.current_model)
            
            # Generate response with context
            response = model.generate_content(prompt)

            # Extract response text safely
            response_text = response.text if hasattr(response, "text") else "Sorry, I couldn't generate a response."

            # Display response
            st.markdown(response_text)
            
            # Add response to history with model info
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "model": st.session_state.current_model
            })
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
