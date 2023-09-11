Pmin = 80   # Минимальный %
Vmin = 80   # Минимальное число
Pmax = 120  # Максимальный %
Vmax = 120   # Минимальное число
C = 110     # Текущее значение
T = 100     # Целевое значение


#elif Pmax == 0 or C<T:
# p = ((100-Pmin)/(T-Vmin)) * C + (100 - ((100-Pmin)/(T-Vmin) * T))

#elif Pmin == 0 or C>T:
p= ((Pmax - 100) / (Vmax - T)) * C + (Pmax - ((Pmax - 100) / (Vmax - T) * Pmax))


print(p)