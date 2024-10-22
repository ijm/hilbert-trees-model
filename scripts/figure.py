import numpy as np
# from math import modf, sqrt
from matplotlib.pyplot import Circle, figtext
from operator import itemgetter

from figureArguments import doArgs
from hilbertLib import i2xy, xy2i, hilbertDir
from figurePlotSetup import hozSubPlots, savefig

circleColors = [
    (0.3, 0.3, 0.3, 1.0),
    (1., 0., 0., 0.6),
    (0., 1., 0., 0.6),
    (0., 0., 1., 0.6),
]
stackColors = [
    (0.6, 0.6, 0.6, 1.0),

    (1., 0., 0., 1.0),
    (0., 0.8, 0., 1.0),

    (0.8, 0.8, 0., 1.0),

    (0., 0., 1., 1.0),
    (1., 0., 1., 1.0),
    (0., 1., 1., 1.0),

    (1., 1., 1., 1.0),
]


def genCircle(ax, popts, ox, oy, r0, n, cid):
    """
    Generate the list of indices for a circle, along with debuging and
    pedalogical stuff.

    Algorithm:
        1. Walk 1/8 of a circle for 'plotting' its boundry like pixels.
        2. look at each of the 8 points (from symetry) to make the whole
           circle:
          a. compute the index for the point
          b. check if the curve actualy crosses the boundry at this point
             by looking at the two adjacent half-way points on the curve.
             (if they are both inside or both outside then DONT add the point)
        3. uniquly sort the points that were added and build in the id and
           entry/exit flag
        4. return the sorted list.
    """

    def pplot(x, y, d):
        ax.scatter([(ox + x) / (1 << n)], [(oy + y) / (1 << n)],
                   c='g' if d else 'r', zorder=100, s=256 / (1 << n))

    def checkBoundryAndAdd(ps, ox, oy, r, x, y, n):
        def check(u, v):
            # s = u * u + v * v
            return (u * u + v * v < r0 * r0)

        i = xy2i(ox + x, oy + y, n)

        if popts.noMerge:
            ps.add(i)
        else:
            (dxN, dyN) = hilbertDir(i, n, 0)
            (dxP, dyP) = hilbertDir(i, n, -1)
            q = 1
            iN = check(x + q * dxN, y + q * dyN)
            iP = check(x - q * dxP, y - q * dyP)
            if popts.showCross:
                # iO = check(x, y)
                # pplot(x, y, iO)
                # pplot(x + q*dxN, y + q*dyN, iN)
                # pplot(x - q*dxP, y - q*dyP, iP)
                ax.plot(
                    np.array([ox + x, ox + x + q * dxN]) / (1 << n),
                    np.array([oy + y, oy + y + q * dyN]) / (1 << n),
                    color="cyan", lw=32 / (1 << n), zorder=105)
                ax.plot(
                    np.array([ox + x - q * dxP, ox + x]) / (1 << n),
                    np.array([oy + y - q * dyP, oy + y]) / (1 << n),
                    color="m", lw=32 / (1 << n), zorder=105)

            if iN != iP:
                ps.add(i)

    def addPoint(ps, x, y):
        checkBoundryAndAdd(ps, ox, oy, r, 2 * x, 2 * y, n)
        checkBoundryAndAdd(ps, ox, oy, r, -2 * x, 2 * y, n)
        checkBoundryAndAdd(ps, ox, oy, r, 2 * x, -2 * y, n)
        checkBoundryAndAdd(ps, ox, oy, r, -2 * x, -2 * y, n)

        checkBoundryAndAdd(ps, ox, oy, r, 2 * y, 2 * x, n)
        checkBoundryAndAdd(ps, ox, oy, r, -2 * y, 2 * x, n)
        checkBoundryAndAdd(ps, ox, oy, r, 2 * y, -2 * x, n)
        checkBoundryAndAdd(ps, ox, oy, r, -2 * y, -2 * x, n)

    # standard-ish circle ploting algorihm
    r = r0 // 2
    x = 0
    y = r
    e = 1 - r

    points = set()
    addPoint(points, x, y)
    while y > x:
        if e < 0:
            e = e + 2 * x + 3
            x = x + 1
        else:
            e = e + 2 * (x - y) + 5
            x = x + 1
            y = y - 1
        addPoint(points, x, y)

    ll = [(x, cid, not (i & 1)) for i, x in enumerate(sorted(points))]
    return ll


# Dealing with computing and adding circles
def plotCircle(ax, popts, ilist, n, ox, oy, r, m, cid):

    ss = (1 << m)  # m = 5, ss = 32

    ax.add_patch(Circle(
        (ox / (1 << m), oy / (1 << m)), r / (1 << m),
        facecolor=circleColors[cid] if popts.fillCircle else 'none',
        edgecolor='black',
        lw=32 / ss, zorder=10,
    ))

    if not popts.noCircPoints:
        xylist = [i2xy(i, n) for i, cid, flag in ilist]
        xy = np.array(xylist) / (1 << n)
        if len(xy) > 0:
            ax.scatter(xy[:, 0], xy[:, 1], s=512 / ss, c='blue', zorder=8)


def computeCircles(ax, circs, n, popts):
    def cleanUp(c, cid):
        (x, y, r) = c
        # (x, y, w) = i2xy( xy2i( x, y, n), n)
        return (x * (1 << n), y * (1 << n), r * (1 << n), n, cid)

    circsW = [cleanUp(c, cid + 1) for cid, c in enumerate(circs)]

    circsI = [genCircle(ax, popts, *c) for c in circsW]

    for s, c in zip(circsI, circsW):
        plotCircle(ax, popts, s, n, *c)

    return circsI


def doPlot(ax, popts):
    def colorOfStack(stack):
        c = 0

        for i in stack:
            c = c | (1 << i)

        c >>= 1

        stackColors[0] = popts.hcol or (0.6, 0.6, 0.6, 1.0)
        return stackColors[c]

    circs = popts.circs
    n = popts.n
    l = 1 << (n * 2)

    # Circular boundaries....

    bpl = []
    if circs:
        for m in computeCircles(ax, circs, n, popts):
            bpl.extend(m)

    if popts.noMerge:  # forget everything if nomerge set.
        bpl = []

    # need to switch to integers for colouring
    Ilist = [(0, 0, True)] + \
            [(i * l, cid, flag) for i, cid, flag in bpl] + \
            [(l - 1, 0, False)]
    Ilist = sorted(Ilist, key=itemgetter(0))
    # cols = [ popts.hcol, 'red' ]

    # The Hilbert curve
    if not popts.noCurve:
        stack = set()
        for i in range(len(Ilist) - 1):
            a = Ilist[i]
            b = Ilist[i + 1]
            ilist = range(int(a[0]), int(b[0]) + 1)
            if a[2]:
                stack.add(a[1])
            else:
                stack.remove(a[1])
            if len(ilist) > 0:
                xy = np.array([i2xy(i / l, n) for i in ilist])
                xy = xy / (1 << n)
                ax.plot(xy[:, 0], xy[:, 1],
                        c=colorOfStack(stack), zorder=5, lw=64 / (1 << n)
                        )

                if popts.showDir:
                    dxdy = np.array([hilbertDir((i / l), n, 0) for i in ilist])
                    dxdy = dxdy / (1 << n) / 2
                    ax.scatter(xy[:, 0] + dxdy[:, 0], xy[:, 1] + dxdy[:, 1],
                               zorder=20, s=1, c='cyan'
                               )

    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.axis('off')
    ax.set_box_aspect(1)


def main():
    args, plots = doArgs()

    N = len(plots)
    fig, ax = hozSubPlots(N)

    for ax, p in zip(ax, plots):
        doPlot(ax, p)

    if args.caption:
        figtext(0.5, 0.05, args.caption, wrap=True,
                horizontalalignment='center', fontsize=12
                )

    fig.subplots_adjust(hspace=0, wspace=0.1)
    fig.set_size_inches(5 * N, 5)

    savefig(fig, args.oname)


if __name__ == "__main__":
    main()

