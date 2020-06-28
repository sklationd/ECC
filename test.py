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


# valid : Secp256K1(It is exactly bitcoin ECC)
p5 = 115792089237316195423570985008687907853269984665640564039457584007908834671663
A5 = 0
B5 = 7
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

# Make Secp256K1 ECC
try:
    bitcoinCurve = EllipticCurve(p5, A5, B5)
except Exception as ex:
    print("[Error]: An error occured: ", ex)


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


# Test big prime ecc(Secp256K1)

Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

P = Point(bitcoinCurve, Gx, Gy)

# (89565891926547004231252920425935692360644145829622209833684329913297188986597,
#  12158399299693830322967808612713398636155367887041628176798871954788371653930)
print(2*P)

# order of Secp256K1, result of below expression should be identity
order = 115792089237316195423570985008687907852837564279074904382605163141518161494337 # IDENTITY
print(order*P)

