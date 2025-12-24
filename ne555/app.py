import streamlit as st

import math

from util.st_pint import q

st.title('NE555 timing calculator')
st.set_page_config(layout="wide")

r1 = st.number_input("R1", 1, 1000000, 10000, 1)
r2 = st.number_input("R2", 1, 1000000, 200000, 1)
c = st.number_input("C", 0.0, 1.0, 0.00000001, 0.000000000001, "%0.12f")
k = st.slider("K", 0.0, 1.0, 2/3)

st.divider()

t_high = (r1+r2)*c*math.log((1 - 0.5*k) / (1 - k))
t_low = math.log(2)*r2*c
t_period = t_high + t_low
duty = t_high / t_period
freq = 1 / t_period

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("T high", str(q(t_high,"s")))
c2.metric("T low", str(q(t_low,"s")))
c3.metric("Period", str(q(t_period,"s")))
c4.metric("Duty", str(q(duty,"").to("%")))
c5.metric("Frequency", str(q(freq,"hertz")))
