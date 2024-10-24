import argparse
from shlex import split


class ArgTuple(object):
    def __init__(self):
        pass

    def __call__(self, s):
        return tuple(float(x) for x in s.split(","))


def doArgs():
    top = argparse.ArgumentParser(description="Plot hilbert")
    top.add_argument('-o', '--outname', dest='oname', required=True,
                     help='output file')
    top.add_argument('-p', '--plot', dest='cmds', nargs='+', required=True, action='append',
                     help='Sub options to plot, one per line, space seperated per col')

    top.add_argument('-ph', '--plothelp', dest='cmdshelp',
                     help='Sub Commands to plot help')
    top.add_argument('-cap', '--caption', dest='caption', type=str,
                     help='figure captions')

    cmds = argparse.ArgumentParser(description="Hilbert Plot Subplot options")
    cmds.add_argument('-n', '--depth', dest='n', type=int, required=True,
                      help='depth or hilbert scale')
    cmds.add_argument('-m', '--depth2', dest='m', type=int, default=0,
                      help='Second depth or hilbert scale')
    cmds.add_argument('-c', '--circles', dest='circs', nargs="*", type=ArgTuple(),
                      help='Circles to plot')
    cmds.add_argument('-hc', '--hilcolor', dest='hcol', type=str, default='grey',
                      help='colour of exterior Hilbert curve')
    cmds.add_argument('-nm', '--nomerge', dest='noMerge', action='store_true',
                      help="don't merge lists")
    cmds.add_argument('-nc', '--nocurve', dest='noCurve', action='store_true',
                      help="don't show hilbert curve")
    cmds.add_argument('-ncp', '--nocirclepoints', dest='noCircPoints', action='store_true',
                      help="don't show points on circle")
    cmds.add_argument('-sp', '--showpoints', dest='showPoints', action='store_true',
                      help="show offset points")
    cmds.add_argument('-sd', '--showdir', dest='showDir', action='store_true',
                      help="show direction indicators on curve")
    cmds.add_argument('-sc', '--showcrossings', dest='showCross', action='store_true',
                      help="show crossing checks on boundaries")
    cmds.add_argument('-fc', '--fillcircles', dest='fillCircle', action='store_true',
                      help="circle fill colour")

    args = top.parse_args()
    print(f"{args.cmds=}")
    if args.cmdshelp:
        cmds.print_help()

    plots = [cmds.parse_args(split(cell)) for row in args.cmds for cell in row]

    return args, plots


