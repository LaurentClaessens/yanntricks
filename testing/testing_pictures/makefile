clean:
	rm *.md5
	rm *.pstricks
	rm *.comment
	rm *.pyc
	rm phystricks*.py
	rm *.dpth
	rm *.aux
pdflatex:
	pytex lst_actu.py --all --no-external
create:
	./create_all.py
figures:
	./figures_all.py --all
all:
	make create
	make figures
	make create
	make pdflatex
