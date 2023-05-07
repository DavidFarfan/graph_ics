'''
disponible en github.com
'''
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, Line
import random
import operator as o
from functools import partial
import math as m
from collections import deque

# Valores y Propiedades Vectoriales de Kivy
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, BooleanProperty
)
from kivy.clock import Clock

class ExMatrix: # matriz expandible

	data = None;    # Arreglo filas
	rows = None;	# num filas
	columns = None;	# num columnas
	
	def __init__(self):
		self.data = [];
		self.rows = 0;
		self.columns = 0;

	def expand_matrix(self, n, m):  # metodo para expandir tamaño de la matriz según necesidad
		for i in range(n+1):
			if(i>=len(self.data)):
				self.data.append([]);
		for i in range(n+1):
			for j in range(m+1):
				if(j>=len(self.data[i])):
					self.data[i].append([]);
		
		self.rows = len(self.data);
		self.columns = len(self.data[0]);
	
	def print_matrix(self): # imprimir matriz
		for i in range(len(self.data)):
			print(self.data[i]);
	
	def intro(self, datos, idx, idy):  # Introducir datos en un indice (x, y)
		self.expand_matrix(idx, idy);
		self.data[idx][idy] = datos;
		
	def mirror(self): # Valores simetricos respecto a la diagonal
		if(self.rows>self.columns):
			self.expand_matrix(self.rows, self.rows);
		elif(self.columns>self.rows):
			self.expand_matrix(self.columns, self.columns);
		for i in range(self.rows):
			for j in range(self.columns):
				if(i<j):
					#print(str(i)+"<"+str(j)+" data: "+str(self.data[j][i]));
					self.data[i][j] = self.data[j][i];

class Graph:	# grafo conceptual

	V = None;	# vertices
	E = None;	# aristas
	Sub = None;	# subgrafos
	
	def __init__(self):
		self.V = [];
		self.E = ExMatrix();
		self.Sub = [];
	
	def get_sub(self, name):
		for s in self.Sub:
			if s[0] == name: return s;
		return None;
	
	def add_sub(self, sub_V, name):	# agregar a la lista de subgrafos
		if sub_V == []: return;	# no agregar vacio
		#print("vertices: "+str(sub_V));	# agregar vertices del subgrafo con un nombre
		
		for i in range(len(self.Sub)): # buscar el subgrafo
			s = self.Sub[i];
			if name == s[0]: 
				self.Sub[i][1] = sub_V;	# si el nombre pertenece a un subgrafo, reemplazar sus vert.
				#print("subgrafos: "+str(self.Sub));
				return;
		
		if name == None:	self.Sub.append(['subG'+str(len(self.Sub)),sub_V]);
		else: self.Sub.append([name,sub_V]);
		#print("subgrafos: "+str(self.Sub));
	
	def get_edge(self, n ,m):	# arista nm
		return self.E.data[n][m];
	
	def edge(self, val, n, m):	# establecer valor para la arista nm
		if n > m: self.E.intro(val, n, m);
		else: self.E.intro(val, m, n);
		self.E.mirror();
		#self.E.print_matrix();
	
	def insertVertex(self):	# insertar vertice
		self.V.append(len(self.V));
		self.edge(1, len(self.V)-1, len(self.V)-1);
		for i in range(len(self.V)-1):
			self.edge(0, len(self.V)-1, i);
		self.add_sub(self.V, 'self');
	
	def opp_edge(self, n, m):	# Invertir arista (Grafo y complemento)
		if self.get_edge(n, m) == 0: self.edge(1, n, m);
		else: self.edge(0, n, m);
	
	def ciclo_edges(self, n):	# Agregar aristas del n-ciclo
		for v in self.V:
			vc = (v+n)%len(self.V);
			self.edge(1, vc, v);
	
	def rand_edges(self, p):	# aristas aleatorias
		ra = 0.0;
		for i in range(self.E.rows):
			for j in range(self.E.columns):
				if j > i:
					ra = random.random();
					if ra <= p:
						self.edge(1,j,i);
					else:
						self.edge(0,j,i);

class Path_Calc:	# calculadora de caminos

	def neighbor_set(self, v, G):
		N = [];
		for u in range(G.E.columns):
			if (not u == v) and (G.get_edge(u, v) == 1):
				N.append(u);
		return N;
	
	def intersection_set(self, A, B):
		I = [];
		for v in A:
			if o.contains(B, v): I.append(v);
		return I;
	
	def bron_kerbosch(self, R_arg, P_arg, X_arg, G, lvl):
		
		'''
		Sin pivoting:
		
		La forma basica del algoritmo Bron-Kerboch es una recursión con retroceso que busca todos los cliques maximales en un grafo dado, G. En general, dados tres conjuntos disyuntos de vertices R, P, y X, encuentra los cliques maximales que incluyen todos los vertices de R, algunos de los vertices de P, y ninguno de los vertices de X. En cada llamada al algoritmo, P y X son conjuntos disyuntos cuya union consiste en aquellos vertices que forman cliques cuando se añaden a R. En otras palabras, P U X es el conjunto de vertices que están unidos a cualquier elemento de R. Cuando P y X son ambos vacios, no hay más elementos que puedan ser agregados a R, de modo que R es un clique maximal y el algoritmo devuelve R.
		
		La recursión inicia estableciendo R y X como vacíos, y a P como el conjunto de vertices del grafo (Si G(V,E), P=V). Dentro de cada llamada recursiva, el algoritmo considera los vertices en P sucesivamente; si no hay tales vertices, se reporta R como clique maximal (Si X es vacio), o se retrocede. Para cada vertice v en P, se hace una llamada recursiva en la que v es agregado a R y en la cual P y X son restringidos al conjunto vecino N(v) de v, que encuentra y reporta todas las extensiones clique de R que contienen v. Entonces, se mueve a v de P a X para excluirlo de los futuros cliques a considerar y continua con el siguiente vértice en P.
		'''
		
		R = R_arg[:];	# computar sin alterar los valores del grafo
		P = P_arg[:];
		X = X_arg[:];
		
		#print("----------> llamada: nivel = "+str(lvl));
		#print("R: "+str(R));
		#print("P: "+str(P));
		#print("X: "+str(X));
		if P == [] and X == []: print("clique: "+str(R));
		while not P == []:
			v = P[0];
			Nv = self.neighbor_set(v, G);
			P_int_Nv = self.intersection_set(P, Nv);
			X_int_Nv = self.intersection_set(X, Nv);
			#print("vertice en P: "+str(v)+" tiene vecinos "+str(Nv)+". P_Nv = "+str(P_int_Nv)+" y P_Nv = "+str(X_int_Nv));
			self.bron_kerbosch(R + [v], P_int_Nv, X_int_Nv, G, lvl+1);
			#print("movemos "+str(v)+" desde P = "+str(P)+" hasta X = "+str(X));
			P.remove(v);
			X.append(v);
			#print("resulta en: P = "+str(P)+" y X = "+str(X));
		
	def bron_kerbosch_pivot(self):
		
		'''
		Con pivoting:
		
		La forma basica del algoritmo, descrito arriba, es ineficiente en el caso de grafos con muchos cliques no-maximales: hace una llamada recursiva por cada clique, maximal o no. Para ahorrar tiempo y permitir al algoritmo retroceder más rápido hacia ramas de busqueda que contienen cliques no maximales, Bron y Kerbosch instrodujeron una variante del algoritmo que involucra un "vertice pivote" u, escogido de P (O de forma más general, como posteriores investigaciones mostraron, de P U X). 
		
		Cualquier clique maximal debe incluir ya sea u o uno de sus no-vecinos porque, de lo contrario, el clique podría aumentar agregándole u. Por lo tanto, solo u y sus no vecinos necesitan ser probados como candidatos para el vértice v que es agregado a R en cada llamada recursiva.
		'''
		
		pass;
	
	def bron_kerbosch_order(self):
	
		'''
		Con ordenamiento de vertices:
		
		Un método alternativo de mejorar la forma basica del algoritmo Bron-Kerbosch involucra renunciar al pivoting en el nivel mas externo de la recusión y, en su lugar, escoger el orden de las llamadas recursivas con cuidado para minimizar los tamaños de los conjuntos P de vertices candidatos dentro de cada llamada recursiva.
		
		degen(G) de un grafo G es el minimo numero d tal que todo subgrafo de G tiene un vertice de grado d o menor. Todo grafo tiene un orden de degeneración, un orden de los vertices tal que cada vertice tiene d o menos vecinos que vienen más tarde en el orden; un orden de degeneración puede ser encontrado en tiempo lineal seleccionando repetidamente el vertice de menor grado entre los vertices restantes. Si el orden de los vertices v que el algoritmo Bron-Kerbosch recorre es un orden de degeneración, entonces el conjunto P de vertices candidatos en cada llamada (los vecinos de v que van después en el orden) tendrá, con seguridad, un tamaño de a lo sumo d. El conjunto X de vertices excluidos consistirá en todos los vecinos previos de v, y puede ser mucho más grande que d. En las llamadas recursivas al algoritmo bajo el nivel más alto de recursión, puede emplearse la versión con pivoting.
		
		'''
		
		pass;
	
	def comb(self, n, k):	# coef. binomial
		return int ( m.factorial(n) / ( m.factorial(k) * ( m.factorial(n - k) ) ) );
	
	def matula_beck_deg_order(self, G):	# algoritmo de orden de degeneración
		
		'''
		El algoritmo implementa la cola de prioridad para extraer los vertices, uno a uno, del grafo segun sus grados y, de esa manera, generar un orden de degeneración
		'''
		
		L = [];	# arreglo de salida (orden de degeneración)
		d_V = [];	# arreglo de grados de cada vertice (auxiliar para calcular el orden)
		D = [[]];	# partición de los vertices según su grado (priority queue)
		
		for i in range(G.E.columns):	# calcular grados para cada vertice
			d_v = 0;
			for j in range(G.E.rows):
				if (not i == j) and (G.get_edge(i, j) == 1): d_v += 1;
			d_V.append(d_v);
		
		print("---------- deg order");
		print("d_V = "+str(d_V));
		
		deg_num = 0;
		for i in range(len(d_V)):	# calcular partición
		
			if d_V[i] > deg_num:	# ampliar numero de grados maximo si es necesario
				for j in range(d_V[i] - deg_num):
					D.append([]);
				deg_num = len(D) - 1;
				
			D[d_V[i]].append(i);
		
		print("D = "+str(D));
		
		for j in range(len(d_V)):	# repetir por el numero de vertices
			for i in range(len(D)):	# buscar el menor grado
				if not D[i] == []:	# si esta clase de la particion no es vacía
					v = D[i][0];	# seleccionar vertice de la lista D[i]
					L = [v] + L;	# Agregarlo a L
					D[i].remove(v);	# quitarlo de la partición
					print("v = "+str(v)+" puesto en L = "+str(L)+" y removido de D["+str(i)+"] = "+str(D[i]));
					for w in range(G.E.rows):
						if (not v == w) and (G.get_edge(v, w) == 1): 	# w es vecino con v
							if not o.contains(L, w):	# w no está en L
								d_V[w] = d_V[w] - 1;	# sustraer uno a los grados de w
								D[d_V[w]].append(w);	# mover w en la partición
								D[d_V[w]+1].remove(w);
								print("w = "+str(w)+" es vecino de "+str(v)+" y no está en L = "+str(L));
								print("w = "+str(w)+" tiene un grado menos: dw = "+str(d_V[w])+" y pertenece ahora a D["+str(d_V[w])+"] = "+str(D[d_V[w]]));
					break;
		
		print("L = "+str(L));
	
	def next(self, GC, R, V):	# iteracion del algoritmo camino simple
		for v in GC.V:
			if o.contains(V, v.id) and GC.G.get_edge(R, v.id) == 1:
				GC.V[R].set_type('U');	# anterior ruso ahora es U
				v.set_type('R');
				V.remove(v.id);
				return v.id;
		#print("end of path for R =" + str(R));
		return R;

	def simple_path(self, GC, text_f, s):	# encontrar camino simple desde s
		
		if GC.set_sub: return;	# no interferencia con la funcion de subgrafos
		
		print("----------> bron_kerbosch");
		self.bron_kerbosch([], GC.G.V, [], GC.G, 1);
		
		G = GC.G;	# grafo asociado al visual
		P = deque(); # camino
		V = list(G.V);	# vertices no visitados
		GC.V[s].set_type('R');	# vertice s es ruso
		R1 = s;	# ruso 1
		R2 = s;	# ruso 2
		
		for v in GC.V:	# reiniciar tipos de los vertices
			v.set_type('-');
		
		V.remove(s);	# comenzar en s
		P.append(s);
		#print("V = "+str(V));
		#print("Vertices = "+str(G.V));
		
		vf = self.next(GC, R1, V);
		#print("R1 = "+str(vf));
		#print("V = "+str(V));
		while(not vf == R1):	# agregar vertices en un sentido
			R1 = vf;
			P.append(R1);
			vf = self.next(GC, R1, V);
			#print("R1 = "+str(vf));
			#print("V = "+str(V));
		
		vf = self.next(GC, R2, V);
		#print("R2 = "+str(vf));
		#print("V = "+str(V));
		while(not vf == R2):	# agregar vertices en el sentido contrario
			R2 = vf;
			P.appendleft(R2);
			vf = self.next(GC, R2, V);
			#print("R2 = "+str(vf));
			#print("V = "+str(V));
		#print("V = "+str(V));
		#print(str(P));
		
		GC.V[R2].set_type('R');
		GC.V[R1].set_type('R');	# Determinar rusos
		
		for v in V:	# Determinar los franceses triviales
			count = 0;
			for i in range(G.E.columns):
				if G.get_edge(v, i) == 1 and GC.V[i].type == 'U': 
					count += 1;
					#print("edge ("+str(v)+", "+str(i)+") = "+str(G.get_edge(v, i))+" esta en G");
			if count > 1: GC.V[v].set_type('F');
			elif count == 1: GC.V[v].set_type('F/P');
			else: GC.V[v].set_type('F/P/I');
		
		GC.log = "camino simple calculado."
		text_f.text = "camino simple: "+str(list(P)) +", tamaño = "+str(len(P));
		
		for e in V:	# cambiar etiquetas del grafo
			P.append(e);
		#print(str(P));
		GC.lbl_change_sev(P);

class VertexCanvas(Widget):	# vertice visual
	
	id = NumericProperty(-1);	# id del vertice
	pos_x = NumericProperty(0);	# posicion x
	pos_y = NumericProperty(0);	# posicion y
	d = NumericProperty(0);	# diametro
	selected = BooleanProperty(False);	# seleccionado para ser deslizado
	type = StringProperty('-');	# tipo de vertice
	sub = BooleanProperty(False); # seleccionado para subgrafo
	
	def set_type(self, t):	# establecer tipo
		self.type = t;
	
	def set_d(self, d):	# establecer diametro
		self.d = d;
	
	def set_id(self, id):	# establecer id
		self.id = id;
	
	def pos_set(self, x, y):	# establecer posicion
		self.pos_x = x;
		self.pos_y = y;
	
	def select(self):	# seleccionar
		self.selected = True;
	
	def unselect(self):	# deseleccionar
		self.selected = False;
		
	def on_touch_down(self, touch):
		if (not self.collide_siblings()) and touch.x >= self.pos_x and touch.x < self.pos_x + self.d and touch.y >= self.pos_y and touch.y < self.pos_y + self.d:
			if not self.parent.set_sub:
				self.parent.set_mark(self.id);
				self.select();	# seleccionar si se le hizo clic y no esta activa la func. subgrafo, agregar marca
			else:	# seleccionar con un clic para determinar subgrafo
				if not self.sub:
					self.parent.V_sub.append(self.id);
					self.sub = True;
					self.parent.log = "v = " + str(self.id);	# info del vertice
					self.parent.log += '\n'+"tipo = " + str(self.type);
				else:
					self.parent.V_sub.remove(self.id);
					self.sub = False;
					self.parent.log += '';
				self.parent.show_subgraph();
			#print("mark"+str(self.parent.mark));
			#print("v"+str(self.id));
	
	def on_touch_up(self, touch):
		if self.selected: self.unselect();	# deseleccionar si se levanta el clic
	
	def collide_siblings(self):	# verficar interseccion con otros vertices
		for v in self.parent.V:
			if (not v.id == self.id) and (((v.pos_x <= self.pos_x <= v.pos_x + v.d) and (v.pos_y <= self.pos_y <= v.pos_y + v.d)) or ((v.pos_x <= self.pos_x + self.d <= v.pos_x + v.d) and (v.pos_y <= self.pos_y + self.d <= v.pos_y + v.d)) or ((v.pos_x <= self.pos_x <= v.pos_x + v.d) and (v.pos_y <= self.pos_y + self.d <= v.pos_y + v.d)) or ((v.pos_x <= self.pos_x + self.d <= v.pos_x + v.d) and (v.pos_y <= self.pos_y <= v.pos_y + v.d))):
				return True;
		return False;
	
	def separate(self):	# separar de otro vertice
		if self.collide_siblings():
			ra1 = random.random();
			ra2 = random.random();
			if ra1 <= 0.5:
				if ra2 <= 0.5:
					self.pos_x+=ra1*10; 
					self.pos_y+=ra1*10; 
				else: 
					self.pos_x+=ra1*10; 
					self.pos_y-=ra1*10;
			else:
				if ra2 <= 0.5: 
					self.pos_x-=ra1*10; 
					self.pos_y+=ra1*10; 
				else: 
					self.pos_x-=ra1*10; 
					self.pos_y-=ra1*10;
	
	def on_touch_move(self, touch):
		if not self.parent.set_sub:	# mover vertices solo si no esta activa la funcion de subgrafo
			if self.selected:	# mover si el clic se mantiene, quitar marcas
				self.pos_set(touch.x - self.d/2, touch.y - self.d/2);
				self.parent.set_mark(-1);
			elif touch.x >= self.pos_x and touch.x < self.pos_x + self.d and touch.y >= self.pos_y and touch.y < self.pos_y + self.d:
				self.select();	# seleccionar con el paso del cursor también (deslizar)
		else:	# seleccionar con el paso del cursos para determinar subgrafo
			if touch.x >= self.pos_x and touch.x < self.pos_x + self.d and touch.y >= self.pos_y and touch.y < self.pos_y + self.d:
				if not self.sub:
					self.parent.V_sub.append(self.id);
					self.parent.show_subgraph();
					self.sub = True;	# seleccionar con el paso del cursor también (subgrafo)
					self.parent.log = "v = " + str(self.id);	# info del vertice
					self.parent.log += '\n'+"tipo = " + str(self.type);

class GraphCanvas(Widget):	# grafo visual
	
	G = ObjectProperty(Graph());	# grafo asociado
	V = ObjectProperty([]);	# vertices visuales
	d = NumericProperty(0);	# diametro
	ds = ObjectProperty([]);	# cambio de tamaño del lienzo
	original = BooleanProperty(True);	# ver aristas del grafo
	complement = BooleanProperty(False);	# ver aristas del complemento
	mark = NumericProperty(-1);	# primer vertice marcado
	end = NumericProperty(-1);	# segundo vertice marcado
	log = StringProperty('');	# output
	set_sub = BooleanProperty(False); # se está seleccionando un subgrafo
	V_sub = ObjectProperty([]);	# vertices del subgrafo en construccion
	display_new_sub = BooleanProperty(True);	# bandera para el panel
	view_V = ObjectProperty([]);	# vertices a mostrar
	
	def show_subgraph(self):	# mostrar en el campo de texto el subgrafo que se está construyendo
		self.parent.children[1].children[0].text = "subgrafo: "+str(self.V_sub);	# imprimir en el campo de texto
		#print(self.V_sub);
	
	def reset_subgraph(self):	# desmarcar vertices al terminar de construir subgrafo
		self.log = "";
		for v in self.V:
			if v.sub: 
				self.display_new_sub = True;	# no dar bandera verde al panel si no hubo ningun vertice seleccionado
				v.sub = False;
		self.set_sub = False;
	
	def subgraph_confirm(self):	# Confirmar subgrafo construido
		sub_aux = self.V_sub;
		self.G.add_sub(sub_aux, None);
		self.reset_subgraph();
	
	def subgraph(self, value):	# on/off # seleccion de subgrafo
		self.set_mark(-1);	# quitar marcas
		if value:
			self.V_sub = [];
			self.log = "escoger los vertices del subgrafo";
			self.set_sub = True;
		else:
			self.reset_subgraph();
	
	def lbl_change_sev(self, vec):	# cambiar todas las etiquetas
		pos = [];
		for v in self.V:
			pos.append([v.pos_x, v.pos_y]);
		for i in range(len(self.V)):
			self.V[vec[i]].pos_set(pos[i][0], pos[i][1]);
	
	def lbl_change(self, txt):	# intercambiar un par de etiquetas
		if self.set_sub: return;	# no interferencia con la funcion de subgrafos
		l = list(txt.rsplit(' '));
		n = int(l[0]);
		m = int(l[1]);
		if n < 0 or m < 0: return;
		#print("input: "+str(l));
		x1 = self.V[n].pos_x;
		y1 = self.V[n].pos_y;
		x2 = self.V[m].pos_x;
		y2 = self.V[m].pos_y;
		self.V[m].pos_set(x1, y1);
		self.V[n].pos_set(x2, y2);
	
	def set_mark(self, v):	# manejo de marcas
		if self.set_sub: return;	# no interferencia con la funcion de subgrafos
		if v == -1:	# quitar 1ra y 2da marcas
			self.mark = v;
			self.end = -1;
			self.log = '';
		elif self.mark == -1:	# agregar 1ra marca si no hay ninguna
			self.mark = v;
			self.log = "v = " + str(v);	# info del vertice
			self.log += '\n'+"tipo = " + str(self.V[v].type);
		elif self.mark == v: 	# quitar marcas si se vuelve a escoger un vertice marcado
			self.mark = -1;
			self.end = -1;
			self.log = '';
		else:
			if v == self.end:	# invertir arista si se vuelve a escoger el segundo vertice marcado
				self.G.opp_edge(self.mark, self.end);
				#self.G.E.print_matrix();
				self.log = "edge (" + str(self.mark) + ", " + str(self.end) + ") trasladado.";
				self.mark = -1;
				self.end = -1;
				return;
			e = self.G.get_edge(self.mark, v);	# informar dónde está la arista si se marca un segundo vertice
			self.end = v;
			if e == 0: self.log = "edge (" + str(self.mark) + ", " + str(v) + ") está en Com."+'\n'+"(Otro clic para trasladar)"; 
			else: self.log = "edge (" + str(self.mark) + ", " + str(v) + ") está en G."+'\n'+"(Otro clic para trasladar)"; 
	
	def on_com_active(self, value):	# on/off aristas complemento
		if value:
			self.complement = True;
		else:
			self.complement = False;
	
	def on_or_active(self, value): # on/off aristas grafo
		if value:
			self.original = True;
		else:
			self.original = False;
	
	def recalc_vertexes_pos(self):	# reiniciar posiciones de los vertices
		n = len(self.V);
		self.set_mark(-1);	# quitar marcas al reiniciar
		if not self.set_sub: self.log = '';
		for i in range(n):
			angle = (2 * i * m.pi) / n;
			self.V[i].pos_set(200 * m.cos(angle) + (self.width / 2), 200 * m.sin(angle) + (self.height / 2));
	
	def set_graph(self, G):	# establecer grafo a mostrar
		if self.set_sub: return;	# no interferencia con la funcion de subgrafos
		self.clear_widgets(self.children);	# limpiar canvas
		self.V = [];	# vaciar lista de vertices (visuales)
		self.G = G;		# establecer nuevo grafo
		self.view_V = self.G.get_sub('self')[1];	# ver, por defecto, el grafo en su totalidad
		self.display_new_sub = True;	# bandera verde para agregar el grafo al panel
		for i in range(len(self.G.V)):	# agregar verticeas (visuales)
			v = VertexCanvas();
			v.set_id(i);
			v.set_d(self.d);
			self.V.append(v);
			self.add_widget(self.V[i]);
		self.recalc_vertexes_pos();
	
	def init(self, G, d):	# rutina inicio
		self.d = d;
		self.ds.append(self.width);
		self.ds.append(self.height);
		self.set_graph(G);
	
	def draw_vertex(self, v):	# dibujar un vertice
		with self.canvas:
			Color(200, 200, 200, mode='rgb');
			Line(ellipse=(v.pos_x, v.pos_y, self.d, self.d));
			if not v.selected: Color(0, 0, .05, mode='hsv');
			if self.mark == v.id: Color(50, 100, 0, mode='rgb');
			if self.end == v.id: Color(200, 0, 10, mode='rgb');
			if v.sub: Color(0, 100, 50, mode='rgb');
			Ellipse(pos=(v.pos_x, v.pos_y), size=(self.d, self.d));
			Label(font_size='10', center_x=v.pos_x+self.d/2, top=v.pos_y+60, text=str(v.id));
	
	def draw_vertexes(self):	# dibujar los vertices
		if not self.ds == self.size:
			self.ds = self.size;
			self.recalc_vertexes_pos();
		else:
			for v in self.V:
				if not v.selected: v.separate();
				if o.contains(self.view_V, v.id): self.draw_vertex(v);
	
	def draw_edge(self, v1, v2, d):	# dibujar una arista
		x1 = v1.pos_x;
		y1 = v1.pos_y;
		x2 = v2.pos_x;
		y2 = v2.pos_y;
		Line(points=[d+x1 ,d+y1 ,d+x2 ,d+y2], width=1);
	
	def draw_edges(self):	# dibujar todas las aristas
		d = self.d/2;
		with self.canvas:
			for i in range(self.G.E.rows):
				for j in range(self.G.E.columns):
					if j > i:
						if o.contains(self.view_V, self.V[i].id) and o.contains(self.view_V, self.V[j].id):
							if self.complement and self.G.E.data[i][j] == 0:
								Color(0, 0, 255, mode='rgb');
								self.draw_edge(self.V[i], self.V[j], d);
							elif self.original and self.G.E.data[i][j] == 1:
								Color(255, 0, 0, mode='rgb');
								self.draw_edge(self.V[i], self.V[j], d);

	def draw(self):	# rutina de dibujo
		self.canvas.clear();
		with self.canvas:
			Color(0, 0, .05, mode='hsv');
			Rectangle(size=[self.width, self.height], pos=self.pos);
		self.draw_edges();
		self.draw_vertexes();
		with self.canvas:
			Label(font_size='15', text='>> '+self.log, center_x=self.width/3 - 12, top=self.height/6);
	
	def update(self, dt):	# a ejecutar segun reloj
		self.draw();

class SubPanel(GridLayout):	# panel de subgrafos
	
	Sub = [];	# lista de nombres de los subgrafos almacenados
	up_btn = Button(font_size='10', text='/|', size_hint_y=None, height=30, size_hint_x=None, width=30);	# boton up
	dwn_btn = Button(font_size='10', text='|/', size_hint_y=None, height=30, size_hint_x=None, width=30);	# boton dwn
	first_sub_to_show = 0;

	def add_funct_on_panel(self, i, GC):	# por alguna razón, agregar los botones con un for no funciona
		if i >= 18: return;
		sub_name = self.Sub[self.first_sub_to_show + i];
		aux_btn = Button(font_size='10', text=sub_name, size_hint_y=None, height=30, size_hint_x=None, width=100);
		#print("btn = "+str(sub_name));
		aux_btn.bind(on_press=lambda x:self.display_subgraph(GC, sub_name));
		self.add_widget(aux_btn);
		self.add_funct_on_panel(i+1, GC);

	def go_up(self):	# funcion del boton arriba
		if self.first_sub_to_show == 0: return;	# inicio de la lista
		self.first_sub_to_show -= 1;	# retroceder en la lista

	def go_down(self):	# funcion del boton abajo
		if len(self.Sub) <= 18: return; # no hace nada si aún no hay suficientes botones que mostrar
		if self.first_sub_to_show == len(self.Sub) - 18: return;	# fin de la lista
		self.first_sub_to_show += 1;	# avanzar en la lista
	
	def restart(self):	# reiniciar el panel 
		self.Sub = [];	# vaciar lista de nombres
		self.clear_widgets(self.children);	# limpiar canvas
		self.add_widget(self.up_btn);	# agregar los botones
		self.add_widget(self.dwn_btn);

	def display_subgraph(self, GC, name):	# imponer al canvas la vista seleccionada
		arr = GC.G.get_sub(name)[1];
		name = GC.G.get_sub(name)[0];
		#print("array to display: "+str(arr)+" from sub named: "+str(name));
		GC.view_V = arr;

	def reprint_subs(self, GC):	# imprimir los botones que alcanzan en el panel
		for i in range(19):
			#print(self.children[0].text);
			self.remove_widget(self.children[0]);	# limpiar canvas, menos el boton arriba
		#print("-----------------");
		self.add_funct_on_panel(0, GC);	# agregar botones recursivamente
		self.add_widget(self.dwn_btn); # pintar el boton abajo de ultimo

	def update(self, GC):	# actualizar el panel
		if GC.display_new_sub:	# esperar la bandera del canvas para agregar un nombre a la lista
			name = GC.G.Sub[len(self.Sub)][0];	# copiar el nombre a la lista
			self.Sub.append(name);
			if len(self.Sub) <= 18:
				self.remove_widget(self.dwn_btn);	# cambiar de lugar el boton down
				aux_btn = Button(font_size='10', text=name, size_hint_y=None, height=30, size_hint_x=None, width=100);
				#print("btn = "+str(name));
				aux_btn.bind(on_press=lambda x:self.display_subgraph(GC, name));	# agregar funcionalidad al boton
				self.add_widget(aux_btn);
				self.add_widget(self.dwn_btn);
				#print(str(self.Sub)+" vs "+str(GC.G.Sub));
			GC.display_new_sub = False;	# dejar bandera en falso al terminar
		if len(self.Sub) > 18:
			#print(str(self.Sub[self.first_sub_to_show])+" = "+str(self.children[18].text));
			if not self.Sub[self.first_sub_to_show] == self.children[18].text:	
				self.reprint_subs(GC); # re-imprimir botones si se ha deslizado la lista
	
	def init(self):	# rutina de inicio
		self.cols = 1;
		self.rows = 20;
		self.orientation = "rl-tb";
		self.size_hint_x = None;
		self.width = 100;
		self.up_btn.bind(on_press=lambda x:self.go_up());
		self.dwn_btn.bind(on_press=lambda x:self.go_down());
		self.add_widget(self.up_btn);
		self.add_widget(self.dwn_btn);

class GraphApp(App):	# aplicacion
	
	def rand_graph(self, sub):	# preparar un grafo random
		sub.restart();
		G = Graph();
		for i in range(10):
			G.insertVertex();
		G.rand_edges(.3);
		#print("-------------> random graph:");
		#G.E.print_matrix();
		return G;
	
	def subgraph(self, value, sub_btn, path_btn, ran_btn, lbl_btn, canvas):	# mostrar/ocultar botones y correr funcion
		sub_btn.disabled = not value;
		path_btn.disabled = value;
		ran_btn.disabled = value;
		lbl_btn.disabled = value;
		canvas.subgraph(value);
	
	def subgraph_confirm(self, checkbox, sub_btn, path_btn, ran_btn, lbl_btn, canvas):	# confirmar subgrafo
		checkbox.active = False;
		sub_btn.disabled = True;
		path_btn.disabled = False;
		ran_btn.disabled = False;
		lbl_btn.disabled = False;
		canvas.subgraph_confirm();
	
	def sizes(self, root):
		print(str(root.children[0].width) + ", " + str(root.children[1].width) + ", " + str(root.children[2].width));
	
	def build(self):	# montar la app
		
		root = GridLayout();
		
		# panel de subgrafos
		
		subpanel = SubPanel();
		subpanel.init();
		
		# Pintar grafo inicial
		canvas = GraphCanvas();
		canvas.init(self.rand_graph(subpanel), 50);
		
		# Calculadora
		p = Path_Calc();
		
		# barra de herramientas
		lbl_or = Label(font_size='10', text='grafo', size_hint_y=None, height=25, size_hint_x=None, width=100);
		
		checkbox = CheckBox(size_hint_y=None, height=30, size_hint_x=None, width=100, active=True, color=(255,0,0))
		checkbox.bind(active=lambda x,y:canvas.on_or_active(checkbox.active));
		
		lbl_com = Label(font_size='10', text='complemento', size_hint_y=None, height=25, size_hint_x=None, width=100);
		
		checkbox_c = CheckBox(size_hint_y=None, height=30, size_hint_x=None, width=100, active=True, color=(0,0,255))
		checkbox_c.bind(active=lambda x,y:canvas.on_com_active(checkbox_c.active));
		checkbox_c.active = False;
		
		txt_input = TextInput(multiline=True, size_hint_x=None, width=100);
		
		res_btn = Button(font_size='10',text='Reiniciar pos', size_hint_y=None, height=30, size_hint_x=None, width=100);
		res_btn.bind(on_press=lambda x:canvas.recalc_vertexes_pos());
		
		path_btn = Button(font_size='10', text='Camino simple', size_hint_y=None, height=30, size_hint_x=None, width=100);
		path_btn.bind(on_press=lambda x:p.simple_path(canvas, txt_input, 0));
		
		ran_btn = Button(font_size='10',text='Random', size_hint_y=None, height=30, size_hint_x=None, width=100);
		ran_btn.bind(on_press=lambda x:canvas.set_graph(self.rand_graph(subpanel)));
		
		sub_btn = Button(font_size='10', text='Confirm. subgrafo', size_hint_y=None, height=30, size_hint_x=None, width=100);
		sub_btn.bind(on_press=lambda x:self.subgraph_confirm(checkbox_sub, sub_btn, path_btn, ran_btn, lbl_btn, canvas));
		
		lbl_btn = Button(font_size='10', text='Cambio etiquetas', size_hint_y=None, height=30, size_hint_x=None, width=100);
		lbl_btn.bind(on_press=lambda x:canvas.lbl_change(txt_input.text));
		
		lbl_sub = Label(font_size='10', text='subgrafo', size_hint_y=None, height=25, size_hint_x=None, width=100);
		
		checkbox_sub = CheckBox(size_hint_y=None, height=30, size_hint_x=None, width=100, active=True, color=(0,100,50))
		checkbox_sub.bind(active=lambda x,y:self.subgraph(checkbox_sub.active, sub_btn, path_btn, ran_btn, lbl_btn, canvas));
		checkbox_sub.active = False;
		
		toolbar = GridLayout(orientation="rl-tb", size_hint_x=None, width=100);
		toolbar.rows = 12;
		toolbar.cols = 1;
		toolbar.add_widget(ran_btn);
		toolbar.add_widget(res_btn);
		toolbar.add_widget(path_btn);
		toolbar.add_widget(lbl_or);
		toolbar.add_widget(checkbox);
		toolbar.add_widget(lbl_com);
		toolbar.add_widget(checkbox_c);
		toolbar.add_widget(sub_btn);
		toolbar.add_widget(lbl_sub);
		toolbar.add_widget(checkbox_sub);
		toolbar.add_widget(lbl_btn);
		toolbar.add_widget(txt_input);
		
		# montaje
		root.cols = 3;
		root.add_widget(canvas);
		root.add_widget(toolbar);
		root.add_widget(subpanel);
		
		# Metodo update se ejecutara periodicamente a razon de 60 hercios  
		Clock.schedule_interval(canvas.update, 1.0 / 60.0);
		Clock.schedule_interval(lambda x:subpanel.update(canvas), 1.0 / 60.0);

		return root;

if __name__ == '__main__':
    GraphApp().run();