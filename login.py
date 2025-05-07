import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

def login():
    st.title("Login")
    st.markdown("""
            <style>
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background: linear-gradient(135deg, #7f1d1d, #3f0f0f);
            }
            .login-box {
                background-color: #1f1f1f;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                width: 100%;
                max-width: 400px;
            }
            .login-title {
                font-size: 32px;
                font-weight: bold;
                color: #fff;
                margin-bottom: 30px;
                text-align: center;
            }
            label, .stTextInput > div > input {
                color: #fff;
            }
            </style>
        """, unsafe_allow_html=True)

    password1 = os.getenv("SENHA")

    input_pass = st.text_input("Password", type="password")

    if st.button("Login"):
        if input_pass == password1:
            st.session_state.logged_in = True
            st.success("Successful Login")
            st.session_state.show_main = True

        else:
            st.warning("Invalid  password.")


if __name__ == "__main__":

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.show_main = False

    if st.session_state.logged_in:
        import collection as collection

        collection.main()
    else:
        login()
