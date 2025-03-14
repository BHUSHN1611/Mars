import streamlit as st
import os
def load_css():
    if os.path.exists("styles.css"):
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown("""<style>
                    .stApp {
                        background-color: #14114;
                    }
                    </style>""", unsafe_allow_html=True)
