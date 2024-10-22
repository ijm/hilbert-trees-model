import matplotlib as mpl
mpl.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": "\n".join([
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
    ])
}
# r"\usepackage{cmbright}",
mpl.rcParams.update({'font.size': 9, "font.family": "serif", })
mpl.rcParams.update(pgf_with_pdflatex)
import matplotlib.pyplot as plt  # noqa: E402


# sig:   matplotlib.pyplot.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw)

def savefig(fig, name):
    fig.savefig(name + ".pdf", bbox_inches='tight')
    fig.savefig(name + ".pgf", bbox_inches='tight')
    fig.savefig(name + ".svg", bbox_inches='tight')


def hozSubPlots(N):
    fig, ax = plt.subplots(1, N)

    if N == 1:
        ax = [ax]

    return fig, ax


