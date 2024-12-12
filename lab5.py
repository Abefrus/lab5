import random
from math import gcd

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

print("\nЗавдання 1:\n")

p = int(input("Введіть непарне натуральне число більше 3: "))
k = int(input("Введіть кількість перевірок: "))
result = miller_rabin_test(p, k)
print(result)

print("\nЗавдання 2:\n")

def generate_large_prime(bits, k=5):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if miller_rabin_test(n, k) == f"Число просте з ймовірністю {1 - (0.25 ** k):.6f}":
            return n

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def generate_rsa_keys(bits):
    print("Генерація великих простих чисел...")
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  
    if gcd(e, phi) != 1:
        raise ValueError("e не взаємно просте з phi")

    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    return [mod_pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(mod_pow(char, d, n)) for char in ciphertext])


bits = 1024  # Розмір ключа в бітах
public_key, private_key = generate_rsa_keys(bits)
print("Відкритий ключ:", public_key)
print("Закритий ключ:", private_key)

message = input("Введіть повідомлення для шифрування: ")
encrypted_message = encrypt(message, public_key)
print("Зашифроване повідомлення:", encrypted_message)
decrypted_message = decrypt(encrypted_message, private_key)
print("Розшифроване повідомлення:", decrypted_message)