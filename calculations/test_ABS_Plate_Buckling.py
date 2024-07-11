import ABS_Plate_Buckling_WSD.calculations.ABS_Plate_Buckling as ABS
import math

def test_calc_Alpha():
    assert math.isclose(ABS.calc_Alpha(60,60), 1.0)
    assert math.isclose(ABS.calc_Alpha(120,60), 2.0)

        
def test_calc_sigma_max():
    assert math.isclose(ABS.calc_sigma_max(200,100), 300.0)
    assert math.isclose(ABS.calc_sigma_max(100,0), 100.0)
    
    
def test_calc_sigma_min():
    assert math.isclose(ABS.calc_sigma_min(200,100), 100.0)
    assert math.isclose(ABS.calc_sigma_min(100,0), 100.0)
    
    
def test_calc_C1():
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.ANGLE),1.1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.TEE),1.1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.FLAT_BAR),1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.BULB_PLATE),1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.PLATE_ELEM),1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.WEB_PL_OF_STIFFENERS),1)
    assert math.isclose(ABS.calc_C1(ABS.StiffenerType.LOCAL_PL_OF_CORRUGATED_PANELS),1)
    
def test_calc_C2():
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.ANGLE),1.2)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.TEE),1.2)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.FLAT_BAR),1.1)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.BULB_PLATE),1.1)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.PLATE_ELEM),1)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.WEB_PL_OF_STIFFENERS),1)
    assert math.isclose(ABS.calc_C2(ABS.StiffenerType.LOCAL_PL_OF_CORRUGATED_PANELS),1)         


def test_calc_eta():
    assert math.isclose(ABS.calc_eta(ABS.LoadCaseType.NORMAL_OPERATION),0.6)
    assert math.isclose(ABS.calc_eta(ABS.LoadCaseType.SEVERE_STORM),0.8)
    

def test_calc_kappa():
    assert ABS.calc_kappa(ABS.calc_sigma_min(0,10),ABS.calc_sigma_max(0,10)) == -1.0
    assert ABS.calc_kappa(ABS.calc_sigma_min(100,0),ABS.calc_sigma_max(100,0)) == 1.0
    assert math.isclose(ABS.calc_kappa(ABS.calc_sigma_min(100,10),ABS.calc_sigma_max(100,10)),0.8181818182)
    assert math.isclose(ABS.calc_kappa(ABS.calc_sigma_min(10,100),ABS.calc_sigma_max(10,100)),-0.8181818182)
    assert 1.0 > ABS.calc_kappa(ABS.calc_sigma_min(100,10),ABS.calc_sigma_max(100,10)) > 0.0
    assert 0.0 > ABS.calc_kappa(ABS.calc_sigma_min(10,100),ABS.calc_sigma_max(10,100)) > -1.0    


def test_calc_k_s_tau():
    assert math.isclose(ABS.calc_k_s_tau(1, 1), 9.34)
    assert math.isclose(ABS.calc_k_s_tau(1, 1.1), 10.274)
    assert math.isclose(ABS.calc_k_s_tau(2, 1), 6.34)
    assert math.isclose(ABS.calc_k_s_tau(2, 1.1), 6.974)

    
def test_calc_k_s_sigma_x():
    assert math.isclose(ABS.calc_k_s_sigma_x(10,0),76.36363636)
    assert math.isclose(ABS.calc_k_s_sigma_x(10,0.5),52.50)
    assert math.isclose(ABS.calc_k_s_sigma_x(10,1.0),40.0)
    assert math.isclose(ABS.calc_k_s_sigma_x(10,-0.5),133.0)
    assert math.isclose(ABS.calc_k_s_sigma_x(10,-1.0),240.0)


def test_calc_k_s_sigma_y():
    assert math.isclose(ABS.calc_k_s_sigma_y(10,2.5,1),13.456)
    assert math.isclose(ABS.calc_k_s_sigma_y(10,2.5,(1/3)),19.5112)
    assert math.isclose(ABS.calc_k_s_sigma_y(10,1.0,0.25),-146.625)
    assert math.isclose(ABS.calc_k_s_sigma_y(10,1.5,0.25),-60.97106481)
    assert math.isclose(ABS.calc_k_s_sigma_y(10,2.0,0.25),-29.00976563)
    assert math.isclose(ABS.calc_k_s_sigma_y(10,2.5,0.25),2.21175)

def test_calc_tau_0():
    assert math.isclose(ABS.calc_tau_0(23500), 13567.73133)

 
def test_calc_stress_E():
    assert math.isclose(ABS.calc_stress_E(k_s_stress=10.274, t=1.2, s=60), 76514.52387)


def test_calc_stress_C():
    assert math.isclose(ABS.calc_stress_C(stress_0=10000, stress_E=5000),5000.0)
    assert math.isclose(ABS.calc_stress_C(stress_0=10000, stress_E=6000),6000.0) 
    assert math.isclose(ABS.calc_stress_C(stress_0=10000, stress_E=7000),6571.428571)
    
    
my_panel = ABS.Panel(
    load_case_type= ABS.LoadCaseType.NORMAL_OPERATION,
    stiffener_type= ABS.StiffenerType.ANGLE,
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


def test_Panel_Alpha():
    assert math.isclose(my_panel.Alpha(),2.0)
     
def test_Panel_sigma_x_max():
    assert math.isclose(my_panel.sigma_x_max(),12000.0)
    
def test_Panel_sigma_x_min():
    assert math.isclose(my_panel.sigma_x_min(),8000.0)
    
def test_Panel_sigma_y_max():
    assert math.isclose(my_panel.sigma_y_max(),6000.0)

def test_Panel_sigma_y_min():
    assert math.isclose(my_panel.sigma_y_min(),4000.0)

def test_Panel_C1():
    assert math.isclose(my_panel.C1(),1.1)

def test_Panel_C2():
    pass

def test_Panel_kappa_x():
    pass

def test_Panel_kappa_y():
    pass
       
def test_Panel_k_s_tau():
    assert math.isclose(my_panel.k_s_tau(),6.974)
    
def test_Panel_k_s_sigma_x():
    pass

def test_Panel_k_s_sigma_y():
    pass

def test_Panel_tau_0():
    assert math.isclose(my_panel.tau_0(),13567.73133)

def test_Panel_tau_E():
    assert math.isclose(my_panel.tau_E(),51938.12434)

def test_Panel_sigma_E_x():
    pass

def test_Panel_sigma_E_y():
    pass

def test_Panel_tau_C():
    assert math.isclose(my_panel.tau_C(),12717.10377)
    
def test_Panel_sigma_C_x():
    pass

def test_Panel_sigma_C_y():
    pass

