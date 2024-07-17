import ollama
from ollama import AsyncClient

def chat(model, messages, stream=False):
    if stream:
        return ollama.chat(model=model, messages=messages, stream=True)
    else:
        return ollama.chat(model=model, messages=messages)

def generate(model, prompt):
    return ollama.generate(model=model, prompt=prompt)

def list_models():
    return ollama.list()

def show_model(model):
    return ollama.show(model)

def create_model(model, modelfile):
    return ollama.create(model=model, modelfile=modelfile)

def copy_model(source, destination):
    return ollama.copy(source, destination)

def delete_model(model):
    return ollama.delete(model)

def pull_model(model):
    return ollama.pull(model)

def push_model(model):
    return ollama.push(model)

def get_embeddings(model, prompt):
    return ollama.embeddings(model=model, prompt=prompt)

async def async_chat(model, messages):
    message_data = {'role': 'user', 'content': messages}
    async for part in await AsyncClient().chat(model=model, messages=[message_data], stream=True):
        yield part['message']['content']
