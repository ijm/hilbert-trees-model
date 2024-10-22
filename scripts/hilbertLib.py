from math import modf
from typing import List, Tuple

"""
   Hilbert indexing on the half open interval [0,1) mapped to x,y on the
   open regeon (-1,1)^2

   The index is stored as a float, the 2D XY coordinate as integers in a
   homogenious 3-tupple (X, Y, 1<<W), or as the coresponding (x, y)

   This mapping can be done by bit flipping [JJJMC] but the extra work in unpacking and
   repacking pairs of bits is extensive. When optimized (in C++ or OCMAL) this routine
   is only slightly slower, and much easier to track and debug interactions. (sometime
   I'll even back that up with some proper profiles). In python I've no idea.

   Like the bit flipping it works by following the affine transformations
   at each level of the fractal and keeping track of which reflections
   have been done at each level.

   These routines were ported form the OCAML and C++ routines.
"""

HilbertPointType = Tuple[float, int, int, int, int]


def i2xyStep(hilbertPoint: HilbertPointType) -> HilbertPointType:
    (i, x, y, r, w) = hilbertPoint
    i, q = modf(i * 4.)
    x <<= 1
    y <<= 1
    q = int(q)

    if q == 0:  # - -
        return (i, y - 1, x - 1, r ^ 1, w + 1)

    elif q == 1:  # - +
        return (i, x - 1, y + 1, r, w + 1)

    elif q == 2:  # + +
        return (i, x + 1, y + 1, r, w + 1)

    elif q == 3:  # + -
        return (i, -y + 1, -x - 1, r ^ 2, w + 1)

    else:
        raise ValueError("Mod 4 returned something not mod 4")


def xy2iStep(hilbertPoint: HilbertPointType) -> HilbertPointType:
    def sgn(a):
        return bool(a > 0) - bool(a < 0)

    (i, x, y, r, w) = hilbertPoint
    nw = w - 1

    qx = sgn(x)
    qy = sgn(y)

    # print( f"{x=} {y=} {qx=} {qy=}")

    x = x - (qx << nw)
    y = y - (qy << nw)

    i *= 4.

    # q = (qx & 3) | ((qy & 3) <<2 )
    # Oh python.

    if qx < 0 and qy <= 0:  # - -
        return (i + 0, y, x, r ^ 1, nw)

    elif qx <= 0 and qy > 0:  # - +
        return (i + 1, x, y, r, nw)

    elif qx > 0 and qy >= 0:  # + +
        return (i + 2, x, y, r, nw)

    elif qx >= 0 and qy < 0:  # + -
        return (i + 3, -y, -x, r ^ 2, nw)

    else:
        raise ValueError("0,0 is a problem")


def i2xy(fIndex: float, depth: int) -> Tuple[int, int, int]:
    def i2xyLoop(hilberPoint, m):  # kept recursive to match from other ports
        return hilberPoint if m == 0 else i2xyLoop(i2xyStep(hilberPoint), m - 1)

    (i, x, y, r, m) = i2xyLoop((fIndex, 0, 0, 0, 0), depth)

    if m != depth:
        raise ValueError("Depth missmatch")

    # x /= (1 << n)
    # y /= (1 << n)

    if r == 0:
        return (x, y, depth)
    elif r == 1:
        return (y, x, depth)
    elif r == 2:
        return (-y, -x, depth)
    elif r == 3:
        return (-x, -y, depth)
    else:
        raise ValueError("r isn't 0-4 !?")


def xy2i(x: int, y: int, depth: int) -> float:
    def xy2iLoop(hilbertPoint, m):  # kept recursive to match from other ports
        return hilbertPoint if m == 0 else xy2iLoop(xy2iStep(hilbertPoint), m - 1)

    (i, x, y, r, m) = xy2iLoop((0, x + 0.01, y + 0.01, 0, depth), depth)
    return i / (1 << (2 * depth))


# -----------------------------
# Derived from the code in [JJJMC] ~ p. 84
# This much easyer to do this in the integer domain
# and I'll assume these ints are large enough.

def hilbertParity(iIndex: int) -> int:
    iIndex = iIndex & ((iIndex & 0xaaaaaaaaaaaaaaaa) >> 1)
    iIndex = iIndex ^ (iIndex >> 2)
    iIndex = iIndex ^ (iIndex >> 4)
    iIndex = iIndex ^ (iIndex >> 8)
    iIndex = iIndex ^ (iIndex >> 16)
    iIndex = iIndex ^ (iIndex >> 32)
    return iIndex & 1


def hilbertDir(fIndex: float, depth: int, direction: int) -> Tuple[int, int]:
    """
    We need to return the flip state :
       0 : right  dx=+1  dy= 0
       1 : down   dx= 0  dy=-1
       2 : up     dx= 0  dy=+1
       3 : left   dx=-1  dy= 0
    for n even, and flip xy for n odd
    """

    iIndex = int(fIndex * (1 << (2 * depth))) + 1 + direction

    p = hilbertParity(iIndex)  # 0 -> (dx+dy)==-1 ; 1 -> (dx+dy)==+1
    m = hilbertParity(-iIndex)  # 0 -> (dx-dy)==-1 ; 1 -> (dx-dy)==+1

    d = p ^ (m << 1)

    return ([(0, 1), (-1, 0), (1, 0), (0, -1)][d]
            if depth & 1 else
            [(1, 0), (0, -1), (0, 1), (-1, 0)][d])


# -----------------------------
def test(depth: int, printthem: bool):
    # Obviously not exaustive.
    w = 1 << depth
    fIndexListA: List[float] = [i / w for i in range(w)]

    xyList: List[Tuple[int, int, int]] = [i2xy(fIndex, depth) for fIndex in fIndexListA]
    fIndexListB: List[float] = [xy2i(x, y, m) for x, y, m in xyList]

    if (printthem):
        print(f"{xyList=}")
        print(f"{fIndexListA=}")
        print(f"{fIndexListB=}")

    print(f"{w=} {fIndexListA == fIndexListB}")


def tests():
    test(4, True)
    # test(8, False)
    # test(10, False)
    # test(16, False)


if __name__ == "__main__":
    tests()


