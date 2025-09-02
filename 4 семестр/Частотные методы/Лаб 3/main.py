import numpy as np
import matplotlib.pyplot as plt

# ===== Функции для генерации сигналов =====
def generate_signals(a, t1, t2, b, c, d, T, dt):
    """
    Генерирует временной вектор, исходный сигнал g(t) и зашумлённый сигнал u(t).
    Здесь u(t) = g(t) + b*ξ(t) + c*sin(d*t), где ξ(t) – белый шум (U[-1,1]).
    """
    t = np.arange(-T/2, T/2, dt)
    g = np.zeros_like(t)
    g[(t >= t1) & (t <= t2)] = a

    # Генерация белого шума (равномерное распределение на [-1,1])
    xi = 2 * np.random.rand(len(t)) - 1
    u = g + b * xi + c * np.sin(d * t)
    return t, g, u


# ===== Функции для работы с Фурье-преобразованием =====
def compute_fft(u, dt):
    """
    Вычисляет центрированное Фурье-преобразование сигнала u(t) и вектор частот.
    """
    N = len(u)
    U = np.fft.fftshift(np.fft.fft(u))
    # Ширина спектра и шаг по частоте:
    V = 1 / dt
    dv = 1 / (N * dt)
    f = np.linspace(-V/2, V/2 - dv, N)
    return f, U

def inverse_fft(U):
    """
    Выполняет обратное Фурье-преобразование от центрированного спектра U.
    """
    u_rec = np.fft.ifft(np.fft.ifftshift(U))
    return np.real(u_rec)

# ===== Функции для построения графиков =====
def plot_time_signals(t, signals, labels, title, freq_lim=None, src=None):
    """
    Строит график временных сигналов.
    """
    plt.figure(figsize=(10, 4))
    for signal, label in zip(signals, labels):
        plt.plot(t, signal, label=label)
    if freq_lim is not None:
        plt.xlim([-freq_lim, freq_lim])
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if src is not None:
        plt.savefig(src)
        plt.close()
    else:
        plt.show()

def plot_spectra(f, spectra, labels, title, freq_lim=None, colors=None, src=None):
    """
    Строит график спектров сигналов (модули Фурье-образов). Если задан freq_lim, выводит ось частот в диапазоне [-freq_lim, freq_lim].
    """
    plt.figure(figsize=(10, 4))
    for n, (spec, label) in enumerate(zip(spectra, labels)):
        if colors:
            plt.plot(f, spec, colors[n], label=label)
        else:
            plt.plot(f, spec, label=label)
    if freq_lim is not None:
        plt.xlim([-freq_lim, freq_lim])
    plt.xlabel('Частота')
    plt.ylabel('Модуль')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if src is not None:
        plt.savefig(src)
        plt.close()
    else:
        plt.show()


# ===== Функция фильтрации =====
def low_pass_filter(U, f, cutoff):
    """
    Применяет фильтр нижних частот: обнуляет спектральные компоненты для |f| > cutoff.
    """
    U_filtered = U.copy()
    U_filtered[np.abs(f) > cutoff] = 0
    return U_filtered

# ===== Функция обработки сигнала для заданных параметров =====
def process_signal(a, t1, t2, b, c, d, T, dt, cutoff):
    """
    Генерирует сигналы, вычисляет Фурье-преобразование, применяет фильтр нижних частот и восстанавливает сигнал.
    Возвращает:
      t, g, u, u_filtered, f, U_spec, U_filtered_spec, G_spec
    """
    t, g, u = generate_signals(a, t1, t2, b, c, d, T, dt)
    f, U = compute_fft(u, dt)
    U_filtered = low_pass_filter(U, f, cutoff)
    u_filtered = inverse_fft(U_filtered)

    N = len(t)
    # Вычисляем модули спектров, нормированные по числу точек:
    G_spec = np.abs(np.fft.fftshift(np.fft.fft(g))) / N
    U_spec = np.abs(U) / N
    U_filtered_spec = np.abs(U_filtered) / N

    return t, g, u, u_filtered, f, G_spec, U_spec, U_filtered_spec

# ===== Функция Notch‑фильтра =====
def notch_filter(U, f, f0, notch_width):
    """
    Применяет notch-фильтр, обнуляя спектральные компоненты в окрестности частоты f0:
    обнуляются компоненты в диапазоне [f0 - notch_width, f0 + notch_width] и для отрицательных частот [-f0 - notch_width, -f0 + notch_width].
    """
    mask = np.ones_like(f, dtype=bool)
    # Обнуляем спектральные компоненты вокруг f0
    mask[np.logical_and(f >= f0 - notch_width, f <= f0 + notch_width)] = False
    # Обнуляем компоненты вокруг -f0
    mask[np.logical_and(f >= -f0 - notch_width, f <= -f0 + notch_width)] = False
    return U * mask

def task1_0(a, t1, t2, b_values, c=0.0, d=20.0, T=10.0, dt=0.01):
    """
    Генерирует сигнал, вычисляет Фурье-преобразование и строит графики временных сигналов и спектров.
    """
    t, g, _ = generate_signals(a, t1, t2, b_values[0], c, d, T, dt)
    plot_time_signals(t, [g], ['g(t)'], '')
    for b in b_values:
        t, g, u = generate_signals(a, t1, t2, b, c, d, T, dt)
        f, U = compute_fft(u, dt)
        N = len(t)
        U_spec = np.abs(U) / N

        plot_time_signals(t, [u], ['u(t)'], '')
        plot_spectra(f, [U_spec], ['Спектр u(t)'], '', freq_lim=10)


def task1_1(a, t1, t2, b_values, cutoff_values, c=0.0, d=20.0, T=10.0, dt=0.01, cutoff=5.0):
    """
    Реализует задание 1.1: генерирует сигнал, вычисляет Фурье-преобразование,
    фильтрует сигнал фильтром нижних частот и строит графики временных сигналов и спектров.
    """
    for b in b_values:
        for cutoff in cutoff_values:
            t, g, u, u_filtered, f, G_spec, U_spec, U_filtered_spec = process_signal(a, t1, t2, b, c, d, T, dt, cutoff)
            title_time = f"Временные сигналы (b={b}, ν₀={cutoff})"
            print(title_time)
            plot_time_signals(t, [g, u, u_filtered], ['g(t)', 'u(t)', 'Фильтрованный'], '')

            title_spec = f"Спектры сигналов (b={b}, ν₀={cutoff})"
            print(title_spec)
            plot_spectra(f, [G_spec, U_spec, U_filtered_spec], ['Спектр g(t)', 'Спектр u(t)', 'Спектр фильтрованного'], '', freq_lim=15)


a = 3              # Амплитуда прямоугольного сигнала
t1, t2 = -2, 1     # Интервал, где g(t) = a
T = 30          # Общая длительность временного интервала
dt = 0.001          # Шаг дискретизации
b_values = [0.1, 1.0, 3.0]
cutoff_values = [1.0, 5.0, 10.0]

# task1_0(a, t1, t2, b_values)
# task1_1(a, t1, t2, b_values, cutoff_values)

b_values = [0, 1, 2.0]
c_values = [0.5, 1]
d_values = [5.0, 10.0]
cutoff_values = [4.0, 8.0]
notch_width_values = [0.5]        # ширина notch‑фильтра

task1_2(a, t1, t2, b_values, c_values, d_values, cutoff_values, notch_width_values, T=T, dt=dt, freq_lim=5)