import streamlit as st
import asyncio
from ollama_utils import chat, generate, list_models, show_model, create_model, copy_model, delete_model, pull_model, push_model, get_embeddings, async_chat

def display_chat():
    st.header("Chat")
    model = st.text_input("Model", "llama2")
    message = st.text_area("Message", "Why is the sky blue?")
    stream = st.checkbox("Enable Streaming")

    if st.button("Send"):
        if stream:
            response_container = st.empty()
            stream = chat(model=model, messages=[{'role': 'user', 'content': message}], stream=True)
            full_response = ""
            for chunk in stream:
                full_response += chunk['message']['content']
                response_container.text(full_response)
        else:
            response = chat(model=model, messages=[{'role': 'user', 'content': message}])
            st.write(response['message']['content'])

def display_generate():
    st.header("Generate")
    model = st.text_input("Model", "llama2")
    prompt = st.text_area("Prompt", "Why is the sky blue?")
    if st.button("Generate"):
        response = generate(model=model, prompt=prompt)
        st.write(response['message']['content'])

def display_list():
    st.header("List")
    if st.button("List Models"):
        models = list_models()
        st.write(models)

def display_show():
    st.header("Show")
    model = st.text_input("Model", "llama2")
    if st.button("Show Model"):
        model_info = show_model(model)
        st.write(model_info)

def display_create():
    st.header("Create")
    model = st.text_input("Model Name", "example")
    modelfile = st.text_area("Modelfile", "FROM llama2\nSYSTEM You are mario from super mario bros.")
    if st.button("Create Model"):
        create_model(model=model, modelfile=modelfile)
        st.success(f"Model {model} created successfully.")

def display_copy():
    st.header("Copy")
    source = st.text_input("Source Model", "llama2")
    destination = st.text_input("Destination Model", "user/llama2")
    if st.button("Copy Model"):
        copy_model(source, destination)
        st.success(f"Model copied from {source} to {destination}.")

def display_delete():
    st.header("Delete")
    model = st.text_input("Model", "llama2")
    if st.button("Delete Model"):
        delete_model(model)
        st.success(f"Model {model} deleted successfully.")

def display_pull():
    st.header("Pull")
    model = st.text_input("Model", "llama2")
    if st.button("Pull Model"):
        pull_model(model)
        st.success(f"Model {model} pulled successfully.")

def display_push():
    st.header("Push")
    model = st.text_input("Model", "user/llama2")
    if st.button("Push Model"):
        push_model(model)
        st.success(f"Model {model} pushed successfully.")

def display_embeddings():
    st.header("Embeddings")
    model = st.text_input("Model", "llama2")
    prompt = st.text_area("Prompt", "The sky is blue because of rayleigh scattering")
    if st.button("Get Embeddings"):
        embeddings = get_embeddings(model=model, prompt=prompt)
        st.write(embeddings)

# Asynchronous Chat
def display_async_chat():
    st.header("Asynchronous Chat")
    model = st.text_input("Async Model", "llama2")
    message = st.text_area("Async Message", "Why is the sky blue?")

    async def async_chat_function():
        response_container = st.empty()
        full_response = ""
        async for part in async_chat(model=model, messages=message):
            full_response += part
            response_container.text(full_response)

    if st.button("Send Async"):
        asyncio.run(async_chat_function())
