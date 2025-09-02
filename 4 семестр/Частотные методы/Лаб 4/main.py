import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры сигнала и фильтра
a = 1.0            # Амплитуда прямоугольного сигнала
t1, t2 = 1.0, 2.0  # Интервал, где g(t) = a
b = 0.2            # Амплитуда шума
c = 0.0            # Для данного задания c = 0 (синусоидальная помеха отсутствует)
T_const = 0.5      # Постоянная времени фильтра T
T_total = 5.0      # Общая длительность моделирования
dt = 0.001         # Шаг дискретизации

# Создание временного вектора
t = np.arange(0, T_total, dt)

# Генерация исходного сигнала g(t)
g = a * ((t >= t1) & (t <= t2)).astype(float)

# Генерация белого шума (равномерное распределение на [-1,1])
xi = 2 * np.random.rand(len(t)) - 1

# Формирование зашумлённого сигнала u(t) = g(t) + b*ξ(t)
u = g + b * xi

# Задание передаточной функции фильтра первого порядка: W1(p)=1/(T*p+1)
# В scipy.signal используем lti для определения системы
system = signal.lti([1], [T_const, 1])

# Моделирование отклика системы на входной сигнал u(t)
t_out, y, _ = signal.lsim(system, U=u, T=t)

# Построение графиков
plt.figure(figsize=(10, 5))
plt.plot(t, g, label='g(t) (исходный сигнал)', linewidth=1.5)
plt.plot(t, u, label='u(t) (зашумлённый сигнал)', linewidth=1.2)
plt.plot(t_out, y, label='y(t) (фильтрованный сигнал)', linewidth=1.5)
plt.xlabel('Время, с')
plt.ylabel('Амплитуда')
plt.title('Фильтр первого порядка: W₁(p)=1/(T*p+1)')
plt.legend()
plt.grid(True)
plt.show()
