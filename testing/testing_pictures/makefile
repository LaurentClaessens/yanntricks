
DEL_FILE      = rm -f

clean:
	-$(DEL_FILE) *.md5
	-$(DEL_FILE) *.pstricks
	-$(DEL_FILE) *.comment
	-$(DEL_FILE) *.pyc
	-$(DEL_FILE) phystricks*.py
	-$(DEL_FILE) *.dpth
	-$(DEL_FILE) *.aux
	-$(DEL_FILE) *.out
	-$(DEL_FILE) tikzFIGLabelFig*
	videlatex.sh

pdflatex:
	pytex lst_actu.py --all --no-external
create:
	./create_testing.py
figures:
	./figures_testing.py --all
all:
	make create
	make figures
	make create
	make pdflatex
