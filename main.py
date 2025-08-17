import numpy as np
 
turbofan_no_ab = "turbofan_no_ab"
turbojet_no_ab = "turbojet_no_ab"
turbojet_ab = "turbojet_ab"
 
 
def engine(engine_type, afterburner, alpha, Mo, m_dot, hPR, To6, To4, To, pi_c, pi_f, gamma, po, ao, cp):
    
    if afterburner == True:
        ao = (gamma*To*1716)**0.5
        # atmospheric temp ratio
        tao_r = 1 + (gamma - 1) / 2 * (Mo) ** 2

        # core temp ratio
        tao_c = pi_c ** ((gamma - 1) / gamma)
        
        # honestly not sure what temp ratio this is
        tao_lambda = To4/To

        # not sure for this either
        tao_t = 1 - tao_r / tao_lambda * (tao_c - 1)
        
        # Afterburner temp ratio
        tao_lambda_ab = To6/To
        
        # total fuel ratio
        f_total = cp*To*(tao_lambda_ab - tao_r)/hPR
        
        # Exit velocity
        u7ao = (2/(gamma-1) * tao_lambda_ab*(1-1/(tao_r*tao_c*tao_t)))**0.5
        u7 = u7ao*ao
        
        # specific thrust
        Fs = ao*(u7/ao - Mo)/32.2
        
        # TSFC
        TSFC = f_total/Fs *3600

        # non afterburning exit velocity
        squared_values = tao_lambda_ab/(tao_t*tao_lambda)
        u7_no_ab = (u7**2/squared_values)**0.5
        
        
    else:
        if engine_type == turbojet_ab:
            ao = (gamma * To * 1716) ** 0.5    
        uo = Mo * ao
        # atmospheric temp ratio
        tao_r = 1 + (gamma-1)/2 * Mo**2
        
        # core temp ratio
        tao_c = pi_c**((gamma-1)/gamma)
        
        # fan temp ratio
        if alpha == 0: 
            tao_f = 0
        else:
            tao_f = pi_f**((gamma-1)/gamma)
        
        # honestly not sure what temp ratio this is
        tao_lambda = To4/To
        
        # not sure for this either
        tao_t = 1 - tao_r/tao_lambda*(tao_c -1 + alpha*(tao_f -1))
        
        # velocity of core exit
        u7ao_squared = 2/(gamma-1) * tao_lambda/(tao_r*tao_c)*(tao_r*tao_c*(1-tao_r/tao_lambda*(tao_c-1+alpha*(tao_f-1))) -1)
        u7 = u7ao_squared**0.5*ao
        M7 = u7/ao
        u0 = Mo*ao
       
        # Velcotiy of fan exit
        if alpha == 0:
            u9 = 0
        else:
            u9ao_squared = 2/(gamma-1)*(tao_r*tao_f -1)
            u9 = u9ao_squared**0.5*ao
      
        # fan and core mass flow rates
        if alpha == 0:
            mdot_c = m_dot
            mdot_fan = 0
        else:
            mdot_fan = m_dot/(1/alpha + 1)
            mdot_c = mdot_fan/alpha
       
        # Fuel air ratio
        f = cp*To/hPR*(tao_lambda - tao_r*tao_c)
        f_total = f
       
        # thrust
        F = (mdot_c*(u7-uo) + mdot_fan*(u9-uo))/32.2
       
        # specific thrust
        Fs = ao/(1+alpha)*(u7/ao - Mo + alpha*(u9/ao - Mo))/32.2
       
        # thrust specific fuel consumption
        TSFC = f/((1+alpha)*Fs)*3600
       
        # Turbine efficiency
        eta_T = 1-1/(tao_r*tao_c)
       
        # power efficiency
        eta_P = 2*(u7/uo - 1 + alpha*(u9/uo -1))/(u7**2/(uo**2)-1+alpha*(u9**2/(uo**2)-1))
       
        # total efficiency
        eta_o = eta_P*eta_T
    
    if engine_type == turbofan_no_ab:
        values = [
            ("Nozzle exit velocity (ft/s)", u7),
            # ("Inlet velocity (ft/s)", u0),
            ("Fan exit velocity (ft/s)", u9),
            # ("m dot fan", mdot_fan),
            # ("m dot c", mdot_c),
            ("Thrust (lbf)", F),
            ("Specific thrust (lbf*sec/lbm)", Fs),
            ("fuel air ratio", f),
            ("TSFC (lbm/lbf-hr)", TSFC),
            ("Thermal efficiency", eta_T),
            ("Propulsive efficiency", eta_P),
            ("Overall efficiency", eta_o)]
    # elif engine_type == turbojet_no_ab:
    #         values = [
    #             ("Exit Mach Number", M7),
    #             ("Thrust (lbf)", F),
    #             ("Specific thrust (lbf*sec/lbm)", Fs),
    #             ("fuel air ratio", f),
    #             ("TSFC (lbm/lbf-hr)", TSFC),
    #             ("Thermal efficiency", eta_T),
    #             ("Propulsive efficiency", eta_P),
    #             ("Overall efficiency", eta_o)]
    # elif engine_type == turbojet_ab:
    #     values = [
    #         # ("Speed of sound (ft/sec)", ao),
    #         ("Exit Velcoity (ft/sec)", u7),
    #         ("Specific thrust (lbf*sec/lbm)", Fs),
    #         ("fuel air ratio", f_total),
    #         ("TSFC (lbm/lbf-hr)", TSFC) ]
    
    print("-----------------------")
    print("Engine Values")
    print("-----------------------")
    for label, value in values:
        print(label)
        print(value)
        print()

# def ramjet(Mo, To, gamma, cp, hPR, To4):
#     ao = 287
# 
#     # calculate ambient temp ratio and other ratio
#     tao_r = 1 + (gamma-1)/2*Mo**2
#     tao_lambda = To4/To
#     
#     # calculate ambient pressure ratio and other pressure ratio
#     pi_s = 1-0.075*(Mo-1)**1.35
#     pi_r = tao_r**(gamma/(gamma-1))
#     
#     # calculate exit velocity
#     u7ao = (2/(gamma-1)*(tao_lambda/tao_r)*((pi_r*pi_s)**((gamma-1)/gamma)-1))**0.5
#     u7 = u7ao*ao
#     
#     # calculate fuel air ratio
#     f = cp*To/(hPR) *(tao_lambda-tao_r)
#     
#     # calculate thrust
#     Fs = ao*(u7ao - Mo)
#     
#     # calcualte inlet velocity
#     uo = u7-Fs
#     
#     # calculate TSFC
#     TSFC = f/Fs*3600
#     
#     # calculate efficiencies
#     eta_T = (u7**2-uo**2)/(2*f*hPR)
#     eta_P = 2*(u7/uo - 1)/(u7**2/(uo**2)-1)
#     eta_O = eta_P * eta_T
# 
#     values = [
#         ("Mach Number", Mo),
#         ("Specific thrust (N/(kg/s))", Fs),
#         ("TSFC (kg/N-hr)", TSFC)]
# 
# 
#     print("-----------------------")
#     print("Engine Values")
#     print("-----------------------")
#     for label, value in values:
#         print(label)
#         print(value)
#         print()

# engine(engine_type, afterburner, alpha, Mo, m_dot, hPR, To6, To4, To, pi_c, pi_f, gamma, po, ao, cp):
# engine(turbofan_no_ab, False, 6.5, 0.8, 1125, 18400, 0, 1850, 411.8, 15, 1.75, 1.4, 629.5, 995, 0.24)
engine(turbofan_no_ab, False, 10, 0.8417,2900, 18400, 0, 4800, 390, 22.4854, 2.2434, 1.4, 393.18996, 982.667, 0.24)
# engine(turbojet_no_ab, False, 0, 0.8, 170, 18400, 0, 1210, 411.8, 13.5, 0, 1.4, 629.5, 995, 0.24)
# engine(turbojet_ab, True, 0, 2, 0, 18400, 2000, 1583, 411.8, 10, 0, 1.4, 629.5, 995, 0.24)
# engine(turbojet_ab, False, 0, 2, 0, 18400, 2000, 1583, 411.8, 10, 0, 1.4, 629.5, 995, 0.24)

# def ramjet(Mo, To, gamma, cp, hPR, To4):
# ramjet(2, 205, 1.4, 1.005, 45000, 3000)
# ramjet(4, 205, 1.4, 1.005, 45000, 3000)