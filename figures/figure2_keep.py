import numpy as np
import argparse
from math import modf

import matplotlib as mpl
mpl.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": "\n".join([
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         ] )
}
         #r"\usepackage{cmbright}",
mpl.rcParams.update({'font.size': 9, "font.family": "serif",})
mpl.rcParams.update(pgf_with_pdflatex)
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker # for custom ticks 
from matplotlib import colors  # for custom colourmaps

from hilLib import i2xy, xy2i, hilbertDir

class ArgTuple(object):
    def __init__(self):
        pass

    def __call__(self, s):
        return tuple(float(x) for x in s.split(","))

def doArgs() :
  parser = argparse.ArgumentParser(description= "Plot hilbert")
  parser.add_argument('-o', '--outname', dest='oname', required=True, help='output file')
  parser.add_argument('-n', '--depth', dest='n',type=int, required=True, help='depth or hilbert scale')
  parser.add_argument('-c', '--circles', dest='circs', nargs="*", type=ArgTuple(), help='Circles to plot' )
  parser.add_argument('-hc', '--hilcolor', dest='hcol',type=str, required=True, help='colour of exterior Hilbert curve')
  parser.add_argument('-cap', '--caption', dest='caption',type=str, help='figure captions')
  return parser.parse_args()


# sig:   matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)

def savefig(fig, name) :
    fig.savefig(name+".pdf", bbox_inches = 'tight')
    fig.savefig(name+".pgf", bbox_inches = 'tight')
    fig.savefig(name+".svg", bbox_inches = 'tight')

"""
X = 0;
Y = radius;
d = 1 - radius;
draw8Points(X, Y);
while(Y > X)

if (d< 0)

add 2 * X + 3 to d
add 1 to X

else

add 2 * (X-Y) + 5 to d
add 1 to X
subtract 1 from Y

draw8Points(X, Y);
"""

def circ(ox,oy, r, n) :
    r = r//2
    
    def addPoint(pl, x, y) :
        pl.extend([
                  (ox+2*x,oy+2*y), 
                  (ox-2*x,oy+2*y), 
                  (ox+2*x,oy-2*y), 
                  (ox-2*x,oy-2*y), 
                  (ox+2*y,oy+2*x), 
                  (ox-2*y,oy+2*x), 
                  (ox+2*y,oy-2*x), 
                  (ox-2*y,oy-2*x),
                  ])
    x = 0
    y = r 
    d = 1 - r

    p = []
    addPoint(p, x,y )
    while y > x :
        if d < 0 :
            d = d + 2*x + 3
            x = x + 1
        else:
            d = d + 2*(x-y) + 5
            x = x + 1
            y = y - 1
        addPoint(p,x,y )
    
    ilist = [ xy2i( x,y, n) for x,y in p ]

    return sorted(set(ilist))

        
def plotCircle(ax, ilist, n, ox, oy, r, m):
    
    ss = (1 << m) # m = 5, ss = 32

    ax.add_patch(plt.Circle(
        (ox/ (1<<m), oy/ (1<<m)), r/ (1<<m), facecolor='none', edgecolor='black', alpha=1.0, lw = 64/ss, zorder=10,
        ))

    xylist = [ i2xy(i, n) for i in ilist ]
    xy = np.array(xylist) / (1<<n)
    ax.scatter( xy[:,0], xy[:,1], s = 512/ss, c = 'black', zorder=8 )


def renderCircles(ax, circs, n) :
    circsW = [ (x*(1<<n), y*(1<<n), r*(1<<n), n) for x,y,r in circs ]

    circIs = [ circ(*c) for c in circsW ]

    for s, c in zip(circIs, circsW) :
        plotCircle(ax, s, n, *c)

    return circIs


def main() :

    args = doArgs()
    circs = args.circs
    n = args.n    

    fig,ax = plt.subplots(1, 1)
    
    l = 1 << (n*2)

    #ilist = np.arange(l) / l

    bpl = []
    if args.circs:
        for m in renderCircles(ax, args.circs, n):
            bpl.extend(m)

    # need to switch to integers for colouring
    Ilist = [0] + [ i * l for i in bpl ] + [l-1]

    cols = [ 'grey', 'blue' ]

    for i in range(len(Ilist)-1) :
        a = Ilist[i]
        b = Ilist[i+1]
        ilist = range(int(a), int(b)+1)
        print(ilist)
        xy = np.array( [ i2xy(i/l, n) for i in ilist ] )
        dxdy = np.array( [ hilbertDir( (i/l), n) for i in ilist] )

        #print(f"{xy=}")
        #print(f"{dxdy=}")
        xy = xy / (1<<n)
        dxdy = dxdy/ (1<<n) / 2

        ax.plot( xy[:,0], xy[:,1], c=cols[ i & 1], zorder=5 , lw= 64/(1<<n))
        ax.scatter( xy[:,0] + dxdy[:,0] , xy[:,1] + dxdy[:,1] , zorder = 20, s = 1)

    ax.set_xlim( (-1,1) )
    ax.set_ylim( (-1,1) )
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.axis('off')
    ax.set_box_aspect(1)

    if args.caption :
        plt.figtext(0.5, 0.05, args.caption, wrap=True, horizontalalignment='center', fontsize=12)

    savefig( fig, args.oname )


main()

"""
x/w=-0.21875 y/w=0.15625 r/w=0.5
x/w=0.34375 y/w=0.46875 r/w=0.375
x/w=0.03125 y/w=-0.46875 r/w=0.375

    circs = [
        (-7, 5, 16, n),
        (11, 15, 12, n),
        ( 1,-15, 12, n),
        ]
        """
