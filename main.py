'''
GRaPH_ICS
disponible en github.com
'''

#	Modulos graficos de Kivy
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import (
	Color, Rectangle, Ellipse, Line
)

# Valores y Propiedades de Kivy
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, BooleanProperty
)

# Otros modulos de Kivy
from kivy.clock import Clock
from kivy.app import App

# Modulos de Python
import random as r
import operator as o
import math as m
from collections import deque

# Matriz expandible
class ExMatrix:

	data = None;    # Arreglo filas
	rows = None;	# Num. filas
	columns = None;	# Num. columnas
	
	# Valores por defecto
	def __init__(self):
	
		# Iniciar valores
		self.data = [];
		self.rows = 0;
		self.columns = 0;

	# Expandir tamaño de la matriz según necesidad
	def expand_matrix(self, n, m):
		
		# Insertar casillas 
		for i in range(n+1):
			if(i>=len(self.data)):
				self.data.append([]);
		for i in range(n+1):
			for j in range(m+1):
				if(j>=len(self.data[i])):
					self.data[i].append([]);
		
		# Calcular nuevo tamaño de la matriz
		self.rows = len(self.data);
		self.columns = len(self.data[0]);
	
	# Imprimir matriz en consola
	def print_matrix(self):
	
		# Imprimir cada fila en una nueva línea
		for i in range(len(self.data)):
			print(self.data[i]);
	
	# Introducir dato en una fila/columna
	def intro(self, datos, idx, idy):
	
		# Expandir matriz lo suficiente
		self.expand_matrix(idx, idy);
		
		# Introducir dato
		self.data[idx][idy] = datos;
		
	# Valores simetricos respecto a la diagonal, toma la mitad bajo la diagonal
	def mirror(self):
	
		# Volverla una matriz cuadrada
		if(self.rows>self.columns):
			self.expand_matrix(self.rows, self.rows);
		elif(self.columns>self.rows):
			self.expand_matrix(self.columns, self.columns);
			
		# Copiar los valores de la mitad bajo la diagonal a la mitad superior
		for i in range(self.rows):
			for j in range(self.columns):
				if(i<j):
					self.data[i][j] = self.data[j][i];

# Grafo conceptual
class Graph:

	V = None;	# Vértices
	E = None;	# Aristas
	Sub = None;	# Lista de subgrafos de interés: Pares ordenados: (Nombre del subgrafo, Subconjunto de V)
	vertices = 0; # Número de vértices
	edges = 0; # Número de aristas
	subgraphs = 0;	# Número de subgrafos
	
	# Iniciar propiedades
	def __init__(self, tst = False):
		
		# Inicializar como grafo sin vértices
		self.V = [];
		self.E = ExMatrix();
		self.Sub = dict();
		
		# Agregarse a sí mismo en la lista de subgrafos bajo el nombre de 'self'
		self.add_sub(self.V, 'self');
		
		# Notificarse al terminar
		if tst: 
			print("El grafo se ha iniciado.");
			self.print_ady();
			self.print_subs();
	
	# Imprimir |V| y |E|
	def vertices_and_edges(self):
	
		# |V| y |E|
		print("edges = "+str(self.edges)+", vertices = "+str(self.vertices));
	
	# Imprimir matriz de adyacencia
	def print_ady(self):
		
		# Señalar inicio de la impresión
		print('<Adyacencia del grafo>');
		
		# Avisar si el grafo no tiene vértices
		if self.vertices == 0: 
			print('Sin vértices');
			return;
		
		# Método de la ExMatrix
		self.E.print_matrix();
	
	# Establecer valor en la arista nm
	def edge(self, n, m, val = 1):
		
		# Introducir valor bajo la diagonal, para poder reflejarlo
		if n > m: self.E.intro(val, n, m);
		else: self.E.intro(val, m, n);
		
		# arista nm = arista mn
		self.E.mirror();
		
		# Incrementar en 1 el núm. de aristas si la adyacencia no es de un vértice hacia sí mismo
		if (not val == 0) and (not n == m): self.edges += 1;
	
	# Agregar/eliminar un conjunto de aristas
	def set_edges(self, arr, add = True):
	
		# Según la bandera, add, se eliminan o se agregan
		for pair in arr:
		
			# No proceder cuando se introduce una adyacencia de un vértice hacia sí mismo
			if pair[0] == pair[1]: continue;
			
			# Agregar/quitar según el caso
			if add: self.edge(pair[0], pair[1]);
			else: self.edge(pair[0], pair[1], 0);
	
	# Devolver adyacencia de vértices n y m
	def get_edge(self, n ,m):
	
		# Tomar de la matriz E
		return self.E.data[n][m];
	
	# Invertir arista
	def opp_edge(self, n, m):
	
		# Consultar valor e introducir su opuesto
		if self.get_edge(n, m) == 0: self.edge(n, m);
		else: self.edge(n, m, 0);
	
	# Agregar un vértice nuevo al grafo
	def insertVertex(self):
		
		# Agregar, de forma incremental, un id numérico a la lista de vértices
		self.V.append(self.vertices);
		
		# Hacer a un vértice adyacente a sí mismo
		self.edge(self.vertices, self.vertices);
		
		# Incrementar en 1 el núm. de vértices
		self.vertices += 1;
		
		# Agregar el vértice sin adyacencia a ninún otro anterior a él
		for i in range(self.vertices-1):
			self.edge(self.vertices-1, i, 0);
		
		# Agregarse/Actualizarse a sí mismo en la lista de subgrafos bajo el nombre de 'self'
		self.add_sub(self.V, 'self');
	
	# Hacer aleatorias las aristas
	def rand_edges(self, p):
		
		ra = 0.0;	# Valor para contrastar con la probabilidad p de agregar una arista al grafo
		
		# Recorrer la matriz de adyacencia y agregar aristas
		for i in range(self.vertices):
			for j in range(self.vertices):
				if j > i:
					ra = r.random();
					if ra <= p:
						self.edge(j, i);
					else:
						self.edge(j, i, 0);
	
	# Agregar aristas que conectan a dos vértices que están a distancia n
	def dist_edges(self, n):
	
		# Recorrer cada vértice y agregar uno de los dos pares que cumplen la condición
		for v in self.V:
			v_c = (v + n) % self.vertices;	# vértice emparejado con v
			self.edge(v_c, v);

	# Imprmir todos los subgrafos almacenados (Conjuntos de vértices)
	def print_subs(self):
	
		# Señalar inicio de la impresión
		print('<Subgrafos del grafo>');
	
		# Imprimir cada subgrafo almacenado junto con su nombre
		print(self.Sub.items());

	# Obtener un subgrafo almacenado (subconjunto de V)
	def get_sub(self, name):
	
		# Buscar en el diccionario, devolver el conjunto de vertices, o bien, None, si no está el nombre
		if name in self.Sub: return self.Sub[name];
		else: return None;

	# Agregar a la lista de subgrafos
	def add_sub(self, sub_V, name):
		
		# No agregar vacío si el grafo ya tiene vértices
		if sub_V == [] and not self.V == []: return;
		
		# Sumar 1 al número de subgrafos al agregar uno nuevo
		if name not in self.Sub: self.subgraphs += 1;
		
		# Reemplazar el subgrafo si ya existe, si no, guardarlo con un el nombre proporcionado/por defecto
		if name == None: self.Sub['subG'+str(len(self.Sub))] = sub_V;
		else: self.Sub[name] = sub_V;
	
	# Obtener subgrafo a partir de su nombre
	def get_subgraph(self, name):
		
		# Devolver el grafo sin aristas si el nombre no corresponde a un subgrafo almacenado
		if self.get_sub(name) == None: return Graph();
	
		SubG = Graph();	# Nuevo grafo a devolver
		SubV = self.get_sub(name);	# Subconjunto de V asociado al nombre
		
		# Insertar los vértices de SubV al grafo
		for i in range(len(SubV)):
			SubG.insertVertex();
		
		# Tomar las aristas del grafo involucradas
		for i in range(SubG.vertices):
			for j in range(SubG.vertices):
				if j >= i:
					SubG.edge(i, j, self.get_edge(SubV[i], SubV[j]));
		return SubG;
	
	# Obtener el grafo complemento
	def get_complement(self):
		
		Com = Graph();	# Grafo nuevo para no sobreescribir nada
		
		# Agregarle el mismo numero de vertices
		for i in range(self.vertices):
			Com.insertVertex();
			
		# Hacer que grafo Com copie las aristas del complemento
		Com.copy_inv_other_s_edges(self, True);
		return Com;
	
	# Copiar las aristas de otro grafo o de su complemento, del mismo tamaño
	def copy_inv_other_s_edges(self, G, inv = False):
	
		# Recorrer las aristas y asignarles el valor del grafo/complemento al que se copia
		for i in range(self.vertices):
			for j in range(self.vertices):
				if j >= i:
					if inv:
						if G.get_edge(j, i) == 0: self.edge(j, i);
						else: self.edge(j, i, 0);
					else: self.edge(j, i, G.get_edge(j,i));

# Calculadora para grafos
class GraphCalc:

	found_cliques = []; # Cliques almacenados en el alg. Bron-Kerbosch
	R1 = 0; # Vértices R del alg. Camino simple
	R2 = 0;
	ue = [];	# Vértices U del alg. Camino simple
	france = []; # Vértices F del alg. Camino simple
	peninsular = []; # Vértices F/P del alg. Camino simple
	uk = [];	# Vértices F/P/E del alg. Camino simple
	
	# Imprimir ultimos cliques encontrados
	def get_cliques(self):
	
		# Señalar inicio de la impresión
		print('<Cliques hallados>');
	
		# Imprimirlos en una nueva linea
		for k in self.found_cliques:
			print(k);
	
	# Coeficiente binomial
	def comb(self, n, k):
		
		# Devolver el valor entero
		return int ( m.factorial(n) / ( m.factorial(k) * ( m.factorial(n - k) ) ) );

	# Conjunto interseccion
	def intersection_set(self, A, B):
	
		I = [];	# Intersección
		
		# Recorrer cada vértice en A y verificar si está también en B
		for v in A:
			if o.contains(B, v): I.append(v);
		return I;

	# Conjunto de vecinos de un vertice
	def neighbor_set(self, v, G):
	
		N = [];	# Conjunto de vecinos
		
		# Recorrer cada vertice u y verificar si es vecino de v
		for u in range(G.vertices):
			if (not u == v) and (G.get_edge(u, v) == 1):
				N.append(u);
		return N;
	
	# Grados de un vértice
	def degrees(self, v, G, tst):
		
		# Devolver el tamaño del conjunto de vecinos
		N = self.neighbor_set(v, G);	# conjunto de vecinos de v
		
		# Imprimir vecinos de v1
		d = len(N);	# tamaño del conjunto de vecinos
		if tst: print("vecinos de "+str(v)+": "+str(N)+" para un total de "+str(d));
		
		return d;
	
	# Alg. Bron-Kerbosch para cliques maximales (forma básica)
	def bron_kerbosch(self, G, P_arg, tst = False, R_arg = [], X_arg = [], lvl = 1):
		
		'''
		Sin vértices pivote:
		La idea es hacer un arbol de búsqueda en el que cada rama acumula en R los vértices que han sido vecinos en todos los pasos anteriores, estos candidatos están en P (de los elmentos de P se seleccionan algunos en concreto, por lo que no es una cola) y al descartarse se trasladan a X. 
		'''
		
		# Computar sin alterar los valores de otras ramas
		P = P_arg.copy();
		R = R_arg.copy();
		X = X_arg.copy();
		
		# Limpiar cliques al comenzar
		if lvl == 1: self.found_cliques = [];
		
		# Imprmir entrada
		if tst:
			print("----------> llamada BK: nivel = "+str(lvl));
			print("R: "+str(R));
			print("P: "+str(P));
			print("X: "+str(X));
		
		# Guardar R como clique max. si P y X son vacíos
		if P == [] and X == []:
			self.found_cliques.append(R);
		
		# Recorrer vértices de P hasta que, por eliminación, P sea vacío
		while not P == []:
		
			v = P[0];	# Escoger el primer vertice de P, v
			Nv = self.neighbor_set(v, G);	# Calcular vecinos de v
			P_int_Nv = self.intersection_set(P, Nv);	# Restringir P a los vecinos de v
			X_int_Nv = self.intersection_set(X, Nv);	# Restringir X a los vecinos de v
			
			# Imprimir llamada recursiva que se hará
			if tst: print("vertice en P: "+str(v)+" tiene vecinos "+str(Nv)+". P_Nv = "+str(P_int_Nv)+" y X_Nv = "+str(X_int_Nv));
			
			# Hacer la llamada recursiva
			self.bron_kerbosch(G, P_int_Nv, tst, R + [v], X_int_Nv, lvl+1);
			
			# Imprimir traslación de v
			if tst: print("movemos "+str(v)+" desde P = "+str(P)+" hasta X = "+str(X));
			
			# Trasladar v desde P hasta X
			P.remove(v);
			X.append(v);
			
			# Imprimir P y X después de la traslación
			if tst: print("resulta en: P = "+str(P)+" y X = "+str(X));
		
	def bron_kerbosch_pivot(self):
		
		'''
		Con pivoting:
		La forma basica del algoritmo, descrito arriba, es ineficiente en el caso de grafos con muchos cliques no-maximales: hace una llamada recursiva por cada clique, maximal o no. Para ahorrar tiempo y permitir al algoritmo retroceder más rápido hacia ramas de busqueda que contienen cliques no maximales, Bron y Kerbosch introdujeron una variante del algoritmo que involucra un "vertice pivote" u, escogido de P (O de forma más general, como posteriores investigaciones mostraron, de P U X). 	
		Cualquier clique maximal debe incluir ya sea u o uno de sus no-vecinos porque, de lo contrario, el clique podría aumentar agregándole u. Por lo tanto, solo u y sus no vecinos necesitan ser probados como candidatos para el vértice v que es agregado a R en cada llamada recursiva.
		'''
		
		# Aún no implementado
		pass;
	
	def bron_kerbosch_order(self):
	
		'''
		Con ordenamiento de vertices:
		Un método alternativo de mejorar la forma basica del algoritmo Bron-Kerbosch involucra renunciar al pivoting en el nivel mas externo de la recusión y, en su lugar, escoger el orden de las llamadas recursivas con cuidado para minimizar los tamaños de los conjuntos P de vertices candidatos dentro de cada llamada recursiva.
		degen(G) de un grafo G es el minimo numero d tal que todo subgrafo de G tiene un vertice de grado d o menor. Todo grafo tiene un orden de degeneración, un orden de los vertices tal que cada vertice tiene d o menos vecinos que vienen más tarde en el orden; un orden de degeneración puede ser encontrado en tiempo lineal seleccionando repetidamente el vertice de menor grado entre los vertices restantes. Si el orden de los vertices v que el algoritmo Bron-Kerbosch recorre es un orden de degeneración, entonces el conjunto P de vertices candidatos en cada llamada (los vecinos de v que van después en el orden) tendrá, con seguridad, un tamaño de a lo sumo d. El conjunto X de vertices excluidos consistirá en todos los vecinos previos de v, y puede ser mucho más grande que d. En las llamadas recursivas al algoritmo bajo el nivel más alto de recursión, puede emplearse la versión con pivoting.
		'''
		
		# Aún no implementado
		pass;
	
	# Alg. Matula-Beck para encontrar un orden de degeneración
	def matula_beck_deg_order(self, G, tst = False):
		
		'''
		El algoritmo "implementa una cola de prioridad" (la prioridad puede cambiar durante su estadía en la cola) para extraer los vértices del grafo según sus grados, uno a uno, y de esa manera, producir un orden de degeneración.
		'''
		
		L = [];	# Arreglo de salida (orden de degeneración)
		deg = [];	# Arreglo de grados de cada vertice en el subgrafo actual
		D = [[]];	# Partición de los vertices según su grado (prioridad)
		
		# Señalar el comienzo
		if tst: print("---------> Deg. Order MB");
		
		# Almacenar los grados iniciales en deg
		for v in range(G.vertices):
			deg.append(self.degrees(v, G, tst));
		
		# Imprimir grados
		if tst: print("Grados: "+str(deg));
		
		num_parts = 0;	# Número de clases de la partición
		
		# Calcular partición
		for v in range(G.vertices):
		
			# Ampliar numero de clases de la partición si es necesario
			if deg[v] > num_parts:
				for i in range(deg[v] - num_parts):
					D.append([]);
				num_parts = len(D) - 1;
			
			# Agregar el vertice a su clase
			D[deg[v]].append(v);
		
		# Imprimir partición
		if tst: print("Partición: "+str(D));
		
		# Extraer el vértice de menor grado en el subgrafo restante
		for j in range(G.vertices):
		
			# Extraer un vértice, v, de la cola y ponerlo en L
			for i in range(len(D)):
				if not D[i] == []:
					v = D[i][0];
					L = [v] + L;
					D[i].remove(v);
					
					# Imprimir operación
					if tst: print("v = "+str(v)+" puesto en L = "+str(L)+" y removido de D["+str(i)+"] = "+str(D[i]));
					
					# Cambiar los grados de los vecinos de v
					for w in self.neighbor_set(v, G):
						if not o.contains(L, w):
							deg[w] = deg[w] - 1;
							
							# Cambiar prioridad de w en la cola
							D[deg[w]].append(w);
							D[deg[w]+1].remove(w);
							
							# Imprimir operación
							if tst:
								print("w = "+str(w)+" es vecino de "+str(v)+" y no está en L = "+str(L));
								print("w = "+str(w)+" tiene un grado menos: dw = "+str(deg[w])+" y su prioridad es: D["+str(deg[w])+"] = "+str(D[deg[w]]));
					break;
		
		# Imprimir orden final
		if tst: print("Orden de degeneración: L = "+str(L));
	
	# Iteracion del alg. Camino simple
	def simple_path_next(self, G, R, Vn, tst = False):
	
		NR = self.intersection_set(Vn, self.neighbor_set(R, G)); # Vecinos no visitados de R
		
		# Si no quedan vecinos sin visitar, terminar el camino en este sentido.
		if NR == []:
		
			# Imprimir operación
			if tst: print("fin del camino para R = " + str(R));
			return R;
		
		# si aún hay, tomar el primero, v, poner R en los vértices UE y marcar v como visitado 
		else:
			v = NR[0];
			if not o.contains(self.ue, R): self.ue.append(R);
			Vn.remove(v);
			
			# Imprimir operación
			if tst: print("El siguiente de R = " + str(R) + " es: "+str(v));
			return v;

	# Encontrar un camino desde un vértice fijo, s
	def simple_path(self, G, s, tst = False):
		
		'''
		Encontrar un camino simple desde s, implementa un deck para extender el camino hacia dos lados desde el vértice inicial
		'''
		
		P = deque(); # Camino
		V = G.V.copy();	# Vertices no visitados
		self.R1 = s;	# Ruso 1
		self.R2 = s;	# Ruso 2
		
		# Señalar el comienzo
		if tst: print("---------> Simple Path:");
		
		# Limpiar vértices al comenzar
		self.ue = [];
		self.france = [];
		self.peninsular = [];
		self.uk = [];
		
		# Comenzar el camino en s
		V.remove(s);
		P.append(s);
		
		# Extender el camino hacia la dirección de R1
		vf = self.simple_path_next(G, self.R1, V, tst);
		while(not vf == self.R1):
			self.R1 = vf;
			P.append(self.R1);
			vf = self.simple_path_next(G, self.R1, V, tst);
		
		# Determinar R1 definitivo
		self.R1 = vf;
		if o.contains(self.ue, self.R1): self.ue.remove(self.R1);
		
		# Imprimir camino parcial
		if tst: print("Camino parcial: "+str(P));
		
		# Extender el camino hacia la dirección de R2
		vf = self.simple_path_next(G, self.R2, V, tst);
		while(not vf == self.R2):
			self.R2 = vf;
			P.appendleft(self.R2);
			vf = self.simple_path_next(G, self.R2, V, tst);
		
		# Determinar R2 definitivo
		self.R2 = vf;
		if o.contains(self.ue, self.R2): self.ue.remove(self.R2);
		
		# Imprimir camino calculado
		if tst: print("Camino calculado: "+str(P));
		
		# Determinar los tipos para los vértices no visitados
		for v in V:
			count = 0;	# Contador de vecinos UE
			
			# Contar los vecinos UE de v
			for u in self.ue:
				if G.get_edge(v, u) == 1:
					count += 1;
					
			# Decidir sobre v
			if count > 1: 
				if tst: print(str(v)+" es francés.");
				self.france.append(v);
			elif count == 1:
				if tst: print(str(v)+" es peninsular o francés.");
				self.peninsular.append(v);
			else:
				if tst: print(str(v)+" Puede ser cualquier tipo.");
				self.uk.append(v);
		
		# imprimir tipos de vértice
		if tst:
			print("R1: "+str(self.R1));
			print("R2: "+str(self.R2));
			print("U: "+str(self.ue));
			print("F: "+str(self.france));
			print("F/P: "+str(self.peninsular));
			print("F/P/E: "+str(self.uk));

# Vértice visual
class VertexCanvas(Widget):
	
	id = NumericProperty(-1);	# Id del vertice
	pos_x = NumericProperty(0);	# Posición x
	pos_y = NumericProperty(0);	# Posición y
	colliding = BooleanProperty(False);	# Colisionando con otro vértice
	selected = BooleanProperty(False);	# Seleccionado para ser deslizado
	
	type = StringProperty('-');	# tipo de vertice
	sub = BooleanProperty(False); # seleccionado para subgrafo
	
	# Establecer id
	def set_id(self, id):
		self.id = id;
	
	# Establecer posición
	def pos_set(self, x, y):
		self.pos_x = x;
		self.pos_y = y;
	
	# Establecer tipo
	def set_type(self, t):
		self.type = t;
	
	# Seleccionar/deseleccionar
	def select(self, select):
		self.selected = select;
	
	# Verficar intersección con otros vértices
	def collide_siblings(self, d):
		
		# Recorrer vértices hermanos
		for v in self.parent.V:
		
			# Verificar si las hitboxes se intersectan
			if (not v.id == self.id) and (((v.pos_x <= self.pos_x <= v.pos_x + d) and (v.pos_y <= self.pos_y <= v.pos_y + d)) or ((v.pos_x <= self.pos_x + d <= v.pos_x + d) and (v.pos_y <= self.pos_y + d <= v.pos_y + d)) or ((v.pos_x <= self.pos_x <= v.pos_x + d) and (v.pos_y <= self.pos_y + d <= v.pos_y + d)) or ((v.pos_x <= self.pos_x + d <= v.pos_x + d) and (v.pos_y <= self.pos_y <= v.pos_y + d))):
				self.colliding = True;
				return;
		self.colliding = False;
	
	# Mover hacia una dirección aleatoria al estar colisionado
	def separate(self, d, tst = False):
	
		# Comprobar si está colisionado
		self.collide_siblings(d);
		if self.colliding: 
		
			ra1 = r.random(); # Dirección horizontal
			ra2 = r.random(); # Dirección vertical
			ra3 = r.random(); # Magnitud
			
			if ra1 <= 0.5:
			
				# Izquierda, Arriba
				if ra2 <= 0.5:
					self.pos_x -= ra3 * d; 
					self.pos_y += ra3 * d;
					
				# Izquierda, Abajo
				else: 
					self.pos_x -= ra3 * d; 
					self.pos_y -= ra3 * d;
			else:
			
				# Derecha, Arriba
				if ra2 <= 0.5: 
					self.pos_x += ra3 * d; 
					self.pos_y += ra3 * d;
				
				# Derecha, Abajo
				else: 
					self.pos_x += ra3 * d; 
					self.pos_y -= ra3 * d;
	
	# Al levantar el clic
	def on_touch_up(self, touch):
	
		# Deseleccionar si se levanta el clic
		if self.selected: self.select(False);
	
	# Al hundir el clic
	def on_touch_down(self, touch):
	
		d = self.parent.d; # Radio del vértice
	
		# Si el ratón está sobre el vértice al momento de hundir y ningún otro lo intersecta
		if (not self.colliding) and touch.x >= self.pos_x and touch.x < self.pos_x + d and touch.y >= self.pos_y and touch.y < self.pos_y + d:
			if not self.parent.set_sub:
			
				# Seleccionar si se le hizo clic, agregándole una marca
				self.parent.set_mark(self.id);
				self.select(True);
			
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
	
	# Al mover el ratón
	def on_touch_move(self, touch):
	
		d = self.parent.d;	# Radio del vértice
	
		# Mover vértice solo si no está activa la función de subgrafo.
		if not self.parent.set_sub:
		
			# Mover vértice si está seleccionado y el clic se mantiene.
			if self.selected:
			
				# Llevar el vértice hacia el ratón
				self.pos_set(touch.x - d / 2, touch.y - d / 2);
				
				# Quitar todas las marcas al mover un vértice de sitio
				self.parent.set_mark(-1);
			
			# Seleccionar el vértice si aún no lo estaba
			elif touch.x >= self.pos_x and touch.x < self.pos_x + d and touch.y >= self.pos_y and touch.y < self.pos_y + d:
				self.select(True);
		
		else:	# seleccionar con el paso del cursos para determinar subgrafo
			if touch.x >= self.pos_x and touch.x < self.pos_x + self.d and touch.y >= self.pos_y and touch.y < self.pos_y + self.d:
				if not self.sub:
					self.parent.V_sub.append(self.id);
					self.sub = True;	# seleccionar con el paso del cursor también (subgrafo)
					self.parent.log = "v = " + str(self.id);	# info del vertice
					self.parent.log += '\n'+"tipo = " + str(self.type);
					self.parent.show_subgraph();

# Dibujante de grafos
class GraphCanvas(Widget):
	
	d = NumericProperty(0);	# Diámetro de los vértices
	V = ObjectProperty(None);	# Vértices visuales
	view_V = ObjectProperty([]); # Subgrafo a mostrar
	original = BooleanProperty(True);	# Ver aristas del grafo
	complement = BooleanProperty(False);	# Ver aristas del complemento
	
	mark = NumericProperty(-1);	# primer vertice marcado
	end = NumericProperty(-1);	# segundo vertice marcado
	log = StringProperty('');	# output
	set_sub = BooleanProperty(False); # se está seleccionando un subgrafo
	V_sub = ObjectProperty([]);	# vertices del subgrafo en construcción
	display_new_sub = BooleanProperty(True);	# bandera para el panel
	
	# Actualizar el lienzo
	def update(self, G, d, tst = False):
		
		# Inicializar valores si no se ha hecho aún
		if self.V == None: self.init(G, d, tst);
		
		# Mover los vértices visuales que estén juntos
		for v in self.V:
			if not v.selected: v.separate(d, tst);
		
		# Redibujar
		self.draw(G);
	
	# Valores iniciales del lienzo
	def init(self, G, d, tst = False):
		
		# Establecer dibujo inicial
		self.set_graph(G, tst);
		
		# Establecer el diámetro inicial de los vértices
		self.d = d;
		
		# Imprimir vértices a representar
		if tst:
			for v in self.V:
				print("Vértice visual agregado: "+str(v.id));
			print("Subgrafo: "+str(self.view_V));
	
	# Establecer el grafo a representar
	def set_graph(self, G, tst = False):
	
		# No interferencia con la funcion de subgrafos
		#if self.set_sub: return;
		
		# Limpiar lienzo
		self.clear_widgets(self.children);
		
		# Vaciar lista de vértices visuales
		self.V = [];
		
		# Ver, por defecto, el grafo en su totalidad
		self.view_V = G.get_sub('self');
		
		# Bandera verde para agregar el grafo al panel
		#self.display_new_sub = True;
		
		# Agregar vértices visuales
		for v in range(G.vertices):
			u = VertexCanvas();
			u.set_id(v);
			self.V.append(u);
			self.add_widget(self.V[v]);
		
		#  Recalcular posiciones en el lienzo
		self.recalc_vertexes_pos(tst);
	
	# Reiniciar posiciones de los vertices
	def recalc_vertexes_pos(self, tst = False):
	
		n = len(self.V); # Número de vértices visuales
		r = self.height / 3; # Radio del círculo en torno al que se ubican los vértices
		
		# Quitar marcas al reiniciar
		#self.set_mark(-1);

		# Limpiar el log
		#if not self.set_sub: self.log = '';
		
		# Imprimir tamaño de lienzo al momento del cálculo
		print("Tamaño del lienzo usado para calcular los vértices= "+str(self.size));
		
		# Asignar posiciones en torno a un círculo 
		for v in self.V:
			angle = (2 * v.id * m.pi) / n;	# Ángulo del vértice v
			cx = r * m.cos(angle) + (self.width / 2); # Centro x
			cy = r * m.sin(angle) + (self.height / 2) # Centro y
			
			# Guardar posición
			v.pos_set(cx, cy);
			
			# Notificar posicionamiento
			if tst:
				print("Posición del vértice v["+str(v.id)+"] = ["+str(v.pos_x)+", "+str(v.pos_y)+"]");
	
	# Rutina de dibujo
	def draw(self, G):
		
		# Limpiar el dibujo anterior
		self.canvas.clear();
		
		# Fondo oscuro
		with self.canvas:
			Color(.27, 0, .15, mode='rgb');
			Rectangle(size=self.size, pos=self.pos);
		
		# Dibujar aristas
		self.draw_edges(G);
		
		# Dibujar vértices
		self.draw_vertexes();
		
		'''
		with self.canvas:
			Label(font_size='15', text='>> '+self.log, center_x=self.width/3 - 12, top=self.height/6);
		'''
	
	# Dibujar los vertices del subgrafo actual
	def draw_vertexes(self):
	
		# Si un vértice está listado en la vista actual, dibujarlo.
		for v in self.V:
			if o.contains(self.view_V, v.id): self.draw_vertex(v);

	# Dibujar un vertice
	def draw_vertex(self, v):
	
		# Dibujo del vértice
		with self.canvas:
			
			# Borde blanco
			Color(1, 1, 1, mode='rgb');
			Line(ellipse=(v.pos_x, v.pos_y, self.d, self.d));
			
			# Color según el estado del vértice gráfico
			if not v.selected: Color(.27, 0, .15, mode='rgb');	# Fondo
			if self.mark == v.id: Color(1, 1, 0, mode='rgb');	# Amarillo
			#if self.end == v.id: Color(200, 0, 10, mode='rgb');
			#if v.sub: Color(0, 100, 50, mode='rgb');
			
			# Relleno
			Ellipse(pos=(v.pos_x, v.pos_y), size=(self.d, self.d));
			
			# Etiqueta
			Label(font_size='10', center_x=v.pos_x+self.d/2, top=v.pos_y+60, text=str(v.id));
	
	# Dibujar las aristas
	def draw_edges(self, G):
	
		r = self.d/2; # Radio de los vértices
		
		# Recorrer los pares de vértices visuales
		with self.canvas:
			for v in self.V:
				for u in self.V:
					if v.id > u.id:
					
						# Verificar si ambos vértices están en el subgrafo a representar
						if o.contains(self.view_V, v.id) and o.contains(self.view_V, u.id):
						
							# Dibujar una arista azul si está activado el complemento
							if self.complement and G.get_edge(u.id, v.id) == 0:
								Color(0, 0, 1, mode='rgb');
								self.draw_edge(v, u, r);
							
							# Dibujar una arista roja si está activado el grafo original
							elif self.original and G.get_edge(u.id, v.id) == 1:
								Color(1, 0, 0, mode='rgb');
								self.draw_edge(v, u, r);

	# Dibujar una arista
	def draw_edge(self, v1, v2, r):
		x1 = v1.pos_x;
		y1 = v1.pos_y;
		x2 = v2.pos_x;
		y2 = v2.pos_y;
		Line(points=[r+x1 ,r+y1 ,r+x2 ,r+y2], width=1);
		
	# Manejo de marcas
	def set_mark(self, v):
		if self.set_sub: return;	# no interferencia con la funcion de subgrafos
		if v == -1:	# quitar 1ra y 2da marcas
			self.mark = v;
			self.end = v;
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
			e = self.G.get_edge(self.mark, v);	# informar sobre la arista si se marca un segundo vertice
			self.end = v;
			if e == 0: self.log = "edge (" + str(self.mark) + ", " + str(v) + ") está en Com."+'\n'+"(Otro clic para trasladar)"; 
			else: self.log = "edge (" + str(self.mark) + ", " + str(v) + ") está en G."+'\n'+"(Otro clic para trasladar)"; 
	
	def auto_add_subs(self, subs, names, panel):	# agregar subgrafos automaticamente
		for i in range(len(subs)):
			self.subgraph(True);
			for s in subs[i]:
				self.V_sub.append(s);
				self.V[s].sub = True;
				self.log = "v = " + str(self.V[s].id);	# info del vertices
				self.log += '\n'+"tipo = " + str(self.V[s].type);
			#print(str(names[i])+" en proceso con bandera verde en: "+str(self.display_new_sub));
			self.subgraph_confirm(names[i]);
			panel.update(self);
		#print(self.G.Sub);
	
	def show_subgraph(self):	# mostrar en el campo de texto el subgrafo que se está construyendo
		self.parent.children[1].children[1].text = "subgrafo: "+str(self.V_sub);	# imprimir en el campo de texto
		#print(self.V_sub);
	
	def reset_subgraph(self):	# desmarcar vertices al terminar de construir subgrafo
		self.log = "";
		for v in self.V:
			if v.sub: 
				self.display_new_sub = True;	# no dar bandera verde al panel si no hubo ningun vertice seleccionado
				v.sub = False;
		self.set_sub = False;
	
	def subgraph_confirm(self, name):	# Confirmar subgrafo construido
		sub_aux = self.V_sub;
		self.G.add_sub(sub_aux, name);
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
		if not l[0].isnumeric(): return;	# control provisional de la entrada
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

class SubPanel(GridLayout):	# panel de subgrafos
	
	Sub = [];	# lista de nombres de los subgrafos almacenados
	up_btn = Button(font_size='10', text='/|', size_hint_y=None, height=30, size_hint_x=None, width=30);	# boton up
	dwn_btn = Button(font_size='10', text='|/', size_hint_y=None, height=30, size_hint_x=None, width=30);	# boton dwn
	first_sub_to_show = 0;	# primer subgrafo a ser mostrado en el panel (de arriba hacia abajo)

	def sort_subs(self, GC, max_min):	# ordenar subgrafos segun tamaño del subconjunto
		sorted = [];
		k = 0;
		while(not len(sorted) == len(self.Sub)):
			#print("tamaño: "+str(k));
			arr_aux = [];
			for name in self.Sub:
				sub = GC.G.get_sub(name)[1];
				if len(sub) == k: arr_aux.append(name);
			if max_min:
				sorted = arr_aux + sorted;
			else: 
				sorted = sorted + arr_aux;
			k += 1;
		
		#print("subs: "+str(self.Sub));
		print("------------------------------");
		print("sorted: "+str(sorted));
		#print("------------------------------");
		
		self.Sub = sorted;
		self.first_sub_to_show = 0;	# ir al inicio de la lista de botones
		self.reprint_subs(GC);	# actuaizar panel con botones organizados

	def add_funct_on_panel(self, i, b, GC): # agregar botones (recursivo). Por alguna razón, con un for no funciona.
		if i > b-1: return;	# el indice llega hasta b-1 para b botones
		sub_name = self.Sub[self.first_sub_to_show + i];
		aux_btn = Button(font_size='10', text=sub_name, size_hint_y=None, height=30, size_hint_x=None, width=100);
		#print("btn = "+str(sub_name));
		aux_btn.bind(on_press=lambda x:self.display_subgraph(GC, sub_name));
		self.add_widget(aux_btn);
		self.add_funct_on_panel(i+1, b, GC);

	def go_up(self):	# funcion del boton arriba
		if self.first_sub_to_show == 0: return;	# inicio de la lista
		self.first_sub_to_show -= 1;	# retroceder en la lista

	def go_down(self):	# funcion del boton abajo
		if len(self.Sub) <= 18: return; # no hace nada si aún no hay suficientes botones que mostrar
		if self.first_sub_to_show == len(self.Sub) - 18: return;	# fin de la lista
		self.first_sub_to_show += 1;	# avanzar en la lista
	
	def restart(self):	# reiniciar el panel 
		self.Sub = [];	# vaciar lista de nombres
		self.clear_widgets(self.children);	# limpiar botones
		self.add_widget(self.up_btn);	# agregar de nuevo los botones arriba/abajo
		self.add_widget(self.dwn_btn);

	def display_subgraph(self, GC, name):	# pintar en el canvas el subgrafo seleccionado
		arr = GC.G.get_sub(name)[1];
		name_sub = GC.G.get_sub(name)[0];
		print(GC.G.get_subgraph(name_sub));
		#print("array to display: "+str(arr)+" from sub named: "+str(name_sub));
		GC.view_V = arr;

	def reprint_subs(self, GC):	# imprimir los botones que alcancen en el panel
		n = len(self.children) - 1;
		for i in range(n):
			#print(self.children[0].text);
			self.remove_widget(self.children[0]);	# limpiar canvas, menos el boton arriba
		#print("-----------------");
		#print(str(len(self.children))+" is "+str(self.children[0].text));
		add_num = n-1;
		if add_num > 18: add_num = 18;
		#print("hay que agregar "+str(n-1)+" subgrafos al panel y el botón de abajo.");
		self.add_funct_on_panel(0, add_num, GC);	# agregar botones recursivamente
		self.add_widget(self.dwn_btn); # pintar el boton abajo de ultimo

	def update(self, GC):	# actualizar el panel
		#print("botones en total: "+str(len(self.children)));
		if GC.display_new_sub and (not len(GC.G.Sub) == len(self.Sub)):	# esperar la bandera, comprobar lista de G
			name = GC.G.Sub[len(self.Sub)][0];	# copiar el nuevo nombre a la lista propia
			self.Sub.append(name);
			#print("hay que imprimir: "+name);
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

# Aplicacion gráfica
class GraphApp(App):
	
	G = Graph(); # Grafo principal
	n = 0; # Número inicial de vértices
	d = 0; # Diámetro de los vértices visuales
	
	# Preparar un grafo inicial
	def prepare_graph(self, n = 1, d = 20, p = .2):
		
		# Establecer el diámetro de los vértices
		self.d = d;
		
		# Establecer el número de vértices
		self.n = n
		
		# Agregar n vértices y hacer aleatorias las aristas
		for i in range(self.n):
			self.G.insertVertex();
		self.G.rand_edges(p);
		
		return self.G;
	
	def void_text(self, input):
		input.text = '';
	
	def count_subs(self, lbl, panel):	# contador de subgrafos almacenados
		lbl.text = "subg's: "+str(len(panel.Sub))
	
	def subgraph(self, value, sub_btn, path_btn, ran_btn, lbl_btn, canvas):	# mostrar/ocultar botones y lanzar funcion
		sub_btn.disabled = not value;
		path_btn.disabled = value;
		ran_btn.disabled = value;
		lbl_btn.disabled = value;
		canvas.subgraph(value);
	
	def subgraph_confirm(self, checkbox, sub_btn, path_btn, ran_btn, lbl_btn, canvas):	# confirmar subgrafo construido
		checkbox.active = False;
		sub_btn.disabled = True;
		path_btn.disabled = False;
		ran_btn.disabled = False;
		lbl_btn.disabled = False;
		canvas.subgraph_confirm(None);
	
	# Montaje de la app
	def build(self):
		
		'''
		# panel de subgrafos
		subpanel = SubPanel();
		subpanel.init();
		
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
		
		cliq_btn = Button(font_size='10', text='Cliques', size_hint_y=None, height=30, size_hint_x=None, width=100);
		cliq_btn.bind(on_press=lambda x:p.calc_cliques(canvas, subpanel));
		
		path_btn = Button(font_size='10', text='Camino simple', size_hint_y=None, height=30, size_hint_x=None, width=100);
		path_btn.bind(on_press=lambda x:p.simple_path(canvas, txt_input, 0, subpanel));
		
		ran_btn = Button(font_size='10',text='Random', size_hint_y=None, height=30, size_hint_x=None, width=100);
		ran_btn.bind(on_press=lambda x:canvas.set_graph(self.rand_graph(subpanel)));
		
		sub_btn = Button(font_size='10', text='Confirm. subgrafo', size_hint_y=None, height=30, size_hint_x=None, width=100);
		sub_btn.bind(on_press=lambda x:self.subgraph_confirm(checkbox_sub, sub_btn, path_btn, ran_btn, lbl_btn, canvas));
		
		lbl_btn = Button(font_size='10', text='Cambio etiquetas', size_hint_y=None, height=30, size_hint_x=None, width=100);
		lbl_btn.bind(on_press=lambda x:canvas.lbl_change(txt_input.text));
		
		void_btn = Button(font_size='10', text='Vaciar', size_hint_y=None, height=30, size_hint_x=None, width=100);
		void_btn.bind(on_press=lambda x:self.void_text(txt_input));
		
		lbl_sub = Label(font_size='10', text='subgrafo', size_hint_y=None, height=25, size_hint_x=None, width=100);
		
		checkbox_sub = CheckBox(size_hint_y=None, height=30, size_hint_x=None, width=100, active=True, color=(0,100,50))
		checkbox_sub.bind(active=lambda x,y:self.subgraph(checkbox_sub.active, sub_btn, path_btn, ran_btn, lbl_btn, canvas));
		checkbox_sub.active = False;
		
		lbl_sub_n = Label(font_size='10', text="subg's: "+str(len(subpanel.Sub)), size_hint_y=None, height=25, size_hint_x=None, width=100);
		
		toolbar = GridLayout(orientation="rl-tb", size_hint_x=None, width=100);
		toolbar.rows = 15;
		toolbar.cols = 1;
		toolbar.add_widget(ran_btn);
		toolbar.add_widget(res_btn);
		toolbar.add_widget(path_btn);
		toolbar.add_widget(cliq_btn);
		toolbar.add_widget(lbl_or);
		toolbar.add_widget(checkbox);
		toolbar.add_widget(lbl_com);
		toolbar.add_widget(checkbox_c);
		toolbar.add_widget(sub_btn);
		toolbar.add_widget(lbl_sub);
		toolbar.add_widget(checkbox_sub);
		toolbar.add_widget(lbl_btn);
		toolbar.add_widget(void_btn);
		toolbar.add_widget(txt_input);
		toolbar.add_widget(lbl_sub_n);
		
		'''
		# Preparar grafo inicial
		self.prepare_graph(10, 30, .1);
		
		# Widget raíz
		root = GridLayout();
		root.cols = 3;
		
		# Lienzo del grafo
		graph_canvas = GraphCanvas();
		
		# Contenido de las 3 columnas (lienzo, barra y panel)
		root.add_widget(graph_canvas);
		
		# Actualizar el contenido del lienzo con el grafo de la aplicación
		Clock.schedule_interval(lambda x:graph_canvas.update(self.G, self.d, True), 1.0 / 60.0);
		
		'''
		Clock.schedule_interval(lambda x:subpanel.update(canvas), 1.0 / 60.0);
		Clock.schedule_interval(lambda x:self.count_subs(lbl_sub_n, subpanel), 1.0 / 60.0);
		'''
		
		return root;

if __name__ == '__main__':
    GraphApp().run();