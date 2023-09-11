Pmin = 50   # Минимальный %
Vmin = 50   # Минимальное число
Pmax = 250  # Максимальный %
Vmax = 250   # Максимальное число
C =    -100 # Текущее значение
T = 150     # Целевое значение

if C == T:
    p =100
    x = 1

elif Pmin is None and Vmin is None:
    p = ((Pmax - 100) / (Vmax - T)) * C + (Pmax - ((Pmax - 100) / (Vmax - T) * Vmax))
    x = 2

elif Pmax is None and Vmax is None:
    p = ((100-Pmin)/(T-Vmin)) * C + (100 - ((100-Pmin)/(T-Vmin) * T))
    x = 3

elif Vmax<Vmin and C <= Vmax:
    p = Pmax
    x = 4
elif Vmax<Vmin and C<T:
    p = ((100-Pmin)/(T-Vmin)) * C + (100 - ((100-Pmin)/(T-Vmin) * T))
    x = 5
elif Vmax<Vmin and C>T:
    p= ((Pmax - 100) / (Vmax - T)) * C + (Pmax - ((Pmax - 100) / (Vmax - T) * Vmax))
    x = 6
elif C > Vmax and Vmax>Vmin:
    p = Pmax
    x = 7
elif Pmax == 0 or C<T:
    p = ((100-Pmin)/(T-Vmin)) * C + (100 - ((100-Pmin)/(T-Vmin) * T))
    x = 8
elif Pmin == 0 or C>T:
    p= ((Pmax - 100) / (Vmax - T)) * C + (Pmax - ((Pmax - 100) / (Vmax - T) * Vmax))
    x = 9

print(p)
print(x)





