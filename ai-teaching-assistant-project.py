import streamlit as st

from google import genai

from google.genai import types

import config



# Initialize Gemini API client

client = genai.Client(api_key=config.GEMINI_API_KEY)



def generate_response(prompt, temperature=0.3):

    try:

        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

        config_params = types.GenerateContentConfig(temperature=temperature)

        response = client.models.generate_content(

            model="gemini-2.0-flash", contents=contents, config=config_params)

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"



def setup_ui():

    st.title("Enhanced AI Teaching Assistant")

    st.write("Ask questions and get AI responses tailored by role. Your conversation history is saved below!")



    # Initialize session state for conversation history

    if "conversation" not in st.session_state:

        st.session_state.conversation = []



    # Dropdown for role selection

    role = st.selectbox("Select AI Role", ["Teacher", "Expert", "Friendly Helper"])



    # Input text box for question

    user_input = st.text_input("Enter your question here:")



    # Button to submit question

    if st.button("Ask"):

        if user_input.strip() != "":

            # Create role-based prompt

            prompt = f"You are a {role}. Please answer the following question:\n{user_input}"



            # Generate AI response

            response = generate_response(prompt)



            # Save Q&A to conversation history

            st.session_state.conversation.append({"question": user_input, "answer": response})



    # Button to clear conversation

    if st.button("Clear Conversation"):

        st.session_state.conversation = []



    # Display conversation history

    for i, chat in enumerate(st.session_state.conversation):

        st.markdown(f"**You:** {chat['question']}")

        st.markdown(f"**AI ({role}):** {chat['answer']}")

        st.markdown("---")



def main():

    setup_ui()



if __name__ == "__main__":

    main()
