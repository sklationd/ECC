##########  Initialize  ##########

from EC import EllipticCurve, Point

p1 = 37
A1 = -5
B1 = 8

p2 = 23
A2 = -1
B2 = 0

# invalid : zero discriminant
p3 = 23
A3 = -3
B3 = 2

# invalid : non prime p
# TODO: implement prime checker
p4 = 16
A4 = -1
B4 = 0


##########    Build     ##########

# Make valid ECC
try:
    curve = EllipticCurve(p1, A1, B1)
except Exception as ex:
    print("[Error]: An error occured: ", ex)

try:
    otherCurve = EllipticCurve(p2, A2, B2)
except Exception as ex:
    print("[Error]: An error occured: ", ex)

# Make invalid ECC, it should raise an error
try:
    invalid_d_Curve = EllipticCurve(p3, A3, B3)
except Exception as ex:
    print("[Error]: An error occured: ", ex)

# TODO: implement prime checker, if should raise an error
try:
    invalid_p_Curve = EllipticCurve(p4, A4, B4)
except Exception as ex:
    print("[Error]: An error occured:", ex)


##########  Test case  ###########

P = Point(curve, 6, 3)
Q = Point(curve, 9, 10)
O = Point(curve, inf=True)

P_ = Point(otherCurve, -1, 0)

# Test basic arithmetic
print(P + P)  # (35,11)
print(P + Q)  # (11,10)
print(P - Q)  # (12,23)
print(-P + Q)  # (12,14)
print(-P - Q)  # (11,27)
print(-(P + Q))  # (11,27)
print(P * 9)  # (11,27)
print(9 * P)  # (11,27)
print(3 * P + 4 * Q)  # (31,28)

# Test for infinite point(identity)
print(P - P)  # IDENTITY
print(P + O)  # (6,3)
print(O + P)  # (6,3)
print(O + O)  # IDENTITY
print(3 * O)  # IDENTITY
print(-O)  # IDENTITY

# Try to add two different curve point, should raise an error
try:
    print(P + P_)
except Exception as ex:
    print("[Error]: An error occured: ", ex)
