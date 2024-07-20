import streamlit as st
import ABS_Plate_Buckling_WSD.calculations.ABS_Plate_Buckling as ABS
import ABS_Plate_Buckling_WSD.app_module as AM
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
        sigma_0_plate = st.number_input("Yield Stress for Plate Panel Material: sigma_0_plate (N/cm2)",min_value=1e-6)
        E = st.number_input("Young's Modulus of Panel Material: E (N/cm2)",value=2.06e7)
        nu = st.number_input("Poisson's Ratio for Panel Material: nu",value=0.3)
        
    stiffener_inputs = st.expander("Panel Stiffener Details",expanded=False)
    with stiffener_inputs:
        st.selectbox("Select Stiffener Type", [*ABS.valid_stiffener_types])

    stress_inputs = st.expander("Load & Stress Data (Refer Figure 2)",expanded=False)
    with stress_inputs:
        load_case_type = st.selectbox("Select Load Case Type", [*ABS.valid_load_case_types]) 
        sigma_ax = st.number_input("Axial stress normal to shorter side (s): sigma_ax (N/cm2)",min_value=1e-6)
        sigma_ay = st.number_input("Axial stress normal to longer side (l): sigma_ay (N/cm2)",min_value=1e-6)
        sigma_bx = st.number_input("Bending stress normal to shorter side (s): sigma_bx (N/cm2)",min_value=1e-6)
        sigma_by = st.number_input("Bending stress normal to longer side (l): sigma_by (N/cm2)",min_value=1e-6)
        tau = st.number_input("Shear stress: tau (N/cm^2)",min_value=1e-6)


my_panel = ABS.Panel(
    load_case_type = "NORMAL OPERATION",
    stiffener_type = "ANGLE",
    s = 60,
    l = 120,
    t = 1.2,
    sigma_ax = 10000,
    sigma_ay = 5000,
    sigma_bx = 2000,
    sigma_by = 1000,
    tau = 5000,
    sigma_0 = 23500,
    E = 2.06e7,
    nu = 0.3
)


example_latex = AM.calc(
    my_panel.load_case_type,
    my_panel.stiffener_type,
    my_panel.s,
    my_panel.l,
    my_panel.t,
    my_panel.sigma_ax,
    my_panel.sigma_ay,
    my_panel.sigma_bx,
    my_panel.sigma_by,
    my_panel.tau,
    my_panel.sigma_0,
    my_panel.E,
    my_panel.nu
    )

st.markdown("### Results Summary")
st.write(f"tau_C = {round(my_panel.tau_C(),3)} N/cm2")
st.write(f"sigma_C_x = {round(my_panel.sigma_C_x(),3)} N/cm2")
st.write(f"sigma_C_y = {round(my_panel.sigma_C_y(),3)} N/cm2")
st.write(f"UC_buckling_state_limit = {round(my_panel.UC_buckling_state_limit(),3)}")


detail_calc = st.expander("Detail Calculation", expanded = False)
with detail_calc:
    st.write(f"Load Case Type = {my_panel.load_case_type}")
    st.write(f"Stiffener Type = {my_panel.stiffener_type}")
    st.write(f"Panel Short Side (s) = {round(my_panel.s,3)} cm")
    st.write(f"Panel Long Side (l) = {round(my_panel.l,3)} cm")
    st.write(f"Panel Thickness (t) = {round(my_panel.t,3)} cm")
    st.write(f"sigma_ax = {round(my_panel.sigma_ax,3)} N/cm2")
    st.write(f"sigma_ay = {round(my_panel.sigma_ay,3)} N/cm2")
    st.write(f"sigma_bx = {round(my_panel.sigma_bx,3)} N/cm2")
    st.write(f"sigma_by = {round(my_panel.sigma_by,3)} N/cm2")
    st.write(f"sigma_0 = {round(my_panel.sigma_0,3)} N/cm2")
    st.write(f"E = {round(my_panel.E,3)} N/cm2")
    st.write(f"nu = {round(my_panel.nu,3)}")
    st.write(f"alpha = {round(my_panel.alpha(),3)}")
    st.latex(example_latex[0])   
    st.write(f"sigma_x_max = {round(my_panel.sigma_x_max(),3)} N/cm2")
    st.latex("\sigma_xmax =" + example_latex[1])
    st.write(f"sigma_x_min = {round(my_panel.sigma_x_min(),3)} N/cm2")
    st.latex("\sigma_xmin =" + example_latex[2])
    st.write(f"sigma_y_max = {round(my_panel.sigma_y_max(),3)} N/cm2")
    st.latex("\sigma_ymax =" + example_latex[3])
    st.write(f"sigma_y_min = {round(my_panel.sigma_y_min(),3)} N/cm2")
    st.latex("\sigma_ymin =" + example_latex[4])
    st.write(f"C1 = {round(my_panel.C1(),3)}")
    st.write(f"C2 = {round(my_panel.C2(),3)}")
    st.write(f"eta = {round(my_panel.eta(),3)}")
    st.write(f"kappa_x = {round(my_panel.kappa_x(),3)}")
    st.write(f"kappa_y = {round(my_panel.kappa_y(),3)}")
    st.write(f"k_s_tau = {round(my_panel.k_s_tau(),3)}")
    st.write(f"k_s_sigma_x = {round(my_panel.k_s_sigma_x(),3)}")
    st.write(f"k_s_sigma_y = {round(my_panel.k_s_sigma_y(),3)}")
    st.write(f"tau_0 = {round(my_panel.tau_0(),3)} N/cm2")
    st.latex(example_latex[5])
    st.write(f"tau_E = {round(my_panel.tau_E(),3)} N/cm2")
    st.write(f"sigma_E_x = {round(my_panel.sigma_E_x(),3)} N/cm2")
    st.write(f"sigma_E_y = {round(my_panel.sigma_E_y(),3)} N/cm2")
    st.write(f"tau_C = {round(my_panel.tau_C(),3)} N/cm2")
    st.write(f"sigma_C_x = {round(my_panel.sigma_C_x(),3)} N/cm2")
    st.write(f"sigma_C_y = {round(my_panel.sigma_C_y(),3)} N/cm2")
    st.write(f"UC_buckling_state_limit = {round(my_panel.UC_buckling_state_limit(),3)}")
     