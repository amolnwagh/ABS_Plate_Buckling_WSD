import streamlit as st
import ABS_Plate_Buckling_WSD.calculations.ABS_Plate_Buckling as ABS

st.markdown("# ABS Plate Buckling Checks")
st.markdown("### (WSD Method) - *July 2022 Edition*")
st.divider()

st.image(r"figures/typ_stiffened_panel.png","Figure 1: Typical Stiffened Panel")
st.divider()

st.image(r"figures/loads_on_panel.png","Figure 3: Typical Loads on a Stiffened Panel")
st.divider()

with st.sidebar:
    st.markdown("# Inputs")
    
    panel_inputs = st.expander("Plate Panel Details (Refer Figure 1)",expanded=False)
    with panel_inputs:
        s = st.number_input("Shorter side of panel: s (cm)",min_value=1e-6)
        l = st.number_input("Longer side of panel: l (cm)",min_value=s)
        t = st.number_input("Thickness of plate panel: t (cm)",min_value=1e-6)
        sigma_0_plate = st.number_input("Yield Stress for Plate Panel Material: sigma_0_plate (N/cm^2)",min_value=1e-6)
        
    stiffener_inputs = st.expander("Panel Stiffener Details",expanded=False)
    with stiffener_inputs:
        st.selectbox("Select Stiffener Type", [*ABS.valid_stiffener_types])

    stress_inputs = st.expander("Load & Stress Data (Refer Figure 2)",expanded=False)
    with stress_inputs:
        load_case_type = st.selectbox("Select Load Case Type", [*ABS.valid_load_case_types]) 
        sigma_ax = st.number_input("Axial stress normal to shorter side (s): sigma_ax (N/cm^2)",min_value=1e-6)
        sigma_ay = st.number_input("Axial stress normal to longer side (l): sigma_ay (N/cm^2)",min_value=1e-6)
        sigma_bx = st.number_input("Bending stress normal to shorter side (s): sigma_bx (N/cm^2)",min_value=1e-6)
        sigma_by = st.number_input("Bending stress normal to longer side (l): sigma_by (N/cm^2)",min_value=1e-6)
        tau = st.number_input("Shear stress: tau (N/cm^2)",min_value=1e-6)
        # sigma_xmax = sigma_ax + sigma_bx
        # sigma_xmin = sigma_ax - sigma_bx
        # sigma_ymax = sigma_ay + sigma_by
        # sigma_ymin = sigma_ay - sigma_by
        # st.write(f'{sigma_xmax = }')
        # st.write(f'{sigma_xmin = }')
        # st.write(f'{sigma_ymax = }')
        # st.write(f'{sigma_ymin = }')
        # st.write(f'{tau = }')


st.markdown("### Calculation")
