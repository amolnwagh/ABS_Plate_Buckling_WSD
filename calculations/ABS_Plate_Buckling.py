from dataclasses import dataclass
from math import pi, sqrt
from handcalcs.decorator import handcalc
    
valid_stiffener_types = ("ANGLE","TEE","FLAT BAR","BULB PLATE","PLATE ELEMENT","WEB PLATE OF STIFFENERS","LOCAL PLATE OF CORRUGATED PANELS")
valid_load_case_types = ("NORMAL OPERATION","SEVERE STORM")

@dataclass
class Panel:
    
    """
    load_case_type: str # any item from the list "valid_load_case_types"
    stiffener_type: str # any item from the list "valid_stiffener_types"
    s: float # length of shorter side of the plate panel (cm)
    l: float # length of longer side of the plate panel (cm)
    t: float # thickness of plating (cm)
    sigma_ax: float # axial stress normal to shorter side (N/cm^2)
    sigma_ay: float # axial stress normal to longer side (N/cm^2)
    sigma_bx: float # bending stress normal to shorter side (N/cm^2)
    sigma_by: float # bending stress normal to longer side (N/cm^2)
    tau: float = 1e-6 # edge shear stress (N/cm^2)
    sigma_0: float  = 235000 # yeild stress of panel material (N/cm^2)
    E: float = 2.06e7 # modulus of elasticity (N/cm^2)
    nu: float = 0.3 # poisson's ratio for steel
    """
    load_case_type: str # any item from the list "valid_load_case_types"
    stiffener_type: str # any item from the list "valid_stiffener_types"
    s: float # length of shorter side of the plate panel (cm)
    l: float # length of longer side of the plate panel (cm)
    t: float # thickness of plating (cm)
    sigma_ax: float # axial stress normal to shorter side (N/cm^2)
    sigma_ay: float # axial stress normal to longer side (N/cm^2)
    sigma_bx: float # bending stress normal to shorter side (N/cm^2)
    sigma_by: float # bending stress normal to longer side (N/cm^2)
    tau: float # edge shear stress (N/cm^2)
    sigma_0: float  = 235000 # yeild stress of panel material (N/cm^2)
    E: float = 2.06e7 # modulus of elasticity (N/cm^2)
    nu: float = 0.3 # poisson's ratio for steel
       
    def alpha(self):
        return calc_alpha(self.l, self.s)
       
    def sigma_x_max(self):
        return calc_sigma_max(self.sigma_ax,self.sigma_bx)
    
    def sigma_x_min(self):
        return calc_sigma_min(self.sigma_ax,self.sigma_bx)
    
    def sigma_y_max(self):
        return calc_sigma_max(self.sigma_ay,self.sigma_by)
    
    def sigma_y_min(self):
        return calc_sigma_min(self.sigma_ay,self.sigma_by)
    
    def C1(self):
        return calc_C1(self.stiffener_type)
    
    def C2(self):
        return calc_C2(self.stiffener_type)
    
    def eta(self):
        return calc_eta(self.load_case_type)
    
    def kappa_x(self):
        return calc_kappa(self.sigma_x_min(),self.sigma_x_max())
    
    def kappa_y(self):
        return calc_kappa(self.sigma_y_min(),self.sigma_y_max())
          
    def k_s_tau(self):
        return calc_k_s_tau(self.alpha(), self.C1())
    
    def k_s_sigma_x(self):
        return calc_k_s_sigma_x(self.C1(),self.kappa_x())
    
    def k_s_sigma_y(self):
        return calc_k_s_sigma_y(self.C2(), self.alpha(), self.kappa_y())
    
    def tau_0(self):
        return calc_tau_0(self.sigma_0)
        
    def tau_E(self):
        return calc_stress_E(self.k_s_tau(),self.t, self.s, self.E, self.nu)
    
    def sigma_E_x(self):
        return calc_stress_E(self.k_s_sigma_x(), self.t, self.s, self.E, self.nu)
    
    def sigma_E_y(self):
        return calc_stress_E(self.k_s_sigma_y(), self.t, self.s, self.E, self.nu)
    
    def tau_C(self):
        return calc_stress_C(self.tau_0(), self.tau_E())
    
    def sigma_C_x(self):
        return calc_stress_C(self.sigma_0, self.sigma_E_x())
    
    def sigma_C_y(self):
        return calc_stress_C(self.sigma_0, self.sigma_E_y())
    
    def UC_buckling_state_limit(self):
        return calc_UC_buckling_state_limit(
            self.sigma_x_max(),
            self.sigma_y_max(),
            self.tau,
            self.sigma_C_x(),
            self.sigma_C_y(),
            self.tau_C(),
            self.eta()
        )
     
         
def calc_alpha(l:float,s:float) -> float:
    """calculate aspect ratio of a plate panel defined according to ABS Requirements for Buckling (WSD Method)

    Args:
        l (float): length of longer side of the plate panel
        s (float): length of shorter side of the plate panel

    Returns:
        alpha: aspect ratio of the plate panel
    """
    alpha = l/s
    return alpha


def calc_sigma_max(sigma_a:float, sigma_b: float) -> float:
    """calulates maximum normal stress

    Args:
        sigm_a (float): axial normal stress
        sigma_b (float): bending normal stress

    Returns:
        float: maximum normal stress
    """
    max_stress = sigma_a + sigma_b
    return max_stress


def calc_sigma_min(sigma_a:float, sigma_b: float) -> float:
    """calulates minimum normal stress

    Args:
        sigm_a (float): axial normal stress
        sigma_b (float): bending normal stress

    Returns:
        float: minimum normal stress
    """
    min_stress = sigma_a - sigma_b
    return min_stress


def calc_C1(stiffener_type: str) -> float:
    """calculates value of C1 based on Stiffener type

    Args:
        stiffener_type (str): any item from the list "valid_stiffener_types"
        
    Returns:
        float: value of C1
    """
    if stiffener_type in  valid_stiffener_types:
        if stiffener_type in ("ANGLE", "TEE"):
            C1 = 1.1
        else:
            C1 = 1.0
        return C1
    else:
        raise ValueError(f"Invalid stiffener type provided. Acceptable stiffener types are: {valid_stiffener_types}")

    
def calc_C2(stiffener_type: str) -> float:
    """calculates value of C2 based on Stiffener type

    Args:
        stiffener_type (str): any item from the list "valid_stiffener_types"
        
    Returns:
        float: value of C2   
    """
    if stiffener_type in  valid_stiffener_types:
        if stiffener_type in ("ANGLE", "TEE"):
            C2 = 1.2
        elif stiffener_type in ("FLAT BAR", "BULB PLATE"):
            C2 = 1.1
        else:
            C2 = 1.0
        return C2
    else:
        raise ValueError(f"Invalid stiffener type provided. Acceptable stiffener types are: {valid_stiffener_types}")
  
       
def calc_eta(load_case_type: str) -> float:
    """calculates maximum allowable strength factor

    Args:
        load_case_type (str): any item from the list "valid_load_case_types"
        
    Returns:
        float: maximum allowable strength factor, eta
    """
    phi = 1.0 # Adjustment factor ABS Buckling Requirements (WSD), Cl 3-1.7
    if load_case_type in valid_load_case_types:
        if load_case_type == "NORMAL OPERATION":
            eta = 0.6 * phi
        else:
            eta = 0.8 * phi
        return eta
    else:
        raise ValueError(f"Invalid load case type provided. Acceptable load case types are: {valid_load_case_types}")

    
def calc_kappa(sigma_min:float, sigma_max:float) -> float:
    """calculates ratio of edge stresses

    Args:
        sigma_min (float): minimum stress (Axial Stress + Bending Stress), N/cm2
        sigma_max (float): maximum stress (Axial Stress - Bending Stress), N/cm2

    Returns:
        float: ratio of edge stresses, kappa
    """
    try:
        kappa = sigma_min/sigma_max
        return kappa
    except: ValueError
    
    
def calc_k_s_tau(alpha:float, C1:float) -> float:
    """calculates boundary dependent constant for shear buckling

    Args:
        alpha (float): aspect ratio of the plate panel
        C1 (float): value of C1 based on Stiffener type

    Returns:
        float: boundary dependent constant for shear buckling
    """
    k_s = (4.0 * (1/alpha)**2 + 5.34) * C1
    return k_s
    

def calc_k_s_sigma_x(C1:float, kappa_x:float) -> float:
    """calculates boundary dependant factor for stress sigma_x (normal to shorter side)
    
    Args:
        C1 (float): value of C1 based on Stiffener type
        kappa_x (float): boundary dependant factor for stress sigma_x (normal to shorter side)

    Returns:
        float: boundary dependant factor for stress normal to shorter side
    """
    if 0 <= kappa_x <= 1.0:
        k_s_sigma_x = C1 * (8.4/(kappa_x + 1.1))
    elif -1.0 <= kappa_x < 0.0:
        k_s_sigma_x = C1 * (7.6 - (6.4 * kappa_x) + 10*(kappa_x**2))
    return k_s_sigma_x


def calc_k_s_sigma_y(C2:float, alpha:float, kappa_y:float) -> float:
    """calculates boundary dependant factor for stress sigma_y (normal to longer side)
    
    Args:
        C2 (float): value of C2 based on Stiffener type
        alpha (float): aspect ratio of the plate panel
        kappa_y (float): _description_

    Returns:
        float: boundary dependant factor for stress sigma_y (normal to longer side)
    """
    if kappa_y < (1/3):
        if 1.0 <= alpha <= 2.0:
            k_s_sigma_y = C2 * (1.0875 * (1 + (1/(alpha**2)))**2 - (18/(alpha**2))) * (1 + kappa_y) + (24/(alpha**2))
        elif alpha > 2.0:
            k_s_sigma_y = C2 * (1.0875 * (1 + (1/(alpha**2)))**2 - (9/(alpha**2))) * (1 + kappa_y) + (12/(alpha**2))
    elif kappa_y >= (1/3):
        k_s_sigma_y = C2 * (1 + (1/(alpha**2)))**2 * (1.675 - (0.675*kappa_y))
    return k_s_sigma_y


def calc_tau_0(sigma_0:float) -> float:
    """calculate shear strength of plate

    Args:
        sigma_0 (float): specified minimum yield point of plate, N/cm2 

    Returns:
        float: shear strength of plate, N/cm2
    """
    tau_0  = sigma_0/sqrt(3)
    return tau_0


def calc_stress_E(k_s_stress:float, t:float, s:float, E:float = 2.06e7, nu:float=0.3) -> float:
    """calculate elastic shear buckling stress

    Args:
        k_s_stress (float): boundary dependent constant
        t (float): thickness of plating, cm
        s (float): length of short plate edge, cm
        E (float, optional): modulus of elasticity. Defaults to 2.06e7, N/cm2 .
        nu (float, optional): Poisson's ratio. Defaults to 0.3 for steel.

    Returns:
        float: elastic shear buckling stress, N/cm2 
    """
    stress_E = k_s_stress * (((pi**2) * E)/(12 * (1 - (nu**2))) ) * (t/s)**2
    return stress_E


def calc_stress_C(stress_0:float, stress_E:float, P_r:float = 0.6) -> float:
    """calculate critical buckling stress for edge shear
    Args:
        stress_0 (float): shear strength of plate, N/cm2
        stress_E (float): elastic shear buckling stress, N/cm2
        P_r (float, optional): proportional linear elastic limit of the structure. Defaults to 0.6 for steel.

    Returns:
        float: critical buckling stress for edge shear, N/cm2
    """
    if stress_E <= P_r * stress_0:
        stress_C = stress_E
        return stress_C
    else:
        stress_C = stress_0 * (1 - P_r * (1 - P_r) * (stress_0 / stress_E))
        return stress_C

    
def calc_UC_buckling_state_limit(sigma_x_max:float, sigma_y_max:float, tau:float, sigma_C_x:float, sigma_C_y:float, tau_C:float, eta:float) -> float:
    """calculates buckling state limit UC

    Args:
        sigma_x_max (float): maximum compressive stress in the longitudinal direction (i.e. normal to shorter side), N/cm2
        sigma_y_max (float): maximum compressive stress in the transverse direction (i.e. normal to longer side), N/cm2 
        tau (float): edge shear stress, N/cm2 
        sigma_C_x (float): critical buckling stress for uniaxial compression in the longitudinal direction, N/cm2
        sigma_C_y (float): critical buckling stress for uniaxial compression in the transverse direction,N/cm2
        tau_C (float): critical buckling stress for edge shear, N/cm2 
        eta (float): maximum allowable strength utilization factor, as defined in Subsection 1/11 and 3/1.7

    Returns:
        float: buckling state limit UC of a plate panel, subjected to in-plane loads
    """
    UC_buckling_state_limit = (sigma_x_max/(eta*sigma_C_x))**2 + (sigma_y_max/(eta*sigma_C_y))**2 + (tau/(eta*tau_C))**2
    return UC_buckling_state_limit
    