import streamlit as st
import calculations.ABS_Plate_Buckling as ABS
import app_module as AM
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator

st.markdown("# ABS Plate Buckling Checks")
st.markdown("### (WSD Method) - *July 2022 Edition*")
* Link to ABS Buckling Requirements: https://pub-rm20.apps.eagle.org/r/4/2022-07-01/Buckling-and-Ultimate-Strength-Assessment-for-Offshore-Structures

* This app calculates the buckling state limit of a stiffened plated panel as per Section 3 of the ABS reference as mentioned above.
* Such stiffened panels are typically used in hulls of ships and floating offshore structures like jack-up rigs and semi-submersibles.
* Generally, the inputs are details regarding plate panel dimensions and material properties.
* Instead of loads, the inputs are stresses, since these buckling check calculations are used typically after extracting stresses from a detailed finite element analysis model of the mentioned structures.
* Currently, the app gives buckling state limit (UC) check if you have entered the stresses.
* Even if the stresses are not input, the critical buckling state limits are calculated.
* Additionally, interactive plotly charts are presented for the values of the critical buckling stresses and UCs (if stresses are supplied) for the defined panel and also for a range of aspect ratios of the panel, keeping all other inputs same.
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
        sigma_0 = st.number_input("Yield Stress for Plate Panel Material: sigma_0 (N/cm2)",min_value=1e-6)
        E = st.number_input("Young's Modulus of Panel Material: E (N/cm2)",value=2.06e7)
        nu = st.number_input("Poisson's Ratio for Panel Material: nu",value=0.3)
        
    stiffener_inputs = st.expander("Panel Stiffener Details",expanded=False)
    with stiffener_inputs:
        stiffener_type = st.selectbox("Select Stiffener Type", [*ABS.valid_stiffener_types])

    stress_inputs = st.expander("Load & Stress Data (Refer Figure 2)",expanded=False)
    with stress_inputs:
        load_case_type = st.selectbox("Select Load Case Type", [*ABS.valid_load_case_types]) 
        sigma_ax = st.number_input("Axial stress normal to shorter side (s): sigma_ax (N/cm2)",min_value=1e-6)
        sigma_ay = st.number_input("Axial stress normal to longer side (l): sigma_ay (N/cm2)",min_value=1e-6)
        sigma_bx = st.number_input("Bending stress normal to shorter side (s): sigma_bx (N/cm2)",min_value=1e-6)
        sigma_by = st.number_input("Bending stress normal to longer side (l): sigma_by (N/cm2)",min_value=1e-6)
        tau = st.number_input("Shear stress: tau (N/cm^2)",min_value=1e-6)


my_panel = ABS.Panel(
    load_case_type = load_case_type,
    stiffener_type = stiffener_type,
    s = s,
    l = l,
    t = t,
    sigma_ax = sigma_ax,
    sigma_ay = sigma_ay,
    sigma_bx = sigma_bx,
    sigma_by = sigma_by,
    tau = tau,
    sigma_0 = sigma_0,
    E = E,
    nu = nu
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


st.markdown(f"### Plots: Allowable Buckling Stresses v/s Aspect Ratio of the Plate Panel")
st.markdown(f"#### Parameters:")
st.markdown(f"###### _Stiffener Type_ = {stiffener_type}")
st.markdown(f"###### _Shorter Side of Panel_ = {s} cm")
st.markdown(f"###### _Thickness of Panel_ = {t} cm")
st.markdown(f"###### _Yield Stress_ = {sigma_0} N/cm2")


max_alpha = st.slider("Select maximum aspect ratio for the plots:",min_value=1,max_value=100,value=20)
no_of_pts = st.slider("Select the number of data points for the plots:",min_value=10,max_value=100,value=50)
lengths = [s]
for i in range(1,no_of_pts+1):
    lengths.append(s + (i/no_of_pts)*((max_alpha-1)*s))


tau_C_s = []
sigma_C_x_s = []
sigma_C_y_s = []
alphas = []
UCs = []

for length in lengths:
    panel = ABS.Panel(
        load_case_type = load_case_type,
        stiffener_type = stiffener_type,
        s = s,
        l = length,
        t = t,
        sigma_ax = sigma_ax,
        sigma_ay = sigma_ay,
        sigma_bx = sigma_bx,
        sigma_by = sigma_by,
        tau = tau,
        sigma_0 = sigma_0,
        E = E,
        nu = nu
    )
    alphas.append(panel.alpha())
    tau_C_s.append(panel.tau_C())
    sigma_C_x_s.append(panel.sigma_C_x())
    sigma_C_y_s.append(panel.sigma_C_y())
    UCs.append(panel.UC_buckling_state_limit())


fig1 = go.Figure()
fig1.add_scatter(x=alphas, y=tau_C_s)
fig1.layout.title.text = "tau_C v/s alpha"
fig1.layout.xaxis.title = "alpha = aspect ratio = (long side/short side)"
fig1.layout.yaxis.title = "tau_C (N/cm2)"

fig2 = go.Figure()
fig2.add_scatter(x=alphas, y=sigma_C_x_s)
fig2.layout.title.text = "sigma_C_x v/s alpha"
fig2.layout.xaxis.title = "alpha = aspect ratio = (long side/short side)"
fig2.layout.yaxis.title = "sigma_C_x (N/cm2)"

fig3 = go.Figure()
fig3.add_scatter(x=alphas, y=sigma_C_y_s)
fig3.layout.title.text = "sigma_C_y v/s alpha"
fig3.layout.xaxis.title = "alpha = aspect ratio = (long side/short side)"
fig3.layout.yaxis.title = "sigma_C_y (N/cm2)"

fig4 = go.Figure()
fig4.add_scatter(x=alphas, y=tau_C_s, name="tau_C")
fig4.add_scatter(x=alphas, y=sigma_C_x_s, name="sigma_C_x")
fig4.add_scatter(x=alphas, y=sigma_C_y_s,name="sigma_C_y")
fig4.layout.title.text = "Allowable Stresses v/s alpha"
fig4.layout.xaxis.title = "alpha = aspect ratio = (long side/short side)"
fig4.layout.yaxis.title = "Allowable Stress (N/cm2)"

raw_symbols = SymbolValidator().values
symbols = []
for i in range(0,len(raw_symbols),3):
    name = raw_symbols[i+2]
    symbols.append(raw_symbols[i])

fig5 = go.Figure()
fig5.add_scatter(x=alphas, y=UCs, name = "UCs for all aspect ratios")
fig5.add_trace(
    go.Scatter(
        mode="markers",
        x=[my_panel.alpha()],
        y=[my_panel.UC_buckling_state_limit()],
        name = "UC for current aspect ratio",
        marker_symbol = "asterisk",
        marker=dict(
            color='Purple',
            size=10,
            line=dict(
                color='Purple',
                width=1)
            )
        )
)
# fig5.add_scatter(x=[my_panel.alpha()],y=[my_panel.UC_buckling_state_limit()], name = "UC for current aspect ratio")
fig5.layout.title.text = "Buckling State Limit UC v/s alpha"
fig5.layout.xaxis.title = "alpha = aspect ratio = (long side/short side)"
fig5.layout.yaxis.title = "Buckling State Limit UC"

st.divider()
st.plotly_chart(fig1)
st.divider()
st.plotly_chart(fig2)
st.divider()
st.plotly_chart(fig3)
st.divider()
st.plotly_chart(fig4)
st.divider()
st.plotly_chart(fig5)
st.divider()
