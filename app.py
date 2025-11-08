# ----- IMPORTS -----
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai  # import correto

# ----- TÍTULO -----
st.title("Chatbot Gemini de Músicas")

# ----- HISTÓRICO -----
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- CONEXÃO COM A API GEMINI -----
load_dotenv()  # carrega o .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Erro ao carregar a chave GEMINI_API_KEY. Verifique seu arquivo .env.")
    st.stop()

# configura a chave da API
genai.configure(api_key=GEMINI_API_KEY)

# ----- FUNÇÃO DE COMUNICAÇÃO -----
def get_gemini_response(prompt):
    # cria o modelo generativo
    model = genai.GenerativeModel("gemini-2.5-flash")  # modelo recomendado
    response = model.generate_content(prompt)
    return response.text

# ----- LÓGICA DO CHAT -----
if prompt := st.chat_input("Digite sua mensagem aqui:"):
    # exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # obtém resposta do Gemini
    with st.spinner("A IA está pensando..."):
        response = get_gemini_response(prompt)

    # exibe a resposta
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
