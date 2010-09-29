# -*- coding: utf8 -*-

###########################################################################
#	This is part of the module phystricks
#
#   phystricks is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   phystricks is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with phystricks.py.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

# copyright (c) Laurent Claessens, 2010
# email: moky.math@gmai.com

"""
This module uses phystricks in order to produces some mathematical situations/

"""

from __future__ import division
from sage.all import *
from phystricks import *

class NewtonMethodStep():
	"""
	Return the informations about one step of the Newton method.

	self.A : the starting x value
	self.P : the starting point on the graph
	self.B : the next point
	self.vertical_segment : the Segment from the point (xn,0) and the point P
	self.diagonal_segment : the Segment which joins the point P and x_{n+1}
	"""
	def __init__(self,newton,xn):
		self.A = Point(xn,0)
		self.P = newton.f.get_point(xn)
		xnn = xn - (self.P.y)/newton.f.derivative().eval(xn)			# The Newton's iteration formula is here
		self.B = Point(xnn,0)
		self.vertical_segment = Segment(self.A,self.P)
		self.diagonal_segment = Segment(self.P,self.B).dilate(1.5)

class NewtonMethod():
	def __init__(self,f):
		self.f = f
	def step_from_point(self,xn):
		return NewtonMethodStep(self,xn)


# La classe Description_Dynkin décrit la mathématique de Dynkin : elle n'a pas les informations sur les sigles qu'on veut mettre sur les racines.
# Le paramètre ll est une liste de "o" et "*" suivant que la racine ait une norme maximale ou non (cerle plein ou vide dans Dynkin)
# __init__ donne des valeurs par défaut. Par exemples les racines sont mises en ligne droite, et la matrice d'adjacence est nulle.
class Dynkin(object):
	def __init__(self,descr,deco):
		self.description = descr
		self.decoration = deco

class Decoration_Dynkin(object):
	def __init__(self,descr):
		n = len(descr.remplissure)
		self.distMark = []
		self.angleMark = []
		self.visMark = []
		for i in range(0,n):
			self.angleMark.append(90)
			self.distMark.append(0.3)
			self.visMark.append("")
	def PlaceMarque(self,n,dist,angle):
		self.distMark[n] = dist
		self.angleMark[n] = anlge
	def DefMarque(self,n,marque):
		self.visMark[n] = marque

# Un 4 dans une matrice d'adjacence signifie une ligne en pointillé
class Description_Dynkin(object):
	def __init__(self,ll):
		els = list(ll)
		n = len(els)
		lAdj = int(float(n)/2)+1
		#print n
		self.remplissure = []
		for i in range(0,lAdj):
			self.remplissure.append(els[2*i])
		#print self.remplissure
		self.ronds = []
		for i in range(0,n):
			self.ronds.append( Point(i,0) )
		self.Adjacence = []
		for i in range(0,lAdj):	
			z = []
			for j in range(0,lAdj) : z.append(0)
			self.Adjacence.append(z)
		for i in range(0,int(float(n)/2)):
			if ll[2*i+1] == "-": self.Adjacence[i][i+1] = 1
			if ll[2*i+1] == "=": self.Adjacence[i][i+1] = 2
			if ll[2*i+1] == ".": self.Adjacence[i][i+1] = 4

	# n sera le nombre de segments entre les points i et j. C'est relié aux angles entre les racines (cf matrice de Cartan).
	def AjouteSegment(self,i,j,n):
		self.Adjacence[i][j] = n
	def PlacePoint(self,num,P):
		self.ronds[num] = P

class Young(object):
	def __init__(self,T):
		self.diagramme = T

# Une instance de cette classe est un terme à l'intérieur d'un polynôme. Dans 7x^2+3x+9, le second terme est "+3x" et non simplement "3x". C'est à dire que ça tient compte du contexte dans lequel le terme est pour s'afficher.
# Note qu'un terme qui vaut zéro est noté "+0".
class TermeDansPolynome(object):
	def __init__(self,P,n):
		# La liste l crée le code LaTeX, tandis que la liste m crée le code maxima.
		l = []
		m = []
		#print "Je cherche le degré "+str(n)+" dans "+str(P.tab)
		cof = P.coeff[n]
		# Bienvenue au pays du bricolage !!
		if cof == 0:
			l.append("+0")
		if cof <> 0:
			if cof > 0: 
				if n <> P.deg :	
					l.append("+")
					m.append("+")
					if (cof <> 1) or (n == 0) :
						l.append(str(cof))
					m.append(str(cof))
						
				if n == P.deg :
					m.append(str(cof))
					if cof <> 1:
						l.append(str(cof))

			if cof < 0 :
				if cof <> -1:
					l.append(str(cof))
					m.append(str(cof))
				if (cof == -1) and (n <> 0):
					l.append("-")
					m.append("-1")
			if (n <> 0) :
				l.append("x")
				m.append("*x")
				if n <> 1:
					l.append("^"+str(n))
					m.append("^"+str(n))
			if (n == 0) and (cof == -1):
				l.append("-1")
				m.append("-1")

		self.latex = "".join(l)
		self.maxima = "".join(m)

		self.polynome = P
		self.deg = n

	def polynome_seul(self):
		t = [self.polynome.coeff[self.deg]]
		t.extend( [0]*self.deg )
		return Polynome(t)
		

# La classe Polynome prend un tableau et le considère comme un polynôme.
class Polynome(object):
	def __init__(self,P):

		# Si le tableau donné commence par des zéros, il faut les enlever (ça arrive si le polynôme est le résultat d'une addition)
		self.tab = P
		while (self.tab[0] == 0) and (len(self.tab) > 1) : self.tab = self.tab[1:]

		self.deg = len(self.tab)-1
		self.coeff = []
		for i in range(0,self.deg+1) : self.coeff.append(self.tab[self.deg-i])
		
		# self.liste_non_nuls donne la liste des termes non nuls du polynôme.
		lnn = []
		for i in reversed(range(0,self.deg)):
			if self.coeff[i] <> 0:
				lnn.append(self.terme(i))
		self.liste_non_nuls = lnn

		l = []
		for i in reversed(range(0,self.deg+1)):
			terme = self.terme(i).latex
			if terme <> "+0":
				l.append(terme)
		self.latex = "".join(l)
		m = []
		for i in reversed(range(0,self.deg+1)):
			terme = self.terme(i).maxima
			if terme <> "0":
				m.append(terme)
		self.maxima = "".join(m)
		if self.tab == [0] : 
			self.latex = "0"
			self.maxima = "0"

		#for i in range(0,len(self.tab)) :
		if (self.latex <> "0") and (self.coeff[0] == 0 ):
			j = 0
			#print self.coeff
			#print self.latex
			while self.coeff[j] == 0 : j = j+1
			self.minDeg = j
		else : self.minDeg = 0

	def terme(self,degre):
		return TermeDansPolynome(self,degre)

	# Surcharge des opérations courantes pour les polynômes
	def __mult__(self,P):
		return CalculPolynome().MulPoly(self,P)
	def __sub__ (self,P):
		return CalculPolynome().sub_polynome(self,P)

class DivEuclide(object):
	def __init__(self,A,B):
		self.A = A
		self.B = B
		self.reponse = CalculPolynome().DivPoly(A,B)[0]
		self.reste = CalculPolynome().DivPoly(A,B)[1]
		#print "Je divise "+A.latex+" par "+B.latex+". La réponse est : "+self.reponse.latex
		#print "Le degré de "+self.A.latex+" est "+str(self.A.deg)


	# self.reponse_etapes(n) donne un polynome dont les termes non nuls sont les n premiers non nuls de la réponse.
	# Une bonne idée serait de mettre ça comme une méthode de la classe Polynome.
	def reponse_etapes(self,nombre_etapes):
		p = []
		n = 0
		i = self.reponse.deg
		while n < nombre_etapes :
			if self.reponse.coeff[i] <> 0:
				if p == [] : deg = i
				p.append(self.reponse.coeff[i])
				n = n+1
				i = i-1
		p.extend( [0]*(deg-Polynome(p).deg) )
		return Polynome(p)

	# Donne le code LaTeX de n pas de la division euclidienne.
	def code(self,nombre_etapes):
		l = []

		l.append("\\begin{array}{")

		# Poser la division écrite
		for i in range(0,self.A.deg+1) : l.append("c")
		l.append("|l}\n")
		l.append(self.ligne_inter(self.A))
		l.append("	"+self.B.latex+"\\\\\n")
		#l.append("\cline{"+str(self.A.deg+2)+"-"+str(self.A.deg+2+self.B.deg)+"}")
		l.append("\cline{"+str(self.A.deg+2)+"-"+str(self.A.deg+2)+"}")
		l.append("\n")
		
		# Calculer les étapes
		aDiv = self.A
		deg_courant = self.reponse.deg
		for i in range(0,nombre_etapes):		
			while (self.reponse.coeff[deg_courant] == 0) and (deg_courant > 0) : deg_courant = deg_courant - 1		# Trouver le suivant qui n'est pas nul dans la réponse
			aSub = self.reponse.terme(deg_courant).polynome_seul()*self.B
			l.append(self.ligneSub(aSub,nombre_etapes))
			print "Je soustrait "+aDiv.maxima+" - "+aSub.maxima
			aDiv = aDiv - aSub
			print "et le résultat est : "+aDiv.latex
			l.append(self.ligne_inter(aDiv))
			l.append("\\\\\n")
			deg_courant = deg_courant - 1

		# Fermer les environements et conclure.
		l.append("\end{array}")
		return "".join(l)

	# Donne la ligne dans le array qui montre ce qu'il reste à diviser. Il ne met pas le \\ parce qu'il est aussi utilisé au moment de poser
	#   la division écrite.
	def ligne_inter(self,aDiv):
		l = []
		for i in range(0,self.A.deg-aDiv.deg) : l.append("	&	")
		for i in reversed(range(0,aDiv.deg+1)):
			l.append(aDiv.terme(i).latex+"	&	")
		print "Le poly à caser est "+aDiv.latex
		print "".join(l)
		return "".join(l)

	# Donne la ligne dans le array qui consiste à soustraire.
	# Il y a deux cas particuliers : la première ligne contient aussi la réponse de la division,
	# et la dernière ligne ne met pas de & après la parenthèse (Je crois que je pourrais ne pas traiter ce cas particulier)
	def ligneSub(self,aSub,nombre_etapes):
		print "J'essaye de faire rentrer "+aSub.latex
		l = []
		for i in range(aSub.deg,self.A.deg):
			l.append("	&	")
		l.append("-(")

		print aSub.latex+" a degré "+str(aSub.deg)+" et minimum "+str(aSub.minDeg)+"."
		for i in reversed(range(aSub.minDeg,aSub.deg+1)):
			l.append(aSub.terme(i).latex)
			if (i == aSub.minDeg) and (aSub.deg > self.B.deg ) : 
				l.append(")	&	")
			if (i == aSub.minDeg) and (aSub.deg == self.B.deg ) and (aSub.deg <> self.A.deg) : 
				l.append(")")
			if (i == aSub.minDeg) and (aSub.deg == self.B.deg ) and (aSub.deg == self.A.deg) : 
				l.append(")	&	")
			if i <> aSub.minDeg : l.append("	&	")
		for i in range(0,aSub.minDeg): l.append("\\vdots	&	")
		if aSub.deg == self.A.deg : l.append(self.reponse_etapes(nombre_etapes).latex)
		l.append("\\\\\n")
		cd = self.A.deg - aSub.deg + 1
		cf = cd + aSub.deg
		l.append("\cline{"+str(cd)+"-"+str(cd+aSub.deg-aSub.minDeg)+"}")

		l.append("\n")
		return "".join(l)

	def write_the_file(self,nom,n):								# Nous sommes dans la classe DivEuclide
		nombre_etapes = n
		if nombre_etapes > self.reponse.deg : nombre_etapes = self.reponse.deg + 1
		self.fichier = Fichier(nom)
		self.fichier.open_file("w")
		self.fichier.file.write(self.code(nombre_etapes))
		self.fichier.file.close()
		



class OldStuff(object):
	# This is not a class. I put here old methods that were in pspicture.
	def TraceDynkin(self,Dynkin):
		Adjacence	= Dynkin.description.Adjacence
		ronds		= Dynkin.description.ronds
		remplissure	= Dynkin.description.remplissure
		distMark	= Dynkin.decoration.distMark
		angleMark	= Dynkin.decoration.angleMark
		visMark		= Dynkin.decoration.visMark
		n = len( Adjacence )
		for i in range(0,n):
			for j in range(0,n):
				if Adjacence[i][j]==1:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"" )
				if Adjacence[i][j]==2:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"doubleline=true" )
				if Adjacence[i][j]==4:
					self.DrawSegment( Segment(ronds[i],ronds[j]),"linestyle=dotted" )
				# Je dois encore faire le cas avec trois lignes, mais je ne sais pas comment faire :-(
		for i in range(0,n):
				self.MarkThePoint(ronds[i],distMark[i],angleMark[i],remplissure[i],visMark[i])

	def TraceYoung(self,Y):
		for i in range(0,len(Y.diagramme)):
			for j in range(0,len(Y.diagramme[i])):
				self.TraceRectangle( Rectangle( Point(j,-i),Point(j+1,-i-1) ),"" )
				self.MarkThePoint( Point(j,-i), 0.5,-45,"none", Y.diagramme[i][j] )
