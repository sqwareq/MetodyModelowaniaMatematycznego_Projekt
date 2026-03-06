import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import control as ct

# Importujemy nasze moduły
from sygnaly import generuj_sygnaly
from uklad import zbuduj_uklad_zamkniety

# --- 1. PARAMETRY SYMULACJI (CZAS) ---
t = np.arange(0.0, 20.0, 0.01)

# --- 2. PRZYGOTOWANIE GŁÓWNEGO OKNA ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
plt.subplots_adjust(bottom=0.45, hspace=0.4) # Dużo miejsca na dole na suwaki

# Inicjalizacja wykresów "na pusto" (dane podmienimy przy pierwszym uruchomieniu update)
line_u_rect, = ax1.plot(t, np.zeros_like(t), 'k--', linewidth=1.5, label='Wartość zadana')
line_y_rect, = ax1.plot(t, np.zeros_like(t), 'b-', linewidth=2, label='Odpowiedź (PID)')

line_u_tri, = ax2.plot(t, np.zeros_like(t), 'k--', linewidth=1.5, label='Wartość zadana')
line_y_tri, = ax2.plot(t, np.zeros_like(t), 'r-', linewidth=2, label='Odpowiedź (PID)')

line_u_sin, = ax3.plot(t, np.zeros_like(t), 'k--', linewidth=1.5, label='Wartość zadana')
line_y_sin, = ax3.plot(t, np.zeros_like(t), 'g-', linewidth=2, label='Odpowiedź (PID)')

for ax in [ax1, ax2, ax3]:
    ax.grid(True)
    ax.legend(loc='upper right')
    ax.set_ylabel('Amplituda')

ax1.set_title('Sygnał prostokątny')
ax2.set_title('Sygnał trójkątny')
ax3.set_title('Sygnał harmoniczny')
ax3.set_xlabel('Czas [s]')

# --- 3. TWORZENIE SUWAKÓW ---
axcolor = 'lightgoldenrodyellow'

# Kolumna 1: Regulator PID (lewa strona)
ax_Kp = plt.axes([0.08, 0.30, 0.2, 0.03], facecolor=axcolor)
ax_Ki = plt.axes([0.08, 0.25, 0.2, 0.03], facecolor=axcolor)
ax_Kd = plt.axes([0.08, 0.20, 0.2, 0.03], facecolor=axcolor)
ax_Tf = plt.axes([0.08, 0.15, 0.2, 0.03], facecolor=axcolor)

s_Kp = Slider(ax_Kp, 'Kp', 0.0, 20.0, valinit=5.0)
s_Ki = Slider(ax_Ki, 'Ki', 0.0, 20.0, valinit=2.0)
s_Kd = Slider(ax_Kd, 'Kd', 0.0, 10.0, valinit=1.0)
s_Tf = Slider(ax_Tf, 'Tf', 0.01, 1.0, valinit=0.05)

# Kolumna 2: Parametry Obiektu Go (środek)
ax_a1 = plt.axes([0.40, 0.35, 0.2, 0.03], facecolor=axcolor)
ax_a0 = plt.axes([0.40, 0.30, 0.2, 0.03], facecolor=axcolor)
ax_b2 = plt.axes([0.40, 0.25, 0.2, 0.03], facecolor=axcolor)
ax_b1 = plt.axes([0.40, 0.20, 0.2, 0.03], facecolor=axcolor)
ax_b0 = plt.axes([0.40, 0.15, 0.2, 0.03], facecolor=axcolor)

s_a1 = Slider(ax_a1, 'a1', 0.0, 10.0, valinit=1.0)
s_a0 = Slider(ax_a0, 'a0', 0.0, 10.0, valinit=1.0)
s_b2 = Slider(ax_b2, 'b2', 0.1, 10.0, valinit=1.0)
s_b1 = Slider(ax_b1, 'b1', 0.0, 10.0, valinit=2.0)
s_b0 = Slider(ax_b0, 'b0', 0.0, 10.0, valinit=1.0)

# Kolumna 3: Sygnały wejściowe (prawa strona)
ax_amp_r = plt.axes([0.72, 0.30, 0.2, 0.03], facecolor=axcolor)
ax_frq_t = plt.axes([0.72, 0.25, 0.2, 0.03], facecolor=axcolor)
ax_frq_s = plt.axes([0.72, 0.20, 0.2, 0.03], facecolor=axcolor)

s_amp_r = Slider(ax_amp_r, 'Amp Prost.', 0.1, 5.0, valinit=1.0)
s_frq_t = Slider(ax_frq_t, 'Częst. Trójk.', 0.05, 2.0, valinit=0.1)
s_frq_s = Slider(ax_frq_s, 'Częst. Sin.', 0.05, 2.0, valinit=0.2)

# --- 4. FUNKCJA AKTUALIZUJĄCA OBLICZENIA (SERCE PROGRAMU) ---
def update(val):
    # 1. Odczytujemy stan suwaków z sygnałami i generujemy je
    u_rect, u_tri, u_sin = generuj_sygnaly(t, s_amp_r.val, s_frq_t.val, s_frq_s.val)
    
    # 2. Odczytujemy parametry układu i budujemy transmitancję
    G_zamkniety = zbuduj_uklad_zamkniety(
        s_a1.val, s_a0.val, 
        s_b2.val, s_b1.val, s_b0.val, 
        s_Kp.val, s_Ki.val, s_Kd.val, s_Tf.val
    )
    
    # 3. Przeprowadzamy symulację
    resp_rect = ct.forced_response(G_zamkniety, T=t, U=u_rect)
    resp_tri  = ct.forced_response(G_zamkniety, T=t, U=u_tri)
    resp_sin  = ct.forced_response(G_zamkniety, T=t, U=u_sin)
    
    # 4. Aktualizujemy wykresy (wartości zadane oraz odpowiedzi PID)
    line_u_rect.set_ydata(u_rect)
    line_y_rect.set_ydata(resp_rect.y[0])
    
    line_u_tri.set_ydata(u_tri)
    line_y_tri.set_ydata(resp_tri.y[0])
    
    line_u_sin.set_ydata(u_sin)
    line_y_sin.set_ydata(resp_sin.y[0])
    
    # 5. Skalowanie osi Y, jeśli sygnał jest większy niż domyślny podgląd
    for ax in [ax1, ax2, ax3]:
        ax.relim()
        ax.autoscale_view()
        
    fig.canvas.draw_idle()

# Podpinamy funkcję aktualizującą pod każdy z suwaków
wszystkie_suwaki = [
    s_Kp, s_Ki, s_Kd, s_Tf, 
    s_a1, s_a0, s_b2, s_b1, s_b0, 
    s_amp_r, s_frq_t, s_frq_s
]
for suwak in wszystkie_suwaki:
    suwak.on_changed(update)

# Wywołujemy funkcję ręcznie raz na początku, aby narysować wykresy
update(None)

# Wyświetlamy gotowe okno
plt.show()