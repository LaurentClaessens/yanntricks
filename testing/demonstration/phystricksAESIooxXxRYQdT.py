# -*- coding: utf8 -*-
from yanntricks import *

def DS_statistics(moustaches,pspict):
    pspict.dilatation_X(0.8)
    pspict.dilatation_Y(1)

    for i,m in enumerate(moustaches) :
        m.delta_y=len(moustaches)+0.75-i-1
        m.put_mark(dist=0.2,text="DS {}".format( i+1 ),pspict=pspict,position="W")

    maxy=len(moustaches)
    ledix=Segment(  Point(10,0),Point(10,maxy)   )
    ledix.parameters.color="green"
    ledix.parameters.linewidth=2
    ledix.parameters.style="dashed"

    pspict.DrawGraphs(moustaches,ledix)
    pspict.grid.draw_horizontal_grid=False
    pspict.axes.draw_single_axeY=False
    pspict.axes.single_axeY.no_graduation()
    pspict.DrawDefaultGrid()
    pspict.DrawDefaultAxes()

def AESIooxXxRYQdT():
    pspict,fig = SinglePicture("AESIooxXxRYQdT")

    moustaches=[]

    moustaches.append(Moustache(7.90,10.20,14.45,16.70,20.00,h=0.5,delta_y=0.75))   
    moustaches.append(Moustache(5.10,8.75,10.87,16.29,20.00,h=0.5,delta_y=0.75))    
    moustaches.append(BoxDiagram([13.941666666666666, 17.516666666666666, 15.5, 17.416666666666664, 13.341666666666665, 5.949999999999999, 5.883333333333333, 10.308333333333334, 14.733333333333334, 19.46666666666667, 13.925, 17.066666666666666, 14.966666666666665, 8.033333333333333, 14.783333333333331, 20.0, 9.216666666666667, 16.366666666666667, 16.3, 12.991666666666669, 10.433333333333334, 14.091666666666665, 9.691666666666666, 20.0],h=0.5,delta_y=0.75))  
    moustaches.append(BoxDiagram([9.366666666666667, 20.0, 16.616666666666667, 12.629999999999999, 8.37, 5.0166666666666675, 8.02, 11.233333333333334, 18.61, 19.166666666666668, 7.15, 16.04, 14.351666666666665, 4.416666666666666, 11.5, 17.65, 11.158333333333335, 12.475000000000001, 17.766666666666666, 10.333333333333334, 14.783333333333335, 14.0, 12.506666666666666, 16.65],h=0.5,delta_y=0.75))    
    moustaches.append(BoxDiagram([13.0, 19.0, 19.0, 20.0, 13.5, 14.5, 11.5, 12.5, 20.0, 19.5, 12.5, 15.0, 15.5, 7.5, 12.5, 19.0, 14.5, 14.0, 16.0, 10.0, 14.0, 17.5, 12.0],h=0.5,delta_y=0.75))   
    moustaches.append(BoxDiagram([7.0, 14.0, 14.0, 13.5, 3.5, 4.0, 16.5, 13.5, 7.0, 7.0, 11.0, 3.5, 17.0, 11.5, 11.0, 12.5, 6.0, 12.0, 8.0, 17.5],h=0.5,delta_y=0.75))      
    moustaches.append(BoxDiagram([7.0, 18.0, 13.5, 12.0, 12.0, 7.5, 5.0, 8.5, 15.5, 18.0, 12.0, 12.5, 16.0, 6.0, 8.0, 19.5, 7.0, 13.0, 13.5, 6.5, 16.0, 13.5, 11.5, 20.0],h=0.5,delta_y=0.75))     
    moustaches.append(BoxDiagram([2.0, 12.0, 13.0, 13.0, 12.5, 3.5, 4.0, 7.0, 12.5, 10.0, 3.0, 10.0, 13.0, 1.5, 5.0, 0.0, 3.0, 5.5, 8.5, 3.5, 7.5, 10.0, 4.5, 16.5],h=0.5,delta_y=0.75))  
    moustaches.append(BoxDiagram([9.5, 12.5, 11.0, 15.0, 10.5, 6.5, 8.5, 8.5, 15.0, 12.5, 5.5, 12.0, 13.0, 5.5, 8.5, 16.5, 9.0, 10.5, 11.5, 10.5, 11.0, 8.0, 8.5, 19.0],h=0.5,delta_y=0.75))   

    DS_statistics(moustaches,pspict)

    pspict.comment="Box diagrams of student graduation"

    fig.no_figure()
    fig.conclude()
    fig.write_the_file()
