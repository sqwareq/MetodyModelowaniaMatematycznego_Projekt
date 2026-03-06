import numpy as np
from scipy import signal

def generuj_sygnaly(t, amp_rect=1.0, freq_tri=0.1, freq_sin=0.2):
    # 1. Sygnał prostokątny o zmiennej amplitudzie
    u_rect = np.where((t >= 2) & (t <= 10), amp_rect, 0.0)
    
    # 2. Sygnał trójkątny o zmiennej częstotliwości
    u_tri = signal.sawtooth(2 * np.pi * freq_tri * t, 0.5)
    
    # 3. Sygnał harmoniczny (sinusoida) o zmiennej częstotliwości
    u_sin = np.sin(2 * np.pi * freq_sin * t)
    
    return u_rect, u_tri, u_sin