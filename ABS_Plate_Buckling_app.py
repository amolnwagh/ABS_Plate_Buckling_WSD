import streamlit as st

st.markdown("# ABS Plate Buckling Checks")
st.markdown("### (WSD Method) - *July 2022 Edition*")
st.divider()

with st.sidebar:
    s = st.number_input("Shorter side of panel: s (in)",min_value=0.0001)
    l = st.number_input("Longer side of panel: l (in)",min_value=s)
    alpha = s/l
    st.write(f'Aspect ratio {alpha = }')

st.image(r"figures/typ_stiffened_panel.png","Figure 1: Typical Stiffened Panel")
st.divider()

col1, col2 = st.columns([1,2])
with col1:
    st.image(r"figures/sectional_dims_of_panel.png","Figure 2: Sectional Dimensions of a Typical Stiffened Panel")

with col2:
    st.image(r"figures/loads_on_panel.png","Figure 3: Typical Loads on a Stiffened Panel")

st.divider()

