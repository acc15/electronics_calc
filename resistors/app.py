import streamlit as st
import pandas as pd

from resistors.resistors import parse_workbook, find_dividers

from util.st_pint import ureg

if "catalog" not in st.session_state:
    catalog = list(parse_workbook("./resistors/known_resistors.xlsx"))
    st.session_state["catalog"] = catalog
else:
    catalog = st.session_state["catalog"]

if "types" not in st.session_state:
    types = list(set([ r.type for r in catalog ]))
    types.sort()
    st.session_state["types"] = types
else:
    types = st.session_state["types"]

if "powers" not in st.session_state:
    powers = list(set([ r.power for r in catalog ]))
    powers.sort()
    st.session_state["powers"] = powers
else:
    powers = st.session_state["powers"]


st.title('Voltage Divider')

v_ref = st.number_input("V:small[ref]", value = 5.0, format="%.5f")
max_error = st.number_input("Max error (%)", min_value=0.0, max_value=100.0, value=5.00, format="%.2f") / 100.0
search_types = st.segmented_control("Resistor types", types, selection_mode="multi")
search_powers = st.segmented_control("Power", powers, selection_mode="multi")

search_type = st.radio("Search type", ["Resistance", "Factor", "Voltage"], horizontal=True)
match search_type:
    case "Resistance":
        r1_col, r2_col = st.columns(2)
        with r1_col:
            r1 = st.number_input("R:small[1]", min_value=0.0, value=1000.0, step=1.0)
        with r2_col:
            r2 = st.number_input("R:small[2]", min_value=0.0, value=1000.0, step=1.0)
        search_factor = r2 / (r1 + r2)
    case "Voltage":
        v_div = st.number_input("V:small[div]", max_value=v_ref, value=v_ref / 2)
        search_factor = v_div / v_ref
    case _:
        search_factor = st.number_input("Factor", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

found_dividers = find_dividers(
    filter(lambda r: r.type in search_types and r.power in search_powers, catalog),
    v_ref, search_factor, max_error)

data = pd.DataFrame(map(lambda d: {
    "Error": ureg.Quantity(d.error).to("%"),
    "Factor": ureg.Quantity(d.factor).to("%"),
    "Rtev": d.r_tev * ureg.ohms,
    "Vtev": d.v_tev * ureg.volts,
    "Rtotal": d.r_total * ureg.ohms,
    "Current": d.current * ureg.ampere,
    "R1 #": d.r1.row,
    "R1": d.r1.resistance * ureg.ohms,
    "R1 Type": d.r1.type,
    "R1 Power": d.r1.power * ureg.watts,
    "R2 #": d.r2.row,
    "R2": d.r2.resistance * ureg.ohms,
    "R2 Type": d.r2.type,
    "R2 Power": d.r2.power * ureg.watts,
}, found_dividers))

st.dataframe(data, height="stretch")

# f"Found pairs {len(found_dividers)}"