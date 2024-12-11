import random

def mod_pow(a, b, p):
    result = 1
    base = a % p
    while b > 0:
        if b % 2 == 1:
            result = (result * base) % p
        base = (base * base) % p
        b //= 2
    return result

def miller_rabin_test(p, k):
    if 0>= p<=3:
        return "Введені дані не підходять до умови"
    if p % 2 == 0:
        return "Введені дані не підходять до умови"
    
    d = p - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, p - 2) 
        x = mod_pow(a, d, p)

        if x == 1 or x == p - 1:
            continue

        is_composite = True
        for _ in range(1, r):
            x = mod_pow(x, 2, p)
            if x == p - 1:
                is_composite = False
                break

        if is_composite:
            return "Число складене"

    probability = 1 - (0.25 ** k)
    return f"Число просте з ймовірністю {probability:.6f}"

p = int(input("Введіть непарне натуральне число більше 3: "))
k = int(input("Введіть кількість перевірок: "))
result = miller_rabin_test(p, k)
print(result)
