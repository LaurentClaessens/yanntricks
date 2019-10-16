from yanntricks import *
def TgCercleTrigono():
   pspict,fig = SinglePicture("TgCercleTrigono")

   O=Point(0,0)
   X=Point(1,0)
   Cercle=Circle(O,2)
   Q=Cercle.get_point(150)
   vQ=Vector(Q)

   vQ.parameters.color="cyan"

   phi=AngleAOB(X,O,Q)
   #phi.set_mark_angle(0.5*(90+phi.angleF.degree))
   phi.put_mark(text=r"$\varphi$",pspict=pspict)
   phi.parameters.color=vQ.parameters.color

   pspict.DrawGraphs(Cercle,phi,vQ)
   pspict.axes.no_graduation()
   pspict.DrawDefaultAxes()
   fig.no_figure()
   fig.conclude()
   fig.write_the_file()

