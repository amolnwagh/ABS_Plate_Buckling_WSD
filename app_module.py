import ABS_Plate_Buckling_WSD.calculations.ABS_Plate_Buckling as ABS
from handcalcs.decorator import handcalc

hc_renderer = handcalc(override='long')

calc_alpha = hc_renderer(ABS.calc_alpha)
calc_max_stress = hc_renderer(ABS.calc_sigma_max)
calc_min_stress = hc_renderer(ABS.calc_sigma_min)
calc_tau_0 = hc_renderer(ABS.calc_tau_0)


def calc(  
    load_case_type: str, # any item from the list "valid_load_case_types"
    stiffener_type: str, # any item from the list "valid_stiffener_types"
    s: float, # length of shorter side of the plate panel (cm)
    l: float, # length of longer side of the plate panel (cm)
    t: float, # thickness of plating (cm)
    sigma_ax: float, # axial stress normal to shorter side (N/cm^2)
    sigma_ay: float, # axial stress normal to longer side (N/cm^2)
    sigma_bx: float, # bending stress normal to shorter side (N/cm^2)
    sigma_by: float, # bending stress normal to longer side (N/cm^2)
    tau: float, # edge shear stress (N/cm^2)
    sigma_0: float, # yeild stress of panel material (N/cm^2)
    E: float, # modulus of elasticity (N/cm^2)
    nu: float # poisson's ratio for steel    
):
    alpha_latex, _ = calc_alpha(l,s)
    sigma_x_max_latex, _ = calc_max_stress(sigma_ax, sigma_bx)
    sigma_x_min_latex, _ = calc_min_stress(sigma_ax, sigma_bx)
    sigma_y_max_latex, _ = calc_max_stress(sigma_ay, sigma_by)
    sigma_y_min_latex, _ = calc_min_stress(sigma_ay, sigma_by)
    tau_0_latex, _ = calc_tau_0(sigma_0)
    
    return [alpha_latex, sigma_x_max_latex, sigma_x_min_latex, sigma_y_max_latex, sigma_y_min_latex, tau_0_latex]
    



