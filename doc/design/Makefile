COMPILER = rubber
COMPILER_FLAGS = --pdf

all : project_documentation.pdf

%.pdf : %.tex
	$(COMPILER) $(COMPILER_FLAGS) $<

clean :
	-rm -rf *.aux *.toc *.dvi *.log *.pdf *.out
