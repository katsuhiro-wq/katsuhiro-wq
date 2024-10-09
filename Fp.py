import random


def main():
    print("This is a source cord for Prime Field")


def Fp_random(p: int) -> int:
    return random.randint(0, p - 1)  # 0からp-1までの整数、すなわちFpの元をランダムに返す


def Fp_add(a: int, b: int, p: int) -> int:
    ans = a + b
    if ans >= p:
        ans = ans - p  # a,b<pならば、a+b<2pとなるので、%pとせずともans>pの時にans-pとすればよい
    return ans


def Fp_sub(a: int, b: int, p: int) -> int:
    ans = a - b
    if ans < 0:
        ans = ans + p  # a,b<pならば、-p<a-b<pとなるので、%pとせずともans<0の時にans+pとすればよい
    return ans


def Fp_mul(a: int, b: int, p: int) -> int:
    ans = (a * b) % p  # 通常の乗算の後にmod pを行う
    return ans


def Fp_pow(a: int, b: int, p: int) -> int:
    ans = pow(a, b, p)  # Pythonのpow関数はpow(a,b,p)でa**b%pを計算してくれる
    return ans


def Fp_inv(a: int, p: int) -> int:
    ans = Fp_pow(
        a, p - 2, p
    )  # フェルマーの小定理より、a^(p-1)=1(mod p)なので、a^(p-2)=a^(-1)(mod p)となる
    return ans


def is_prinme(num: int) -> int:
    if num == 2:
        return True
    if num > 2 and num & 1 == 0:
        return False

    s, t = 0, num - 1
    while t & 1 == 0:
        s, t = s + 1, t >> 1
    a = random.randint(1, num - 1)
    if pow(a, t, num) == 1:
        return True
    for i in range(0, s):
        if pow(a, pow(2, i) * t, num) == num - 1:
            return True
    return False


def Fp_legendre(a: int, p: int) -> bool:
    tmp = Fp_pow(a, (p - 1) // 2, p)
    if tmp == 1 or tmp == 0:
        return True
    else:
        return False


def Fp_sqrt(a: int, p: int) -> int:
    if p % 4 == 1:
        return Fp_pow(a, (p + 1) // 4, p)
    else:
        n = 0
        while True:
            n = Fp_random(p)
            if not Fp_legendre(n, p):
                break
        e = 0
        tmp = p - 1
        while tmp % 2 != 1:
            tmp = tmp // 2
            e = e + 1
        q = (p - 1) // pow(2, e)
        y = Fp_pow(n, q, p)
        r = e
        l = (q - 1) // 2
        x = Fp_pow(a, l, p)
        b = (a * Fp_pow(x, 2, p)) % p
        x = (a * x) % p
        while b % p != 1:
            m = 0
            while True:
                c = pow(2, m)
                if pow(b, c, p) == 1:
                    break
                m = m + 1
            t = Fp_pow(2, (r - m - 1) % p, p)
            t = Fp_pow(y, t, p)
            y = Fp_pow(t, 2, p)
            r = m
            x = (x * t) % p
            b = (b * y) % p
        return x


if __name__ == "__main__":
    main()
