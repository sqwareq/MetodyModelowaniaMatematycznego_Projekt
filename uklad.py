import control as ct

def zbuduj_uklad_zamkniety(a1, a0, b2, b1, b0, Kp, Ki, Kd, Tf):
    s = ct.TransferFunction.s
    
    # Transmitancja obiektu
    Go = (a1 * s + a0) / (b2 * s**2 + b1 * s + b0)
    
    # Transmitancja realizowalnego PID
    Gpid = Kp + (Ki / s) + (Kd * s) / (Tf * s + 1)
    
    # Układ zamknięty (ujemne sprzężenie zwrotne)
    G_zamkniety = ct.feedback(Gpid * Go, 1)
    
    return G_zamkniety