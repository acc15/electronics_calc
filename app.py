import streamlit as st

st.set_page_config(layout="wide")

pg = st.navigation([
    st.Page("ne555/app.py", title="ne555", url_path="ne555"), 
    st.Page("smd_decoder/app.py", title="smd", url_path="smd"), 
    st.Page("resistors/app.py", title="vdiv", url_path="vdiv")])
pg.run()
