import random

LIMIT = pow(10, 9)

def save_key_to_file(a, b, filename):
    with open(filename, 'w+') as f:
        f.write('{a}\n{b}\n'.format(a=a, b=b))

def euclidean_alorithm(a, n):
    Gprev = n
    G = a
    while G != 0:
        Gnext = Gprev % G
        Gprev = G
        G = Gnext
    return Gprev

def extended_euclidean_alorithm(a, n):
    Gprev = n
    G = a
    Vprev = 0
    V = 1
    i = 1

    while G != 0:
        y = Gprev // G
        Gnext = Gprev - y * G
        Gprev = G
        G = Gnext
        Vnext = Vprev - y * V
        Vprev = V
        V = Vnext
        i = i + 1
    
    x = Vprev

    if x >= 0:
        inv_a = x
    else:
        inv_a = x + n

    if Gprev == 1:
        return inv_a
    else:
        return None

def miller_rabin_test(n, a):
    b = n - 1
    ile_cyfr = 0
    while True:
        if b < pow(2, ile_cyfr):
            break
        else:
            ile_cyfr+=1
    d = 1
    i = ile_cyfr
    while i >= 0:
        x = d
        d = d * d % n
        if d == 1 and x != 1 and x != (n-1):
            return True
        if b // pow(2, i) == 1:
            b = b - pow(2, i)
            d = d * a % n
        i-=1
    
    if d != 1:
        return True
    else:
        return False

def generate_prime(limit):
    prime = random.randint(1, limit)
    k = 0
    while k<30:
        random_number = random.randint(1, prime-1)
        if not miller_rabin_test(prime, random_number):
            k+=1
        else:
            prime = random.randint(1, limit)
            k = 0
    return prime

def generate_keys():
    p = generate_prime(LIMIT)
    print('Generated p: {p}'.format(p=p))
    while True:
        q = generate_prime(LIMIT)
        if p != q:
            print('Generated q: {q}'.format(q=q))
            break
    n = p * q
    print('Generated n: {n}'.format(n=n))
    while True:
        e = random.randint(0, LIMIT)
        if euclidean_alorithm(e, (p-1)*(q-1)) == 1 and extended_euclidean_alorithm(e, (p-1)*(q-1)):
            print('Generated e: {e}'.format(e=e))
            d = extended_euclidean_alorithm(e, (p-1)*(q-1))
            print('Generated d: {d}'.format(d=d))
            break
    
    save_key_to_file(e, n, 'private.key')
    save_key_to_file(d, n, 'public.key')


generate_keys()