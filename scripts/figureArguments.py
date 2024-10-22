import argparse
from shlex import split

class ArgTuple(object):
    def __init__(self):
        pass

    def __call__(self, s):
        return tuple(float(x) for x in s.split(","))

def doArgs() :
  top = argparse.ArgumentParser(description= "Plot hilbert")
  top.add_argument('-o', '--outname', dest='oname', required=True, help='output file')
  top.add_argument('-p', '--plot', dest='cmds', nargs='+', required=True, help='Sub options to plot' )
  top.add_argument('-ph', '--plothelp', dest='cmdshelp', help='Sub Commands to plot help' )
  top.add_argument('-cap', '--caption', dest='caption',type=str, help='figure captions')
  
  cmds = argparse.ArgumentParser(description= "Hilbert Plot Subplot options")
  cmds.add_argument('-n', '--depth', dest='n',type=int, required=True, help='depth or hilbert scale')
  cmds.add_argument('-c', '--circles', dest='circs', nargs="*", type=ArgTuple(), help='Circles to plot' )
  cmds.add_argument('-hc', '--hilcolor', dest='hcol',type=str, default='grey', help='colour of exterior Hilbert curve')
  cmds.add_argument('-nm', '--nomerge', dest='noMerge',action='store_true', help="don't merge lists")
  cmds.add_argument('-nc', '--nocurve', dest='noCurve',action='store_true', help="don't show hilbert curve")
  cmds.add_argument('-ncp', '--nocirclepoints', dest='noCircPoints',action='store_true', help="don't show points on circle")
  cmds.add_argument('-sd', '--showdir', dest='showDir',action='store_true', help="show direction indicators on curve")
  cmds.add_argument('-sc', '--showcrossings', dest='showCross',action='store_true', help="show crossing checks on boundaries")
  cmds.add_argument('-fc', '--fillcircles', dest='fillCircle',action='store_true', help="circle fill colour")

  args = top.parse_args()

  if args.cmdshelp:
      cmds.print_help()

  for x in args.cmds :
      print(split(x))

  plots = [ cmds.parse_args(split(x)) for x in args.cmds ]

  return args, plots


