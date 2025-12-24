import streamlit as st

from smd_decoder.smd_decoder import decode
from util.st_pint import ureg

st.title('SMD decoder')
code = st.text_input("Code", value = "")

value = decode(code)
if value is not None:
    st.markdown(f'<p style="font-size:64px;">{str(ureg.Quantity(value, ureg.ohms))}</p>', text_alignment="center", unsafe_allow_html=True)


