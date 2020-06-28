# ECC
Implementation of Elliptic Curve on integer field with python3

## Environment
```console
$ python3 --version
Python 3.7.5
```

## Usage(Test)
```console
$ python3 test.py
```

- Expected output
  ```
    [Error]: An error occured:  Given A, B do not satisfy elliptic curve condition(discriminant is not 0)
    (35,11)
    (11,10)
    (12,23)
    (12,14)
    (11,27)
    (11,27)
    (22,36)
    (22,36)
    (31,28)
    IDENTITY
    (6,3)
    (6,3)
    IDENTITY
    IDENTITY
    IDENTITY
    [Error]: An error occured:  Can not add two different curve's point
    (89565891926547004231252920425935692360644145829622209833684329913297188986597,12158399299693830322967808612713398636155367887041628176798871954788371653930)
    IDENTITY
  ```

## TODO
- [ ] Implement prime checker (This may not be necessary).
- [ ] Build a p2p key exchange model of [Diffie Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) based on ECC.
- [ ] Add a description about structure of `Point` and `EllipticCurve`.

## Reference
- [ECC](https://www.math.brown.edu/~jhs/Presentations/WyomingEllipticCurve.pdf)
- [Montgomery ladder](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication)
- [Secp256k1](https://en.bitcoin.it/wiki/Secp256k1)