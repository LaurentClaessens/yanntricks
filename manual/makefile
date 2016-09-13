DEL_FILE      = rm -f

clean:
	-$(DEL_FILE) *.md5
	-$(DEL_FILE) *.pstricks
	-$(DEL_FILE) *.comment
	-$(DEL_FILE) *.pyc
	-$(DEL_FILE) *.dpth
	-$(DEL_FILE) *.aux
	-$(DEL_FILE) *.out
	-$(DEL_FILE) tikzFIGLabelFig*
	videlatex.sh

external:
	pytex lst_actu.py --all --lotex
no-external:
	pytex lst_actu.py --all --lotex --no-external 
pictures:
	./figures_manual.py --all
all:
	make pictures no-external
	make pictures no-external
rebuild:clean all
