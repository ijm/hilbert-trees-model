# hilbert-trees-model
Plotting routines for Hilbert curve-based huge tree model integration paper and some other projects.

This is the Python and Matplotlib code used to produce the figures for:
* [Codename: Jimmy, HaRQ: How can I model the growth of a planet's worth of simplistic trees fast enough to be useful on a game server?](https://ghost.codenamejimmy.com/harq-how-can-i-model-the-growth-of-a-planets-worth-of-simplistic-trees-so-10-13-trees-fast-enough-to-be-useful-on-a-game-server/)

For example: ![Example plot](./exampleplot.svg)

### Issues
Parts of this code were ported from OCaml and C++ with the purpose of producing the correct figures. It is not intended to be nice, portable, or reusable code! The code is factored *horribly*. Maybe at some point I'll port the core concepts to a nice open-source library, but not today.

A 2D location is encoded either as (X, Y, 1\<\<W) with X, Y, and Z as integers, or as a float pair (x, y) with x and y in the range (-1, 1). A 1D curve index is encoded either as (I, 1\<\<N) or a float in the range [0, 1). In all cases, these are dyadic fractions. In C++, moving between the two is trivial as it's really just how the structure is packed, and the format needed can be inferred from the context. In Python, well, not so much. Python really wants me to pick a lane, and I really ought to tidy that up.

Lastly, the factoring of when things are plotted is a bit messed up: it's threaded all through figure.py. This is partly from having to debug code that was ported from something that was never intended to produce plots. Again, I ought to tidy that up, or at least disentangle them.
