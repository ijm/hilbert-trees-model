from math import modf

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

def i2xyStep(h) :
  (i, x, y, r, w ) = h
  i, q = modf(i * 4.)
  x <<= 1 
  y <<= 1
  q = int(q)
  
  if q == 0   : # - -
      return (i,  y-1,  x-1, r^1, w+1)

  elif q == 1 : # - +
      return (i,  x-1,  y+1, r,   w+1)

  elif q == 2 : # + +
      return (i,  x+1,  y+1, r,   w+1)

  elif q == 3 : # + -
      return (i, -y+1, -x-1, r^2, w+1)

  else :
     raise ValueError("Mod 4 returned something not mod 4")


def xy2iStep(h)  :
    def sgn(a) :
        return bool(a>0) - bool(a<0)

    (i, x, y, r, w ) = h
    nw = w-1
    
    qx = sgn(x)
    qy = sgn(y)

    #print( f"{x=} {y=} {qx=} {qy=}")

    x = x - (qx << nw)
    y = y - (qy << nw)
    
    i *= 4.

    #q = (qx & 3) | ((qy & 3) <<2 )
    # Oh python.


    if qx<0 and qy <= 0 : # - -
        return (i+0,  y,  x, r^1, nw)

    elif qx<=0 and qy>0 : # - + 
        return (i+1,  x,  y, r,   nw)

    elif qx>0 and qy>=0 : # + + 
        return (i+2,  x,  y, r,   nw)

    elif qx>=0 and qy<0 : # + -
        return (i+3, -y, -x, r^2, nw)

    else:
        raise ValueError("0,0 is a problem")

def i2xy(i, n):
    def i2xyLoop(h, m) : # kept recursive to match from other ports
        return h if m == 0 else i2xyLoop( i2xyStep(h), m-1)

    (i, x, y, r, m) = i2xyLoop( (i,0,0,0,0), n)

    if m != n :
        raise ValueError("Depth missmatch")

    #x /= (1 << n)
    #y /= (1 << n)
    
    if   r == 0 :
        return ( x,  y, n)
    elif r == 1 :
        return ( y,  x, n)
    elif r == 2 :
        return (-y, -x, n)
    elif r == 3  :
        return (-x, -y, n)
    else:
        raise ValueError("r isn't 0-4 !?")

    
def xy2i (x,y, n) :
    def xy2iLoop(h, m) : # kept recursive to match from other ports
        return h if m == 0 else xy2iLoop( xy2iStep(h), m-1)

    (i, x, y, r, m) = xy2iLoop( (0, x+0.01, y+0.01, 0, n) , n)
    return i / (1<<(2*n))

#-----------------------------
# Derived from the code in [JJJMC] ~ p. 84
# This much easyer to do this in the integer domain
# and I'll assume these ints are large enough.

def hilbertParity(I) :
    I = I & ((I & 0xaaaaaaaaaaaaaaaa) >> 1);
    I = I ^ (I>>2);
    I = I ^ (I>>4);
    I = I ^ (I>>8);
    I = I ^ (I>>16);
    I = I ^ (I>>32);
    return  I & 1;


def hilbertDir(i, n, di) :


    """
    We need to return the flip state :
       0 : right  dx=+1  dy= 0
       1 : down   dx= 0  dy=-1
       2 : up     dx= 0  dy=+1
       3 : left   dx=-1  dy= 0
    for n even, and flip xy for n odd
    """

    I = int( i * ( 1<<(2*n) ) ) +1 + di

    p = hilbertParity(I)  # 0 -> (dx+dy)==-1 ; 1 -> (dx+dy)==+1
    m = hilbertParity(-I) # 0 -> (dx-dy)==-1 ; 1 -> (dx-dy)==+1

    d =  p ^ (m<<1)

    return [ (0,1), (-1,0), (1,0), (0,-1) ][d] if n&1 else [ (1,0), (0,-1), (0,1), (-1,0) ][d] 

#-----------------------------

def test(n, printthem) :
    # Obviously not exaustive.
    w = 1<<n
    ilist = [ i / w for i in range(w) ]

    xylist = [ i2xy(i, n) for i in ilist ]
    jlist = [ xy2i(x,y,m) for x,y,m in xylist ]
   
    if (printthem) :
      print(f"{xylist=}")
      print(f"{ilist=}")
      print(f"{jlist=}")

    print(f"{w=} {ilist == jlist}")

def tests() :
    test(4,True)
    #test(8,False)
    #test(10,False)
    #test(16,False)

if __name__ == "__main__" :
    tests()


