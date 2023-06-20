import random
import sympy
from numpy.random import randint
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def keys_generator(numbers):
    def gcd(a, b):
        if b > 0:
            return gcd(b, a % b)
        return a

    def find_mod_inverse(a, m):
        if gcd(a, m) != 1:
            return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m

        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def randomPrimeNumbers(numbers_to_generator):
        p = 0
        q = 0
        flag = False
        for number in numbers_to_generator:
            if sympy.isprime(number):
                flag = True
                p = number
                break

        if flag:
            q = sympy.prevprime(p)
        else:
            random = randint(0, len(numbers_to_generator) - 1)
            x = numbers_to_generator[random]
            p = sympy.prevprime(x)
            q = sympy.prevprime(p)

        return p, q

    def generateKeys():
        p, q = randomPrimeNumbers(numbers)
        n = p * q
        euler = (p - 1) * (q - 1)
        e = 3
        while True:
            e = random.randrange(1, euler)
            g = gcd(e, euler)
            if g == 1:
                break

        d = find_mod_inverse(e, euler)
        dmp1 = int(d % (p - 1))
        dmq1 = int(d % (q - 1))
        iqmp = int(pow(q, -1, p))
        public_numbers = rsa.RSAPublicNumbers(e=e, n=n)
        private_key = rsa.RSAPrivateNumbers(
            p=p,
            q=q,
            d=d,
            dmp1=dmp1,
            dmq1=dmq1,
            iqmp=iqmp,
            public_numbers=public_numbers).private_key()

        public_key = public_numbers.public_key()

        return private_key, public_key

    def private_key_to_pem(private_key):
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return private_key_pem

    def public_key_to_pem(public_key):
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return public_key_pem

    private_key, public_key = generateKeys()
    print("The keys have been generated")

    private_key_pem = private_key_to_pem(private_key)
    with open("private_key.pem", "wb") as pem_file:
        pem_file.write(private_key_pem)

    public_key_pem = public_key_to_pem(public_key)
    with open("public_key.pem", "wb") as pem_public_file:
        pem_public_file.write(public_key_pem)

    print("The keys have been saved")