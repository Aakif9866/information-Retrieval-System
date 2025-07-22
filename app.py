import streamlit as st
from src.helper import (
    get_pdf_text,
    get_text_chunks,
    get_vector_store,
    get_conversational_chain
)

def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        with st.chat_message("user" if i % 2 == 0 else "assistant"):
            st.markdown(message.content)

def main():
    st.set_page_config(page_title="Information Retrieval")
    st.header("Information Retrieval System 💁")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None

    user_question = st.text_input("Ask a Question from the PDF Files")
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True
        )

        if pdf_docs:
            st.markdown("### Uploaded Files:")
            for doc in pdf_docs:
                st.write(doc.name)

        if st.button("Submit & Process") and pdf_docs:
            with st.spinner("Processing..."):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversational_chain(vector_store)
                    st.success("Done ✅ Now ask your question!")
                except Exception as e:
                    st.error(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
