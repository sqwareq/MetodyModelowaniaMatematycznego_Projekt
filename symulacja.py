import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import control as ct

# --- PARAMETRY SYMULACJI ---
t_start = 0.0
t_stop = 20.0
dt = 0.01  # krok całkowania/próbkowania
t = np.arange(t_start, t_stop, dt) # wektor czasu

# --- GENERACJA SYGNAŁÓW WEJŚCIOWYCH (WARTOŚCI ZADANYCH) ---

# 1. Sygnał prostokątny o skończonym czasie trwania (np. impuls od 2s do 6s)
u_rect = np.where((t >= 2) & (t <= 6), 1.0, 0.0)

# 2. Sygnał trójkątny (amplituda 1, częstotliwość 0.5 Hz)
freq_tri = 0.5
u_tri = signal.sawtooth(2 * np.pi * freq_tri * t, 0.5)

# 3. Sygnał harmoniczny (sinusoida, amplituda 1, częstotliwość 1 Hz)
freq_sin = 1.0
u_sin = np.sin(2 * np.pi * freq_sin * t)

# --- WYKRESY KONTROLNE SYGNAŁÓW ---
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(t, u_rect, label='Sygnał prostokątny', color='blue')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, u_tri, label='Sygnał trójkątny', color='orange')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, u_sin, label='Sygnał harmoniczny', color='green')
plt.xlabel('Czas [s]')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# --- 2. PARAMETRY TRANSMITANCJI I REGULATORA ---
# Zmienna 's' Laplace'a
s = ct.TransferFunction.s

# Parametry obiektu Go(s) - na razie wpisujemy przykładowe wartości
a1, a0 = 1.0, 1.0
b2, b1, b0 = 1.0, 2.0, 1.0

# Tworzenie transmitancji obiektu
Go = (a1 * s + a0) / (b2 * s**2 + b1 * s + b0)

# Parametry regulatora PID (do późniejszego strojenia)
Kp = 5.0
Ki = 2.0
Kd = 1.0
Tf = 0.05 # Stała czasowa filtra różniczkowania (musi być > 0)

# Tworzenie transmitancji realizowalnego PID
Gpid = Kp + (Ki / s) + (Kd * s) / (Tf * s + 1)

# --- 3. UKŁAD ZAMKNIĘTY ---
# Transmitancja układu otwartego (regulator * obiekt)
G_otwarty = Gpid * Go

# Transmitancja układu zamkniętego (ujemne sprzężenie zwrotne)
# feedback(sys1, sys2) domyślnie robi ujemne sprzężenie: sys1 / (1 + sys1*sys2)
# U nas w sprzężeniu zwrotnym nic nie ma, więc wstawiamy 1.
G_zamkniety = ct.feedback(G_otwarty, 1)

print("Transmitancja układu zamkniętego:")
print(G_zamkniety)

# --- 4. SYMULACJA ODPOWIEDZI UKŁADU ---
print("Obliczam symulację...")

# Przypisujemy cały wynik do zmiennej (np. resp_rect), a potem wyciągamy z niej samo 'y'
resp_rect = ct.forced_response(G_zamkniety, T=t, U=u_rect)
y_rect = resp_rect.y[0]

resp_tri = ct.forced_response(G_zamkniety, T=t, U=u_tri)
y_tri = resp_tri.y[0]

resp_sin = ct.forced_response(G_zamkniety, T=t, U=u_sin)
y_sin = resp_sin.y[0]

# --- 5. RYSOWANIE WYNIKÓW ---
plt.figure(figsize=(12, 10))

# Wykres 1: Sygnał prostokątny
plt.subplot(3, 1, 1)
plt.plot(t, u_rect, 'k--', linewidth=2, label='Wartość zadana (wymuszenie)')
plt.plot(t, y_rect, 'b-', linewidth=2, label='Odpowiedź układu (PID)')
plt.title('Odpowiedź układu na sygnał prostokątny')
plt.ylabel('Amplituda')
plt.grid(True)
plt.legend()

# Wykres 2: Sygnał trójkątny
plt.subplot(3, 1, 2)
plt.plot(t, u_tri, 'k--', linewidth=2, label='Wartość zadana (wymuszenie)')
plt.plot(t, y_tri, 'r-', linewidth=2, label='Odpowiedź układu (PID)')
plt.title('Odpowiedź układu na sygnał trójkątny')
plt.ylabel('Amplituda')
plt.grid(True)
plt.legend()

# Wykres 3: Sygnał harmoniczny
plt.subplot(3, 1, 3)
plt.plot(t, u_sin, 'k--', linewidth=2, label='Wartość zadana (wymuszenie)')
plt.plot(t, y_sin, 'g-', linewidth=2, label='Odpowiedź układu (PID)')
plt.title('Odpowiedź układu na sygnał harmoniczny')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()