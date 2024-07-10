import eng_module.columns as columns
from dataclasses import dataclass
from enum import Enum
from math import pi, sqrt

class StiffenerType(Enum):
    ANGLE = 1
    TEE = 2
    FLAT_BAR = 3
    BULB_PLATE = 4
    PLATE_ELEM = 5
    LOCAL_PL_OF_STIFFENERS = 6
    LOCAL_PL_OF_CORRUGATED_PANELS = 7

@dataclass
class Panel:
    
    """
    stiffener_type: 
    s: float # length of shorter side of the plate panel (cm)
    l: float # length of longer side of the plate panel (cm)
    t: float # thickness of plating (cm)
    E: float = 2.06e7 # modulus of elasticity (N/cm^2)
    nu: float = 0.3 # poisson's ratio for steel
    sigma_0: float  = 235000 # yeild stress of panel material (N/cm^2)
    sigma_ax: float = 1e-6 # axial stress normal to shorter side (N/cm^2)
    sigma_ay: float = 1e-6 # axial stress normal to longer side (N/cm^2)
    sigma_bx: float = 1e-6 # bending stress normal to shorter side (N/cm^2)
    sigma_by: float = 1e-6 # bending stress normal to longer side (N/cm^2)
    tau: float = 1e-6 # edge shear stress (N/cm^2)
    """
    stiffener_type: StiffenerType #
    s: float # length of shorter side of the plate panel (cm)
    l: float # length of longer side of the plate panel (cm)
    t: float # thickness of plating (cm)
    E: float = 2.06e7 # modulus of elasticity (N/cm^2)
    nu: float = 0.3 # poisson's ratio for steel
    sigma_0: float  = 235000 # yeild stress of panel material (N/cm^2)
    sigma_ax: float = 1e-6 # axial stress normal to shorter side (N/cm^2)
    sigma_ay: float = 1e-6 # axial stress normal to longer side (N/cm^2)
    sigma_bx: float = 1e-6 # bending stress normal to shorter side (N/cm^2)
    sigma_by: float = 1e-6 # bending stress normal to longer side (N/cm^2)
    tau: float = 1e-6 # edge shear stress (N/cm^2)
    
        
    def Alpha(self):
        return calc_Alpha(self.l, self.s)
        
    def sigma_x_max(self):
        return calc_sigma_max(self.sigma_ax,self.sigma_bx)
    
    def sigma_x_min(self):
        return calc_sigma_min(self.sigma_ax,self.sigma_bx)
    
    def sigma_y_max(self):
        return calc_sigma_max(self.sigma_ay,self.sigma_by)
    
    def sigma_y_min(self):
        return calc_sigma_min(self.sigma_ay,self.sigma_by)
        
    def tau_0(self):
        return calc_tau_0(self.sigma_0)
    
    def C1(self):
        return calc_C1(self.stiffener_type)
          
    def k_s(self):
        return calc_k_s(self.Alpha(), self.C1())
    
    def tau_E(self):
        return calc_tau_E(self.ks(),self.t, self.s, self.E, self.nu)
    
    def tau_C(self):
        return calc_tau_C(self.tau_0(), self.tau_E())
        
    
def calc_Alpha(l:float,s:float) -> float:
    """calculate aspect ratio of a plate panel defined according to ABS Requirements for Buckling (WSD Method)

    Args:
        l (float): length of longer side of the plate panel
        s (float): length of shorter side of the plate panel

    Returns:
        Alpha: aspect ratio of the plate panel
    """
    aspect_ratio = l/s
    return aspect_ratio


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


def calc_C1(stiffener_type: StiffenerType) -> float:
    """calculates value of C1 based on Stiffener type

    Args:
        stiffener_type (StiffenerType): Enumeration from Class StiffenerType
    Returns:
        float: value of C1
    """
    if stiffener_type in [StiffenerType.ANGLE, StiffenerType.TEE]:
        C1 = 1.1
        return C1
    else:
        C1 = 1.0
        return C1


def calc_tau_0(sigma_0:float) -> float:
    """calculate shear strength of plate

    Args:
        sigma_0 (float): specified minimum yield point of plate, N/cm2 

    Returns:
        float: shear strength of plate, N/cm2
    """
    tau_0  = sigma_0/sqrt(3)
    return tau_0


def calc_k_s(Alpha:float, C1:float) -> float:
    k_s = (4.0 * (1/Alpha)**2 + 5.34) * C1
    return k_s

  
def calc_tau_E(k_s:float, t:float, s:float, E:float = 2.06e7, nu:float=0.3) -> float:
    """calculate elastic shear buckling stress

    Args:
        k_s (float): boundary dependent constant
        t (float): thickness of plating, cm
        s (float): length of short plate edge, cm
        E (float, optional): modulus of elasticity. Defaults to 2.06e7, N/cm2 .
        nu (float, optional): Poisson's ratio. Defaults to 0.3 for steel.

    Returns:
        float: elastic shear buckling stress, N/cm2 
    """
    tau_E = k_s * (((pi**2) * E)/(12 * (1 - (nu**2))) ) * (t/s)**2
    return tau_E


def calc_tau_C(tau_0:float, tau_E:float, P_r:float = 0.6) -> float:
    if tau_E <= P_r * tau_0:
        tau_C = tau_E
        return tau_C
    else:
        tau_C = tau_0 * (1 - P_r * (1 - P_r) * (tau_0 / tau_E))
        return tau_C
    
       
    




