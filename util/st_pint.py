import pint
import streamlit as st

if "ureg" not in st.session_state:
    ureg = pint.UnitRegistry()
    ureg.formatter.default_format = ".2f~#P"
    st.session_state["ureg"] = ureg
else:
    ureg = st.session_state["ureg"]

def q(value, unit = None):
    return ureg.Quantity(value, unit)