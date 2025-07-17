# login.py
import streamlit as st
from dotenv import load_dotenv
import os

# Para validar a senha sempre carregamos o .env.blueberry (mesma SENHA nos 3 .env)
load_dotenv(dotenv_path=".env.blueberry", override=False)

def login_screen():
    st.title("Login")
    st.write("Digite a sua senha para entrar:")
    pwd = st.text_input("", type="password", placeholder="••••••••")
    if st.button("Entrar"):
        if pwd == os.getenv("SENHA"):
            st.info("Senha correta, pressione novamente o 'Entrar'")
            st.session_state.logged_in = True
        else:
            st.error("❌ Senha incorreta.")

def main():
    # inicializa flag de login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        import collection
        collection.main()
    else:
        login_screen()

if __name__ == "__main__":
    main()
