from __future__ import annotations

# Calculate inverse of x in modulo p
def modinv(x, p):
    return pow(x, p - 2, p)

# Convert decimal number n to binary number(string)
def dec2bin(n):
    return bin(n)[2:]

# Montgomery ladder algorithm
# The Montgomery ladder approach computes the point multiplication in a fixed amount of time.
# This can be beneficial when timing or power consumption measurements are exposed to an attacker
# performing a side-channel attack. The algorithm uses the same representation as from double-and-add.
def mont_mul(scalar_bin, point:Point):
    curve = point.getCurve()

    # '10010' -> [1,0,0,1,0]
    b = [int(ni) for ni in scalar_bin] 
    
    # identity point
    R0 = Point(curve, inf=True)

    # input point
    R1 = Point(curve, x=point.getX(), y=point.getY())

    for d_i in b:
        if d_i == 0:
            R1 = R0 + R1
            R0 = 2 * R0 
        else:
            R0 = R0 + R1
            R1 = 2 * R1
    
    return R0


class EllipticCurve(object):
    def __init__(self, p, A, B):

        # Define curve
        self.p = p
        self.A = A
        self.B = B

        # TODO : Check vulnerability of ECC


        # Calculate a discriminant
        self.d = self.calD()

        # TODO : Check p is really a prime
        self.prime = True

        if self.prime is not True:
            raise Exception("Given p is not a prime number")

        if self.d == 0:
            raise Exception(
                "Given A, B do not satisfy elliptic curve condition(discriminant is not 0)"
            )

    def __eq__(self, EC: EllipticCurve):
        p = self.getP() == EC.getP()
        A = self.getA() == EC.getA()
        B = self.getB() == EC.getB()

        return p and A and B

    def calD(self):
        p = self.getP()
        A = self.getA()
        B = self.getB()

        return -16 * (4 * (A ** 3) + 27 * (B ** 2))

    def getA(self):
        return self.A

    def getB(self):
        return self.B

    def getP(self):
        return self.p


class Point(object):
    def __init__(self, curve: EllipticCurve, x=0, y=0, inf=False):

        self.curve = curve
        self.inf = inf

        if not self.isInf():
            p = self.curve.getP()
            self.x = x % p
            self.y = y % p

            if not self.isInCurve():
                raise Exception("Given x, y does not lie in the curve")

    def __str__(self):

        if self.isInf():
            return "IDENTITY"

        x = self.getX()
        y = self.getY()

        result = f"({x},{y})"

        return result

    def __eq__(self, point: Point):

        if self.isInf():
            if point.isInf():
                return True
            else:
                return False

        x1 = self.getX()
        y1 = self.getY()
        x2 = point.getX()
        y2 = point.getY()

        return (x1 == x2) and (y1 == y2)

    def __neg__(self):
        if self.isInf():
            return self

        x = self.getX()
        y = -self.getY()

        return Point(self.curve, x, y)

    def __add__(self, point: Point):
        if self.curve != point.curve:
            raise Exception("Can not add two different curve's point")

        # One of points is infinite point
        if point.isInf():
            return self
        if self.isInf():
            return point

        # Result is infinite point
        if self == -point:
            return Point(self.curve, inf=True)

        x1 = self.getX()
        y1 = self.getY()

        x2 = point.getX()
        y2 = point.getY()

        samePoint = x1 == x2 and y1 == y2

        p = self.curve.getP()
        A = self.curve.getA()
        B = self.curve.getB()

        if samePoint:
            L = ((3 * x1 ** 2 + A) * modinv(2 * y1, p)) % p
            M = ((-(x1 ** 3) + A * x1 + 2 * B) * modinv(2 * y1, p)) % p
        else:
            L = ((y2 - y1) * modinv(x2 - x1, p)) % p
            M = ((y1 * x2 - y2 * x1) * modinv(x2 - x1, p)) % p

        resultX = (L * L - x1 - x2) % p
        resultY = (-(L ** 3) + L * (x1 + x2) - M) % p

        return Point(self.curve, resultX, resultY)

    def __sub__(self, point: Point):
        return self + (-point)

    def __mul__(self, scalar: int):

        if type(scalar) == int:
            if self.isInf():
                return self

            if scalar == 2:
                return self + self

            else:
                # get binary expression of scalar with string
                scalar_bin = dec2bin(scalar)    

                # multiplication with montgomery ladder algorithm 
                return mont_mul(scalar_bin, self)

        else:
            raise TypeError(
                "unsupported operand type(s) for *: 'Point' and " + type(other).__name__
            )

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    # API
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCurve(self):
        return self.curve

    def isInf(self):
        return self.inf

    def isInCurve(self):
        p = self.curve.getP()
        A = self.curve.getA()
        B = self.curve.getB()

        x = self.getX() % p
        y = self.getY() % p

        lhs = (y ** 2) % p
        rhs = (x ** 3 + A * x + B) % p

        return lhs == rhs
