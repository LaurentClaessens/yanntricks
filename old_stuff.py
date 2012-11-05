

class CalculPolynome(object):
    """
    This class should disappear when I learn how to perform euclidian divisions with Sage.
    """
    # La méthode calcul donne la sortie de maxima en brut. Pour traiter l'information, il faudra encore des tonnes de manipulations, et on peut déjà en mettre dans filtre
    def calcul(self,ligne,filtre):
        commande =  "maxima --batch-string=\"display2d:false; "+ligne+";\""+filtre
        return commands.getoutput(commande)
    # reponse donne ce que calcule donne, après extraction de la partie intéressante, c'est à dire prise de grep o2 et enlevure de "o2" lui-même.
    def reponse(self,ligne):
        ligne = self.calcul(ligne,"|grep o2")
        return ligne.replace("(%o2)","").replace(" ","")
    def DivPoly(self,P,Q):
        l = []
        m = []
        for i in range(0,P.deg-Q.deg+1):
            ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[1],x,"+str(P.deg-Q.deg-i)+")"
            l.append(  int( self.reponse(ligne) ) )
        for i in range(0,Q.deg+1):
            ligne =  "coeff( expand( divide("+P.maxima+","+Q.maxima+"))[2],x,"+str(Q.deg-i)+")"
            m.append( int (self.reponse(ligne) ) )
        return [Polynome(l),Polynome(m)]
    def MulPoly(self,P,Q):
        l = []
        for i in range(0,P.deg+Q.deg+1):
            ligne = "coeff( expand(("+P.maxima+")*("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"
            l.append( int( self.reponse(ligne)) )
        return Polynome(l)
    # Cette méthode est exactement la même que la précédente, au changement près de * vers +. Y'a peut être moyen de factoriser ...
    def sub_polynome(self,P,Q):
        l = []
        for i in range(0,P.deg+Q.deg+1):
            ligne =   "coeff( expand(("+P.maxima+")-("+Q.maxima+")),x,"+str(P.deg+Q.deg-i)+")"
            rep = self.reponse(ligne)
            if rep <> "":
                l.append(int(rep))
        return Polynome(l)

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
		xnn = xn - (self.P.y)/newton.f.derivative()(xn)			# The Newton's iteration formula is here
		self.B = Point(xnn,0)
		self.vertical_segment = Segment(self.A,self.P)
		self.diagonal_segment = Segment(self.P,self.B).dilatation(1.5)

class NewtonMethod():
	def __init__(self,f):
		self.f = f
	def step_from_point(self,xn):
		return NewtonMethodStep(self,xn)




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
		
