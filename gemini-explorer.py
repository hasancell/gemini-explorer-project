import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession

# Initialize and Set Up the Project
project = "gemini-explorer-1"
vertexai.init(project=project)

# Configuration for the Generation Model
config = generative_models.GenerationConfig(temperature=0.4)

# Initialize the Generative Model
model = GenerativeModel("gemini-pro", generation_config=config)

# Start a Chat Session with the Model
chat = model.start_chat()

# Function to implement personalized greetings for all messages
def llm_function(chat: ChatSession, query, user_name):
    # Send the user's query to the model and get the response
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    # Personalize the model's response with the user's name
    personalized_output = f"Hello, {user_name}! {output}"

    # Display the personalized response in the Streamlit chat interface
    with st.chat_message("model"):
        st.markdown(personalized_output)

    # Append the user's query and personalized model's response to the session state
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": personalized_output})

# Set the Title for the Streamlit App
st.title("Gemini Explorer")

# Initialize the Session State Messages if not Already Present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if the Message History is Empty and Send Initial Prompt
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. Start off with a greeting in a Scottish accent. You use emojis to be interactive"
    response = chat.send_message(initial_prompt)
    output = response.candidates[0].content.parts[0].text
    st.session_state.messages.append({"role": "model", "content": output})

# Display Existing Messages from the Session State
for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Provide an Input Box for User Queries and User's Name
query = st.text_input("Ask a question about Gemini")
user_name = st.text_input("Please enter your name:")

# Process the User's Query and Name when the Send Button is Clicked
if st.button("Send"):
    if query and user_name:
        # Process the user's query using the llm_function
        llm_function(chat, query, user_name)

    