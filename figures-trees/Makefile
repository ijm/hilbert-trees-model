
FIGUREFILES=figure.py hilbertLib.py figurePlotSetup.py figureArguments.py 
PYTHON=python
#SVGO=svgo

FIGURES=figure1.pdf figure1.svg \
    figure2.pdf figure2.svg \
    figure3.pdf figure3.svg \

all: $(FIGURES)

clean:
	rm $(FIGURES)

#%.min.svg: %.svg
#	$(SVGO) $< -o $@ --pretty

figure1.pdf figure1.svg : $(FIGUREFILES)
	$(PYTHON) figure.py -o $(basename $@) -p \
		'-n 5 -c "-0.21875, 0.15625, 0.5" "0.34375, 0.46875, 0.375"  "0.03125, -0.46875, 0.375" \
	 	--nocurve --nocirclepoints --fillcircles' -cap 'Figure 1. Three overlaping tree shadows.'

figure2.pdf figure2.svg : $(FIGUREFILES)
	$(PYTHON) figure.py -o $(basename $@) -p \
		'-n 5 -hc orange --nomerge -c "-0.21875, 0.15625, 0.5"' \
	 	'-n 5 -c "-0.21875, 0.15625, 0.5"' \
	 	-cap 'Figure 2. Left: Points intercecting circle and Hilbert curve. Right: Merged point, and ranges along the Hilbert curve.'

figure3.pdf figure3.svg : $(FIGUREFILES)
	$(PYTHON) figure.py -o $(basename $@) -p \
		'-n 5 -c "-0.21875, 0.15625, 0.5" "0.34375, 0.46875, 0.375"  "0.03125, -0.46875, 0.375"' \
		'-n 7 -c "-0.21875, 0.15625, 0.5" "0.34375, 0.46875, 0.375"  "0.03125, -0.46875, 0.375"' \
	 	-cap 'Figure 3: Color coded Hilbert ranges after merging the list from the circular boundaries. Left: scale $$n=5$$. Right: scale $$n=7$$'
