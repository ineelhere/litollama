import streamlit as st
from streamlit_option_menu import option_menu
from ui_components import display_chat, display_generate, display_list, display_show, display_create, display_copy, display_delete, display_pull, display_push, display_embeddings

# Title
st.title('LitOllama')

# Create a horizontal option menu
feature = option_menu(
    menu_title=None,  # Hide the menu title
    options=["Chat", "Generate", "List", "Show", "Create", "Copy", "Delete", "Pull", "Push", "Embeddings"],
    icons=['chat', 'file-earmark-plus', 'list', 'eye', 'file-earmark', 'files', 'trash', 'cloud-arrow-down', 'cloud-arrow-up', 'graph-up'],
    menu_icon="cast",
    default_index=0,
)

# Display selected feature
if feature == "Chat":
    display_chat()
elif feature == "Generate":
    display_generate()
elif feature == "List":
    display_list()
elif feature == "Show":
    display_show()
elif feature == "Create":
    display_create()
elif feature == "Copy":
    display_copy()
elif feature == "Delete":
    display_delete()
elif feature == "Pull":
    display_pull()
elif feature == "Push":
    display_push()
elif feature == "Embeddings":
    display_embeddings()
