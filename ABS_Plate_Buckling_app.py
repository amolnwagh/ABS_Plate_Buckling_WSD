import streamlit as st
import ABS_Plate_Buckling_WSD.calculations.ABS_Plate_Buckling as ABS
from handcalcs.decorator import handcalc

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

my_panel = ABS.Panel(
    load_case_type= "NORMAL OPERATION",
    stiffener_type= "ANGLE",
    s = 60,
    l = 120,
    t = 1.2,
    sigma_0= 23500,
    sigma_ax= 10000,
    sigma_ay= 5000,
    sigma_bx= 2000,
    sigma_by= 1000,
    tau = 5000
)

st.markdown("### Calculation")
st.latex(my_panel.alpha()[0])
st.latex(my_panel.sigma_x_max()[0])
st.latex(my_panel.sigma_x_min()[0])
st.latex(my_panel.sigma_y_max()[0])
st.latex(my_panel.sigma_y_min()[0])
st.latex(my_panel.C1()[0])
st.latex(my_panel.C2()[0])
st.latex(my_panel.eta()[0])
st.latex(my_panel.kappa_x()[0])
st.latex(my_panel.kappa_x()[0])
