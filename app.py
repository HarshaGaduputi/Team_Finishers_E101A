import streamlit as st
import json
from crawler import crawl_website
from indexer import index_website
from agent import answer_query

if "connected" not in st.session_state:
    st.session_state.connected = False
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Universal Website AI Agent Chatbot")

website_url = st.text_input("Enter Website URL to connect:")

if website_url and not st.session_state.connected:
    st.write("Crawling website…")
    pages, graph = crawl_website(website_url, max_pages=10)
    st.write("Indexing website content…")
    st.write(index_website(pages))
    st.session_state.connected = True
    st.success("Website connected and learned!")

if st.session_state.connected:
    user_q = st.text_input("Ask something about the connected website:")

    if user_q:
        score, url, text = answer_query(user_q)
        st.session_state.history.append((user_q, score, url, text))
        st.write("Confidence:", round(score, 2))

        if url and score > 0.75:
            st.write("Auto navigating to:")
            st.write(url)
        elif url:
            st.write("You can reach it through:")
            st.write(url)

        st.write("Answer:")
        st.write(text[:300])
        st.write("---")

    for q, s, u, t in st.session_state.history:
        st.write("**Q:**", q)
        st.write("Confidence:", round(s, 2))
        if u:
            if s > 0.75:
                st.write("Auto-navigate to:", u)
            else:
                st.write("Suggested path:", u)
        st.write("**Answer:**")
        st.write(t[:300])
        st.write("---")
