
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

external:
	pytex lst_actu.py --all 
no-external:
	pytex lst_actu.py --all --no-external
figures:
	./figures_demo.py --all
all:
	make figures
	make create
	make pdflatex
