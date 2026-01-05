import streamlit as st
import math
from typing import ClassVar

st.title("Ohms law")

def enforce_law():
    
    state = st.session_state
    names = set(["P","I","V","R"])

    fill_count = sum(1 for name in names if name in st.session_state and st.session_state[name])
    if fill_count != 2:
        return

    def f(name:str) -> float|None:
        v = state.get(name, None)
        return float(v) if v else None

    P = f("P")
    I = f("I")
    V = f("V")
    R = f("R")
    
    if I is not None and R is not None:
        V, P = I * R, (I**2) * R
    elif V is not None and I is not None:
        R, P = V / I, V * I
    elif V is not None and R is not None:
        I, P = V / R, (V**2) / R
    elif P is not None and I is not None:
        V, R = P / I, P / (I**2)
    elif P is not None and V is not None:
        I, R = P / V, (V**2) / P
    elif P is not None and R is not None:
        V = math.sqrt(P * R)
        I = V / R

    state["P"] = str(P)
    state["I"] = str(I)
    state["V"] = str(V)
    state["R"] = str(R)
    
enforce_law()

st.text("Fill 2 any variables - 2 others will be computed automatically")

col1, col2 = st.columns(2)
with col1:
    st.text_input("P", value=None, key="P")
    st.text_input("V", value=None, key="V")

with col2:
    st.text_input("I", value=None, key="I")
    st.text_input("R", value=None, key="R")

