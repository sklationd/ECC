from __future__ import annotations

# Calculate inverse of x in modulo p
def modinv(x, p):
    return pow(x, p - 2, p)


class EllipticCurve(object):
    def __init__(self, p, A, B):

        # Define curve
        self.p = p
        self.A = A
        self.B = B

        self.knownPoints = set([])

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

        # TODO: Implement double and add method

        if type(scalar) == int:
            result = self
            for _ in range(scalar - 1):
                result = result + self
            return result

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
