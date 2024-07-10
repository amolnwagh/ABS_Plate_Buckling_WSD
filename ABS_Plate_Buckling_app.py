import streamlit as st

st.markdown("# ABS Plate Buckling Checks")
st.markdown("### (WSD Method) - *July 2022 Edition*")
st.divider()

st.image(r"figures/typ_stiffened_panel.png","Figure 1: Typical Stiffened Panel")
st.divider()

col1, col2 = st.columns([1,2])
with col1:
    st.image(r"figures/sectional_dims_of_panel.png","Figure 2: Sectional Dimensions of a Typical Stiffened Panel")

with col2:
    st.image(r"figures/loads_on_panel.png","Figure 3: Typical Loads on a Stiffened Panel")
st.divider()

with st.sidebar:
    st.markdown("# Inputs")
    
    panel_inputs = st.expander("Plate Panel Dimensions (Refer Figure 1)",expanded=False)
    with panel_inputs:
        s = st.number_input("Shorter side of panel: s (in)",min_value=1e-6)
        l = st.number_input("Longer side of panel: l (in)",min_value=s)
        alpha = s/l
        st.write(f'Aspect ratio {alpha = }')
        sigma_0_plate = st.number_input("Yield Stress for Plate Panel Material: sigma_0_plate (psi)",min_value=1e-6)

    stress_inputs = st.expander("Stress Data (Refer Figure 3)",expanded=False)
    with stress_inputs: 
        st.markdown("## Load Data (Stresses)")
        sigma_ax = st.number_input("Axial stress normal to shorter side (s): sigma_ax (psi)",min_value=1e-6)
        sigma_ay = st.number_input("Axial stress normal to longer side (l): sigma_ay (psi)",min_value=1e-6)
        sigma_bx = st.number_input("Bending stress normal to shorter side (s): sigma_bx (psi)",min_value=1e-6)
        sigma_by = st.number_input("Bending stress normal to longer side (l): sigma_by (psi)",min_value=1e-6)
        tau = st.number_input("Shear stress: tau (psi)",min_value=1e-6)
        sigma_xmax = sigma_ax + sigma_bx
        sigma_xmin = sigma_ax - sigma_bx
        sigma_ymax = sigma_ay + sigma_by
        sigma_ymin = sigma_ay - sigma_by
        st.write(f'{sigma_xmax = }')
        st.write(f'{sigma_xmin = }')
        st.write(f'{sigma_ymax = }')
        st.write(f'{sigma_ymin = }')
        st.write(f'{tau = }')
        
    stiffener_inputs = st.expander("Stiffener Data (Refer Figure 2)",expanded=False)
    with stiffener_inputs:
        st.write("In Progress")
        sigma_0_stf = st.number_input("Yield Stress for Stiffener: sigma_0_stf (psi)",min_value=1e-6)
