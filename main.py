'''
GRaPH_ICS
disponible en github.com
'''

#	Modulos graficos de Kivy
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
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
	
	# Insertar varios vértices
	def insert_Vertexes(self, n):
		
		# Repetir n veces la inserción
		for i in range(n):
			self.insertVertex();
	
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
		if sub_V == [] and not self.V == []: return None;
		
		# Sumar 1 al número de subgrafos al agregar uno nuevo
		if name not in self.Sub: self.subgraphs += 1;
		
		# Reemplazar el subgrafo si ya existe, si no, guardarlo con un el nombre proporcionado/por defecto
		if name == None: name = 'subG'+str(len(self.Sub));
		self.Sub[name] = sub_V;
		
		return name;
	
	# Quitar de la lista de subgrafos
	def del_sub(self, name):
		
		# No hacer nada si se recibe nombre igual a None
		if name == None: return;
		
		# Restar 1 al número de subgrafos al quitar uno
		if name in self.Sub: 
			self.subgraphs -= 1;
			
			# Quitar el subgrafo
			del self.Sub[name];
	
	# Obtener subgrafo a partir de su nombre
	def get_subgraph(self, name):
		
		# Devolver el grafo sin aristas si el nombre no corresponde a un subgrafo almacenado
		if self.get_sub(name) == None: return Graph();
	
		SubG = Graph();	# Nuevo grafo a devolver
		SubV = self.get_sub(name);	# Subconjunto de V asociado al nombre
		
		# Insertar los vértices de SubV al grafo
		SubG.insert_Vertexes(len(SubV));
		
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
		Com.insert_Vertexes(self.vertices);
			
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
	
	# Señalar un camino
	def mark_path(self, path):
		
		# No hacer nada si el camino no tiene, al menos, inicio y final distintos
		if len(path) < 2: return;
		
		# Limpiar otra señalización
		for v in range(self.vertices):
			for u in range(self.vertices):
				if v > u:
					if self.get_edge(v, u) > 1: self.edge(v, u, 1);
		
		# Señalizar nuevo camino
		for i in range(len(path)-1):
			if self.get_edge(path[i], path[i+1]) > 0: self.edge(path[i], path[i+1], 2);

# Calculadora para grafos
class GraphCalc:

	found_cliques = []; # Cliques almacenados en el alg. Bron-Kerbosch
	R1 = 0; # Vértices R del alg. Camino simple
	R2 = 0;
	ue = [];	# Vértices U del alg. Camino simple
	france = []; # Vértices F del alg. Camino simple
	peninsular = []; # Vértices F/P del alg. Camino simple
	uk = [];	# Vértices F/P/E del alg. Camino simple
	
	# Obtener un resultado con etiquetas cambiadas
	def res_sub(self, res, view_V):
		
		arr = []; # Resultado con etiquetas cambiadas
		
		# Cambiar etiquetas, una a una
		for i in res:
			arr.append(view_V[i]);
		return arr;
	
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
		
		# Devolver vacío si v es negativo
		if v < 0: return [];
	
		N = [];	# Conjunto de vecinos
		
		# Recorrer cada vertice u y verificar si es vecino de v
		for u in range(G.vertices):
			if (not u == v) and (G.get_edge(u, v) > 0):
				N.append(u);
		return N;
	
	# Grados de un vértice
	def degrees(self, v, G, tst = False):
		
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
	
	#Alg. Bron-Kerbosch para cliques maximales (mejorado con pivoting)
	def bron_kerbosch_piv(self, G, P_arg, tst = False, R_arg = [], X_arg = [], lvl = 1):
		
		'''
		Con pivoting:
		Ejecutar el algoritmo sobre el conjunto de u más sus no-vecinos, u es el vértice pivote.
		'''
		
		# Computar sin alterar los valores de otras ramas
		P = P_arg.copy();
		cands = P.copy();
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
		
		# Escoger pivote del conjunto P U X, el de mayor grado
		U = P + X;	# Unión
		u = -1; # Pivote
		
		# Agregar subgrafo auxiliar P U X
		G.add_sub(U, 'aux');
		if tst: print("P U X: ",G.get_sub('aux'));
		
		# Calcular orden por grados de P U X
		order = self.deg_order(G.get_subgraph('aux'));
		
		# Trabajarlo de mayor a menor
		order.reverse();
		if tst: print("Orden por grados: ",order);
		
		# Trabajarlo con las etiquetas de P U X
		order = self.res_sub(order, U);
		if tst: print("Orden por grados (label): ",order);
		
		# Borrar el subgrafo auxiliar
		G.del_sub('aux');
		if tst: print("auxiliar: ",G.get_sub('aux'));
		
		# Escoger el primer vértice de mayor grado como pivote
		for vx in order:
			if o.contains(U, vx): 
				u = vx;
				break;
		
		Nu = self.neighbor_set(u, G);	# Vecinos del pivote
		
		# Imprimir elección del pivote
		if tst:
			print("Vértice pivote: ",u," escogido de ",U," tiene vecinos: ",Nu);
		
		# Descartar los vecinos del pivote del conjunto de candidatos
		for vx in Nu:
			if o.contains(cands, vx): cands.remove(vx);
		
		# Imprimir candidatos
		if tst:
			print("Los candidatos son: ",cands);
		
		# Recorrer vértices candidatos hasta que, por eliminación, no haya ninguno.
		while not cands == []:
		
			v = cands[0];	# Escoger el primer vertice candidato, v
			Nv = self.neighbor_set(v, G);	# Calcular vecinos de v
			P_int_Nv = self.intersection_set(P, Nv);	# Restringir P a los vecinos de v
			X_int_Nv = self.intersection_set(X, Nv);	# Restringir X a los vecinos de v
			
			# Imprimir llamada recursiva que se hará
			if tst: print("vertice candidato: "+str(v)+" tiene vecinos "+str(Nv)+". P_Nv = "+str(P_int_Nv)+" y X_Nv = "+str(X_int_Nv));
			
			# Hacer la llamada recursiva
			self.bron_kerbosch_piv(G, P_int_Nv, tst, R + [v], X_int_Nv, lvl+1);
			
			# Imprimir traslación de v
			if tst: print("movemos "+str(v)+" desde P = "+str(P)+" hasta X = "+str(X));
			
			# Trasladar v desde P hasta X
			P.remove(v);
			X.append(v);
			
			# Siguiente candidato
			cands.remove(v);
			
			# Imprimir P y X después de la traslación
			if tst: print("resulta en: P = "+str(P)+" y X = "+str(X));
	
	# Alg. Bron-Kerbosch para cliques maximales (forma básica)
	def bron_kerbosch_basic(self, G, tst = False):
		
		# Ejectutar el algoritmo sin pivoting
		self.bron_kerbosch(G, G.V, tst);
	
	# Alg. Bron-Kerbosch para cliques maximales (con pivoting)
	def bron_kerbosch_pivot(self, G, tst = False):
		
		# Ejectutar el algoritmo con pivoting
		self.bron_kerbosch_piv(G, G.V, tst);
	
	# Alg. Bron-Kerbosch para cliques maximales (mejorado con un orden de degen.)
	def bron_kerbosch_order(self, G, tst = False):
	
		'''
		Con ordenamiento de vertices:
		Se ejecuta el algoritmo Bron-Kerbosch con un orden de degeneración P como el nivel de recursión más externo.
		'''
		
		# Calcular orden de degeneración
		P = self.matula_beck_deg_order(G, tst);
		
		# Ejectutar el algoritmo con pivoting
		self.bron_kerbosch_piv(G, P, tst);
	
	# Orden de los vértices por grados
	def deg_order(self, G, tst = False):
		
		k = 0; # Grado del vértice
		L = []; # Orden de los vértices
		V = G.V.copy(); # Vértices del grafo
		
		# Agregar vértice a vértice, según su grado
		while(len(L) < len(G.V)):
			if tst: print("L = ",L,", V = ",V);
			for v in G.V:
				if (o.contains(V, v)) and (self.degrees(v, G) == k):
					if tst: print(v," está en V y tiene grado ",self.degrees(v, G));
					L.append(v);
					V.remove(v);
			k += 1;
		
		# Imprimir orden
		if tst: print("Orden por grados: ",L);
		
		return L;
	
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
		
		# Devolver el orden desde el vértice de menor grado
		L.reverse();
		
		# Imprimir orden final
		if tst: print("Orden de degeneración: L = "+str(L));
		
		return L;
	
	# Iteracion del alg. Camino simple/doble
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

	# Encontrar un camino que inicie en un vértice fijo, s.
	def simple_path(self, G, s, tst = False):
		
		'''
		Encontrar un camino desde s
		'''
		
		P = deque(); # Camino
		V = G.V.copy();	# Vertices no visitados
		self.R1 = s;	# Ruso 1
		self.R2 = s;	# Ruso 2
		
		# Notificar llamada a la función
		if tst: 
			print("---------> Simple Path:");
			print("vértices: ",V);
			print("Comienza en: ",s);
		
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
		
		# Determinar R2 definitivo
		if o.contains(self.ue, self.R2): self.ue.remove(self.R2);
		
		# Imprimir camino calculado
		if tst: print("Camino calculado: "+str(P));
		
		# Determinar los tipos para los vértices no visitados
		for v in V:
			count = 0;	# Contador de vecinos UE
			
			# Contar los vecinos UE de v
			for u in self.ue:
				if G.get_edge(v, u) > 0:
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
		
		# imprimir tipos de vértices
		if tst:
			print("R1: "+str(self.R1));
			print("R2: "+str(self.R2));
			print("U: "+str(self.ue));
			print("F: "+str(self.france));
			print("F/P: "+str(self.peninsular));
			print("F/P/E: "+str(self.uk));

	# Encontrar un camino que pase por un vértice fijo, s
	def double_path(self, G, s, tst = False):
		
		'''
		Encontrar un camino doble que pase por s, implementa un deck para extender el camino hacia dos lados desde el vértice inicial
		'''
		
		P = deque(); # Camino
		V = G.V.copy();	# Vertices no visitados
		self.R1 = s;	# Ruso 1
		self.R2 = s;	# Ruso 2
		
		# Notificar llamada a la función
		if tst: 
			print("---------> Double Path:");
			print("vértices: ",V);
			print("Pasa por: ",s);
		
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
		
		# Dar vuelta a la lista de vértices ue para almacenar en orden correcto los UE
		self.ue.reverse();
		
		# Extender el camino hacia la dirección de R2
		vf = self.simple_path_next(G, self.R2, V, tst);
		while(not vf == self.R2):
			self.R2 = vf;
			P.appendleft(self.R2);
			vf = self.simple_path_next(G, self.R2, V, tst);
		
		# Determinar R2 definitivo
		self.R2 = vf;
		if o.contains(self.ue, self.R2): self.ue.remove(self.R2);
		
		# Dar vuelta a la lista de vértices ue, para encajar con R1 y R2
		self.ue.reverse();
		
		# Imprimir camino calculado
		if tst: print("Camino calculado: "+str(P));
		
		# Determinar los tipos para los vértices no visitados
		for v in V:
			count = 0;	# Contador de vecinos UE
			
			# Contar los vecinos UE de v
			for u in self.ue:
				if G.get_edge(v, u) > 0:
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
		
		# Imprimir tipos de vértice.
		if tst:
			print("R1: "+str(self.R1));
			print("R2: "+str(self.R2));
			print("U: "+str(self.ue));
			print("F: "+str(self.france));
			print("F/P: "+str(self.peninsular));
			print("F/P/E: "+str(self.uk));
	
	# Cálculo de cotas inferiores para caminos peninsulares/franco-españoles
	def pen_path(self, G, tst = False):
		
		per = self.france + self.peninsular + self.uk; # Periferias
		
		# Agregar subgrafo de periferias
		G.add_sub(per, 'periferias');
		if tst: print("Periferias: ",G.get_sub('periferias'));
		
		# Hacer el cálculo para todos los vértices de la periferia
		for i in range(len(per)):
			
			# Calcular un camino simple desde v en el grafo de periferias
			self.simple_path(G.get_subgraph('periferias'), i);
			
			# Trabajar resultados con las etiquetas que corresponden
			v = self.res_sub([i],per)[0];
			ue = self.res_sub(self.ue,per);
			R1 = self.res_sub([self.R1],per)[0];
			R2 = self.res_sub([self.R2],per)[0];
			
			# Imprimir camino peninsular/franco-español de cada vértice
			if R1 == R2:
				print(v, ' tiene un cfe de, al menos, ',len(ue));
				print('Camino simple: ',[R2]+ue);
			else:
				print(v, ' tiene un cfe de, al menos, ',len(ue)+1);
				print('Camino simple: ',[R2]+ue+[R1]);
			
		# Borrar el subgrafo de periferias
		G.del_sub('periferias');
		if tst: print("Periferias: ",G.get_sub('periferias'));

# Vértice visual
class VertexCanvas(Widget):
	
	id = NumericProperty(-1);	# Id del vertice
	pos_x = NumericProperty(0);	# Posición x
	pos_y = NumericProperty(0);	# Posición y
	colliding = BooleanProperty(False);	# Colisionando con otro vértice
	selected = BooleanProperty(False);	# Seleccionado para ser deslizado
	sub = BooleanProperty(False); # Seleccionado para construir un subgrafo
	
	type = StringProperty('-');	# tipo de vertice
	
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
	
	# Verficar intersección con el cursor
	def collide_cursor(self, touch):
		
		d = self.parent.d; # Diámetro del vértice
		
		if touch.x >= self.pos_x and touch.x < self.pos_x + d and touch.y >= self.pos_y and touch.y < self.pos_y + d:
			return True;
		else:	return False;
	
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
	
		# Si el ratón está sobre el vértice al momento de hundir clic y ningún otro lo intersecta
		if (not self.colliding) and self.collide_cursor(touch):
			
			# Si el dibujante no está creando un subgrafo, gestionar su marca
			if not self.parent.set_sub:
				self.parent.set_mark(self.id);
				self.select(True);
			
			# Si el dibujante está creando subgrafo, agregarse a/eliminarse de la selección.
			else:
				self.subgraph(True);
	
	# Al mover el ratón sosteniendo el clic
	def on_touch_move(self, touch):
	
		d = self.parent.d;	# Diámetro del vértice
	
		# Mover vértice solo si no está activa la función de subgrafo.
		if not self.parent.set_sub:
		
			# Mover vértice si está seleccionado y el clic se mantiene.
			if self.selected:
			
				# Llevar el vértice hacia el ratón si este último está sobre el lienzo
				if touch.x + d / 2 < self.parent.width:
					self.pos_set(touch.x - d / 2, touch.y - d / 2);
				
				# Quitar todas las marcas al mover un vértice de sitio
				self.parent.set_mark(-1);
			
			# Seleccionar el vértice si aún no lo estaba
			elif self.collide_cursor(touch):
				self.select(True);
			
		# Seleccionar para el subgrafo con el paso del cursor si la función está activa
		else:
			if self.collide_cursor(touch):
				self.subgraph(False);
		
	# Agregarse/Eliminarse a sí mismo del subgrafo en construcción
	def subgraph(self, reverse):
		
		# Revertir el estado de selección actual
		if reverse:
			if not self.sub:
				
				# Agregarse a la selección
				self.parent.V_sub.append(self.id);
				
				# Identificarse como vértice del subgrafo 
				self.sub = True;
					
			# Si ya estaba seleccionado, deseleccionarse
			else:
				self.parent.V_sub.remove(self.id);
				self.sub = False;
			
		# Seleccionar si no lo está actualmente
		else:
			if not self.sub:
				self.parent.V_sub.append(self.id);
				self.sub = True;
		
		# Actualizar la salida 
		self.parent.out = str(self.parent.V_sub);

# Dibujante de grafos
class GraphCanvas(Widget):
	
	G = Graph(); # Grafo asociado
	C = GraphCalc(); # Calculadora
	d = NumericProperty(0);	# Diámetro de los vértices
	V = ObjectProperty(None);	# Vértices visuales
	view_V = ObjectProperty([]); # Vértices del subgrafo a mostrar
	view_name = StringProperty(''); # Nombre del subgrafo a mostrar
	original = BooleanProperty(True);	# Ver aristas del grafo
	complement = BooleanProperty(False);	# Ver aristas del complemento
	mark = NumericProperty(-1);	# Primer vertice marcado
	end = NumericProperty(-1);	# Segundo vertice marcado
	edge_on_G = BooleanProperty(False);	# Arista seleccionada está en el grafo
	invert = BooleanProperty(False);	# Inveritr Arista seleccionada
	num_subs = NumericProperty(0);	# Número de subgrafos almacenados de G
	set_sub = BooleanProperty(False); # Se está seleccionando un subgrafo
	V_sub = ObjectProperty([]);	# Vétices del subgrafo en construcción
	out = ''; # Salida de funciones
	
	# Actualizar el lienzo
	def update(self, toolbar, subpanel, tst = False, G_0 = Graph(), d_0 = 20):
		
		# Inicializar valores si no se ha hecho aún
		if self.V == None: self.init(G_0, subpanel, d_0, tst);
		
		# Invertir la arista seleccionada, si fue solicitado
		if self.invert:
			self.G.opp_edge(self.mark, self.end);
			
			# Reiniciar marcas al terminar
			self.set_mark(-1);
			self.invert = False;
		
		# Obtener información de la arista seleccionada
		if not (self.mark == -1 or self.end == -1):
			e = self.G.get_edge(self.mark, self.end);
			if e == 0:	self.edge_on_G = False;
			else: self.edge_on_G = True;
		
		# Mover los vértices visuales que estén juntos
		for v in self.V:
			if not v.selected: v.separate(self.d, tst);
		
		# Contar los subgrafos en panel
		self.num_subs = len(subpanel.Sub);
		
		# Imprimir salida de funciones
		toolbar.out(self.out + self.print_log());
		
		# Redibujar
		self.draw(self.G);
	
	# Impresión de logs
	def print_log(self):
		msg = '\n';
		
		# Info. subgrafos
		msg += 'subgrafos en memoria: '+str(self.G.subgraphs);
		msg += '\n subgrafos en panel: '+str(self.num_subs);
		msg += '\n subgrafo actual: '+str(self.view_name);
		
		# Notificar si la función de subgrafos está activa
		if self.set_sub: msg += '\n Escoger vértices del nuevo subgrafo.';
		
		# Info. del vértice 1
		msg += '\n vértice 1: ';
		if not self.mark == -1: msg += str(self.mark);
		else: msg += '-';
		
		# Info. del vértice 2
		msg += '\n vértice 2: ';
		if not self.mark == -1: msg += str(self.end);
		else: msg += '-';
		
		# Info. de la arista
		msg += '\n arista: ';
		if not (self.mark == -1 or self.end == -1):
			msg += str(self.mark)+str(self.end);
			if self.edge_on_G:	msg += ' está en el grafo.';
			else:	msg += ' está en el complemento.';
			msg += '\n Otro clic para invertir la arista';
		else: msg += '-';
			
		return msg;
	
	# Valores iniciales del lienzo
	def init(self, G, subpanel, d, tst = False):
		
		# Establecer dibujo inicial
		self.set_graph(G, subpanel, tst);
		
		# Establecer el diámetro inicial de los vértices
		self.d = d;
		
		# Imprimir vértices a representar
		if tst:
			for v in self.V:
				print("Vértice visual agregado: "+str(v.id));
			print("Subgrafo: "+str(self.view_V));
	
	# Establecer el grafo a representar
	def set_graph(self, G, subpanel, tst = False):
	
		# Vaciar salida
		self.out = '';
	
		# Cambiar el grafo asociado
		self.G = G;
		
		# Imprimir grafo recibido
		if tst: 
			print("grafo a dibujar");
			self.G.print_ady();
		
		# Limpiar lienzo
		self.clear_widgets(self.children);
		
		# Vaciar lista de vértices visuales
		self.V = [];
		
		# Ver, por defecto, el grafo en su totalidad
		self.view_V = self.G.get_sub('self');
		self.view_name = 'self';
		
		# Reiniciar el panel de subgrafos
		subpanel.setup(self);
		
		# Agregar vértices visuales
		for v in range(self.G.vertices):
			u = VertexCanvas();
			u.set_id(v);
			self.V.append(u);
			self.add_widget(self.V[v]);
		
		# Recalcular posiciones en el lienzo
		self.recalc_vertexes_pos(tst);
	
	# Reiniciar posiciones de los vertices
	def recalc_vertexes_pos(self, tst = False):
	
		n = len(self.V); # Número de vértices visuales
		r = self.height / 3; # Radio del círculo en torno al que se ubican los vértices
		
		# Quitar marcas al reiniciar
		self.set_mark(-1);
		
		# Imprimir tamaño de lienzo al momento del cálculo
		if tst: print("Tamaño del lienzo usado para calcular los vértices= "+str(self.size));
		
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
	
	# Dibujar los vertices del subgrafo actual
	def draw_vertexes(self):
	
		# Si un vértice está listado en la vista actual, dibujarlo.
		for v in self.V:
			if o.contains(self.view_V, v.id): self.draw_vertex(v);

	# Dibujar un vertice
	def draw_vertex(self, v):
	
		# Dibujar el vértice con el lienzo de la clase padre
		with self.canvas:
			
			# Borde blanco
			Color(1, 1, 1, mode='rgb');
			Line(ellipse=(v.pos_x, v.pos_y, self.d, self.d));
			
			# Vértice del color del fondo, en condiciones normales
			if not v.selected: Color(.27, 0, .15, mode='rgb');	
			
			# Primer vértice marcado con color amarillo
			if self.mark == v.id: Color(1, 1, 0, mode='rgb');
			
			# Segundo vértice marcado con color magenta
			if self.end == v.id: Color(1, 0, 1, mode='rgb');
			
			# Vértice de subgrafo marcado con color cian
			if v.sub: Color(0, 1, 1, mode='rgb');
			
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
							
							# Dibujar una arista amarilla si es parte de un camino
							elif self.original and G.get_edge(u.id, v.id) == 2:
								Color(1, 1, 0, mode='rgb');
								self.draw_edge(v, u, r);

	# Dibujar una arista
	def draw_edge(self, v1, v2, r):
	
		# Reunir coordenadas y dibujar la línea
		x1 = v1.pos_x;
		y1 = v1.pos_y;
		x2 = v2.pos_x;
		y2 = v2.pos_y;
		Line(points=[r+x1 ,r+y1 ,r+x2 ,r+y2], width=1);
		
	# Manejo de marcas
	def set_mark(self, v):
		
		# No interferencia con la función de subgrafos
		if self.set_sub: return;
		
		# Quitar primera y segunda marcas
		if v == -1:
			self.mark = v;
			self.end = v;
			
		# Agregar primera marca si no hay ninguna
		elif self.mark == -1:
			self.mark = v;
			
		# Quitar marcas si se vuelve a escoger un vértice marcado
		elif self.mark == v:
			self.set_mark(-1);
		
		else:
		
			# Solicitar invertir arista si se vuelve a escoger el segundo vértice marcado
			if v == self.end:
				self.invert = True;
				return;
			
			# Marcar el segundo vértice
			self.end = v;
	
	# On/Off aristas del complemento
	def on_com_active(self, value):
		if value:
			self.complement = True;
		else:
			self.complement = False;
	
	# On/Off aristas del grafo
	def on_or_active(self, value):
		if value:
			self.original = True;
		else:
			self.original = False;
	
	# Encender y apagar función de subgrafos
	def subgraph(self):
		
		# Quitar marcas
		self.set_mark(-1);
		
		# Entrar o salir de la función
		self.set_sub = not self.set_sub;
		
		# Reiniciar vértices del subgrafo en construcción si entramos en la función
		if self.set_sub:
			self.V_sub = [];
			
		# Desmarcar vértices del subgrafo en construcción si salimos de la función
		else:
			for v in self.V:
				if v.sub: v.sub = False;
			
			# Vaciar salida
			self.out = '';
	
	# Confirmar subgrafo construido
	def subgraph_confirm(self, name, subpanel, tst = False):
	
		# Hacer que el grafo asociado almacene el subgrafo seleccionado
		sub_aux = self.V_sub;
		name_sub = self.G.add_sub(sub_aux, name); # Guardar el nombre con el que se guardó el subgrafo
		
		# Almacenar el nombre en el panel de subgrafos si corresponde a un nuevo subgrafo
		if self.G.subgraphs > len(subpanel.Sub):
			if tst: print("último nombre: "+str(name_sub));
			subpanel.add_sub(name_sub);
		
		# Actualizar el panel de subgrafos
		subpanel.reprint_subs(self);
		
		# Imprimir los subgrafos que hay almacenados en el grafo y los nombres en la lista
		if tst:
			print('nombres: '+str(subpanel.Sub));
			self.G.print_subs();
	
	# Selección automatica de vértices para construir un subgrafo
	def subgraph_vertices(self, V_sel):
		
		# Comprobar si los vértices solicitados existen
		if len(V_sel) > self.G.vertices: return;
		for v in V_sel:
			if v >= self.G.vertices: return;
		
		# Recorrer vértices y seleccionarlos, si no lo están
		for i in V_sel:
			self.V[i].subgraph(False);
	
	# Agregar subgrafos automaticamente
	def auto_add_subs(self, subs, names, panel):
	
		# Agregar cada subgrafo por la via común
		for i in range(len(subs)):
		
			# Activar la función
			self.subgraph();
			
			# Seleccionar los vértices del subgrafo
			self.subgraph_vertices(subs[i]);
			
			# Confirmar subgrafo con el nombre correspondiente
			self.subgraph_confirm(names[i], panel);
			
			# Desactivar función
			self.subgraph();
	
	# Intercambiar un par de etiquetas
	def lbl_change(self, lbls, tst = False):
	
		# Comprobar si los vértices solicitados existen
		if len(lbls) < 2: return;
		n = lbls[0];	# Vértice 1
		m = lbls[1];	# Vértice 2
		if n >= self.G.vertices or m >= self.G.vertices: return;
	
		# Imprimir la lista
		if tst: print(lbls);
	
		# Intercambiar las posiciones de los vértices recibidos
		x1 = self.V[n].pos_x;
		y1 = self.V[n].pos_y;
		x2 = self.V[m].pos_x;
		y2 = self.V[m].pos_y;
		self.V[m].pos_set(x1, y1);
		self.V[n].pos_set(x2, y2);
	
	# Cambiar todas las etiquetas
	def lbl_change_sev(self, vec):
	
		pos = [];	# Arreglo de posiciones actuales
		
		# Hacer el cambio respecto a las posiciones por defecto
		self.recalc_vertexes_pos();
		
		# Llenar el arreglo con la info. actual
		for v in self.V:
			pos.append([v.pos_x, v.pos_y]);
			
		# Permutar las posiciones
		for i in range(len(self.V)):
			self.V[vec[i]].pos_set(pos[i][0], pos[i][1]);
	
	# Algoritmo camino simple sobre la vista actual, desde el primer vértice
	def simple_path(self):
		
		Sub_G = self.G.get_subgraph(self.view_name); # Subgrafo seleccionado
		
		# Calcular un camino simple, desde el primer vértice.
		self.C.simple_path(Sub_G, 0);
		
		# Obtener resultados de la calculadora
		r1 = self.view_V[self.C.R1]; # Ruso 1
		r2 = self.view_V[self.C.R2]; # Ruso 2
		ue = self.C.res_sub(self.C.ue, self.view_V); # Vértices UE
		france = self.C.res_sub(self.C.france, self.view_V); # Vértices F
		peninsular = self.C.res_sub(self.C.peninsular, self.view_V); # F/P
		uk = self.C.res_sub(self.C.uk, self.view_V); # F/P/I
		included = [r2]+ue+[r1]+france+peninsular+uk; # Vista actual
		excluded = []; # Vértices que no pertenecen a la vista actual
		
		# Reunir los vértices que no pertenecen a la vista actual
		for v in self.V:
			if not o.contains(included, v.id): excluded.append(v.id);
		
		# Eliminar vértice ruso duplicado, si lo hay.
		if r1 == r2: 
			included.remove(r1);
		
		# Señalizar el camino
		self.G.mark_path([r2]+ue+[r1]);
		
		# Cambiar etiquetas del grafo según el camino encontrado
		self.lbl_change_sev(included+excluded);
		
		# Vaciar salida
		self.out = '';
		
		# Reportar resultados
		self.out += "Camino simple";
		self.out += "\n R1 = "+ str(r1);
		self.out += "\n R2 = "+ str(r2);
		self.out += "\n EU = "+ str(ue);
		self.out += "\n F = "+ str(france);
		self.out += "\n P/F = "+ str(peninsular);
		self.out += "\n I/P/F = "+ str(uk);
	
	# Algoritmo camino soble sobre la vista actual, que pase por el primer vértice
	def double_path(self, tst = False):
		
		Sub_G = self.G.get_subgraph(self.view_name); # Subgrafo seleccionado
		
		# Calcular un camino doble, que pase por el primer vértice.
		self.C.double_path(Sub_G, 0, tst);
		
		# Obtener resultados de la calculadora
		r1 = self.view_V[self.C.R1]; # Ruso 1
		r2 = self.view_V[self.C.R2]; # Ruso 2
		ue = self.C.res_sub(self.C.ue, self.view_V); # Vértices UE
		france = self.C.res_sub(self.C.france, self.view_V); # Vértices F
		peninsular = self.C.res_sub(self.C.peninsular, self.view_V); # F/P
		uk = self.C.res_sub(self.C.uk, self.view_V); # F/P/I
		included = [r2]+ue+[r1]+france+peninsular+uk; # Vista actual
		excluded = []; # Vértices que no pertenecen a la vista actual
		
		# Reunir los vértices que no pertenecen a la vista actual
		for v in self.V:
			if not o.contains(included, v.id): excluded.append(v.id);
		
		# Eliminar vértice ruso duplicado, si lo hay.
		if r1 == r2: 
			included.remove(r1);
		
		# Señalizar el camino
		self.G.mark_path([r2]+ue+[r1]);
		
		# Cambiar etiquetas del grafo según el camino encontrado
		self.lbl_change_sev(included+excluded);
		
		# Vaciar salida
		self.out = '';
		
		# Reportar resultados
		self.out += "Camino doble";
		self.out += "\n R1 = "+ str(r1);
		self.out += "\n R2 = "+ str(r2);
		self.out += "\n EU = "+ str(ue);
		self.out += "\n F = "+ str(france);
		self.out += "\n P/F = "+ str(peninsular);
		self.out += "\n I/P/F = "+ str(uk);
	
	# Calcular cliques y conjuntos independientes sobre el grafo actual
	def calc_cliq_ind(self, subpanel, tst = False):
		
		# Calcular cliques maximales del subgrafo
		self.C.bron_kerbosch_order(self.G);
		
		# Guardar conjuntos calculados
		cliq = self.C.found_cliques;
		
		# Calcular conjuntos independientes maximales del subgrafo
		Com = self.G.get_complement();
		self.C.bron_kerbosch_order(Com);
		
		# Guardar conjuntos calculados
		ind = self.C.found_cliques;
		
		# Preparar lista de nombres
		names = []; # Lista de nombres
		
		# Poner nombres a los cliques
		for sub in cliq:
			names.append("K"+str(len(sub))+": "+str(sub));
		
		# Poner nombres a los conjuntos independientes
		for sub in ind:
			names.append("Ind"+str(len(sub))+": "+str(sub));
		
		# Reiniciar el panel de subgrafos
		subpanel.setup(self);
		
		# Reiniciar vista
		subpanel.display_subgraph(self, 'self');
		
		# Almacenar cliques y conjuntos independientes
		self.auto_add_subs(cliq + ind, names, subpanel);
		
		# Ordenar subgrafos en el panel
		subpanel.sort_subs(self, True);
		
		# Vaciar salida
		self.out = '';
		
		# Imprimir número de subconjuntos calculados
		self.out = "Número de cliques e ind's: "+ str(len(cliq) + len(ind));
	
	# Calcular cliques sobre el grafo actual
	def calc_cliq(self, subpanel, tst = False):
		
		# Calcular cliques maximales del subgrafo
		self.C.bron_kerbosch_order(self.G);
		
		# Guardar conjuntos calculados
		cliq = self.C.found_cliques;
		
		# Preparar lista de nombres
		names = []; # Lista de nombres
		
		# Poner nombres a los cliques
		for sub in cliq:
			names.append("K"+str(len(sub))+": "+str(sub));
		
		# Reiniciar el panel de subgrafos
		subpanel.setup(self);
		
		# Reiniciar vista
		subpanel.display_subgraph(self, 'self');
		
		# Almacenar cliques
		self.auto_add_subs(cliq, names, subpanel);
		
		# Ordenar subgrafos en el panel
		subpanel.sort_subs(self, True);
		
		# Vaciar salida
		self.out = '';
		
		# Imprimir número de subconjuntos calculados
		self.out = "Número de cliques: "+ str(len(cliq));
	
	# Calcular caminos periféricos
	def periferia(self):
		
		# Indicar llamada a la función
		print('<Periferias>');
		
		# Imprimir caminos peninsulares/franco-españoles calculados
		self.C.pen_path(self.G, True);

# Barra de herramientas
class Toolbar(GridLayout):

	wid_height = 20; # Altura de los botones

	txt_in = TextInput(multiline=False, size_hint_x=None, width=100, size_hint_y=None, height=wid_height+10, hint_text='Ex. etiquetas', text_validate_unfocus=False, font_size=10); # Entrada de texto

	txt_out = TextInput(multiline=True, size_hint_x=None, width=100, background_color=(.3,.3,.3), hint_text='Salida', readonly=True, font_size=10); # Salida de funciones
	
	# Imprimir salida
	def out(self, out):
		
		# Imprimirla en el widget hijo
		self.txt_out.text = out;
		
		# Enviar el cursor al inicio
		self.txt_out.cursor = (0,0);
		
	# Vaciar un campo de texto
	def void_text(self, txt):
		txt.text = '';

	# Solicitar al dibujante crear un subgrafo
	def subgraph_definition(self, GC, subpanel, value, btn_sub, check_sub, btn_ran, btn_path, btn_path_2, btn_cliq, btn_cliq_ind, btn_per, txt_in, confirm, tst = False):
	
		# Imprimir un separador para monitorizar las acciones del botón y el checkbox
		if tst: print("------.");
		
		if not confirm:
		
			# Solicitar al dibujante crear el subgrafo
			if check_sub.active:
				if tst:
					print("he sido llamado por el checkbox, que está activo.");
					print("abrir la puerta.");
				GC.subgraph();
			
			# Solicitar al dibujante volver al estado normal
			else:
				if tst: 
					print("he sido llamado por el checkbox, que está inactivo.");
					print("cerrar la puerta.");
				GC.subgraph();
		else:
		
			# Solicitar al dibujante confirmar el subgrafo creado
			if not btn_sub.disabled:
				if tst: 
					print("he sido llamado por el botón, que está activo.");
					print("Es un invitado, dejarlo pasar.");
				GC.subgraph_confirm(None, subpanel, tst);
			else:
				if tst: 
					print("he sido llamado por el botón, que está inactivo.");
					print("Es un invitado, insultarlo.");
		
		# Manipular la barra según se entre/salga de la función de subgrafos
		self.subgraph_buttons(GC, value, btn_sub, check_sub, btn_ran, btn_path, btn_path_2, btn_cliq, btn_cliq_ind, btn_per, txt_in, tst);

	# Mostrar/Ocultar herramientas
	def subgraph_buttons(self, GC, value, btn_sub, check_sub, btn_ran, btn_path, btn_path_2, btn_cliq, btn_cliq_ind, btn_per, txt_in, tst = False):
		
		# Activar/Desactivar botones de otras funciones
		btn_ran.disabled = value;
		btn_path.disabled = value;
		btn_path_2.disabled = value;
		btn_cliq.disabled = value;
		btn_cliq_ind.disabled = value;
		btn_per.disabled = value;
		
		# Cambiar proósito de la entrada de texto
		if value: txt_in.hint_text = 'Sel. subgrafo';
		else: txt_in.hint_text = 'Ex. etiquetas';
		
		# Activar/Desactivar checkbox
		check_sub.active = value;
		
		# Comprobación de por qué no se gatillan solicitudes indeseadas al dibujante
		if btn_sub.disabled: 
			if tst: print("El botón está deshabilitado.");
		else: 
			if tst: print("El botón está habilitado.");
		if value: 
			if tst: print("Lo habilitaré.");
		else: 
			if tst: print("Lo deshabilitaré.");
		
		# Activar/Desactivar botón de confirmación
		btn_sub.disabled = not value;

	# Aplicar función a la entrada de texto
	def input_manage(self, GC, txt_field, hint_text):
		
		l_n = []; # lista para almacenar la entrada numérica
		
		# Recibir entrada y vaciar el campo de texto
		input = txt_field.text;
		self.void_text(txt_field);
		
		# Convertir entrada en una lista
		l = list(input.rsplit(','));
		
		# Descartar la entrada si hay un número negativo
		for n in l:
			if not n.isnumeric() or int(n) < 0: return;
			else: l_n.append(int(n));
		
		# Aplicar la función que corresponda a la situación
		if hint_text == 'Ex. etiquetas':
		
			# Cambiar etiquetas de los 2 primeros números introducidos
			GC.lbl_change(l_n[0:2]);
		
		# Seleccionar vértices del vector introducido
		elif hint_text == 'Sel. subgrafo':
			GC.subgraph_vertices(l_n);
	
	# Generar nuevo grafo random para el dibujante de grafos
	def new_random(self, GC, subpanel, tst = False):
		
		# Crear un nuevo grafo del mismo número de vértices y hacer aleatorias sus aristas
		G = Graph();
		G.insert_Vertexes(len(GC.V));
		G.rand_edges(.2);
		
		# Pasárselo al dibujante
		GC.set_graph(G, subpanel, tst);

	# Vincular la barra a un dibujante
	def setup(self, GC, subpanel, tst = False):
		
		# Limpiar lienzo
		self.clear_widgets(self.children);
		
		# Disposición
		self.orientation = "rl-tb";
		self.size_hint_x = None;
		self.width = 100;
		self.rows = 16;
		self.cols = 1;
		
		# Botón para generar nuevo grafo random
		btn_ran = Button(font_size='10',text='Random', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_ran.bind(on_press=lambda x:self.new_random(GC, subpanel, tst));
		self.add_widget(btn_ran);
		
		# Checkbox: aristas del grafo original
		lbl_or = Label(font_size='10', text='Grafo', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		checkbox_o = CheckBox(size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100, active=True, color=(255,0,0));
		checkbox_o.bind(active=lambda x,y:GC.on_or_active(checkbox_o.active));
		self.add_widget(lbl_or);
		self.add_widget(checkbox_o);
		
		# Checkbox: aristas del grafo complemento
		lbl_com = Label(font_size='10', text='Complemento', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		checkbox_c = CheckBox(size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100, active=False, color=(0,0,255));
		checkbox_c.bind(active=lambda x,y:GC.on_com_active(checkbox_c.active));
		self.add_widget(lbl_com);
		self.add_widget(checkbox_c);
		
		# Botón Camino simple
		btn_path = Button(font_size='10', text='Camino simple', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_path.bind(on_press=lambda x:GC.simple_path());
		self.add_widget(btn_path);
		
		# Botón Camino doble
		btn_path_2 = Button(font_size='10', text='Camino doble', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_path_2.bind(on_press=lambda x:GC.double_path());
		self.add_widget(btn_path_2);
		
		# Botón de calcular cliques
		btn_cliq = Button(font_size='10', text="Cliques", size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_cliq.bind(on_press=lambda x:GC.calc_cliq(subpanel, tst));
		self.add_widget(btn_cliq);
		
		# Botón de calcular cliques y conjuntos independientes
		btn_cliq_ind = Button(font_size='10', text="Cliques e Ind's", size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_cliq_ind.bind(on_press=lambda x:GC.calc_cliq_ind(subpanel, tst));
		self.add_widget(btn_cliq_ind);
		
		# Botón de cálculo de caminos periféricos
		btn_per = Button(font_size='10',text='Periferia', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_per.bind(on_press=lambda x:GC.periferia());
		self.add_widget(btn_per);
		
		# Botón de reinicio de posiciones
		btn_res = Button(font_size='10',text='Reiniciar pos.', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_res.bind(on_press=lambda x:GC.recalc_vertexes_pos());
		self.add_widget(btn_res);
		
		# Kit de creación de subgrafos
		lbl_sub = Label(font_size='10', text='Definir subgrafo', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100);
		btn_sub = Button(font_size='10', text='Confirm. subgrafo', size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100, disabled=True);
		checkbox_sub = CheckBox(size_hint_y=None, height=self.wid_height, size_hint_x=None, width=100, active=False, color=(0,1,1));
		btn_sub.bind(on_press=lambda x:self.subgraph_definition(GC, subpanel, False, btn_sub, checkbox_sub, btn_ran, btn_path, btn_path_2, btn_cliq, btn_cliq_ind, btn_per, self.txt_in, True));
		checkbox_sub.bind(active=lambda x,y:self.subgraph_definition(GC, subpanel, checkbox_sub.active, btn_sub, checkbox_sub, btn_ran, btn_path, btn_path_2, btn_cliq, btn_cliq_ind, btn_per, self.txt_in, False));
		self.add_widget(lbl_sub);
		self.add_widget(checkbox_sub);
		
		# Campo de texto (entrada)
		self.txt_in.bind(on_double_tap=lambda x:self.void_text(self.txt_in));
		self.txt_in.bind(on_text_validate=lambda x:self.input_manage(GC, self.txt_in, self.txt_in.hint_text));
		self.add_widget(self.txt_in);
		self.add_widget(btn_sub);
		
		# Campo de texto (salida)
		self.txt_out.bind(on_double_tap=lambda x:self.void_text(self.txt_out));
		self.add_widget(self.txt_out);

# Panel de subgrafos
class SubPanel(GridLayout):
	
	Sub = []; # Lista de nombres de los subgrafos almacenados
	GC = None; # Dibujante asociado
	up_btn = Button(font_size='10', text='/|', size_hint_y=None, height=30, size_hint_x=None, width=30); # Botón up
	dwn_btn = Button(font_size='10', text='|/', size_hint_y=None, height=30, size_hint_x=None, width=30); # Botón down
	first_sub_to_show = NumericProperty(0);	# Primer subgrafo visible
	current = 0; # Grafo a visualizar
	holding = 0; # Bandera indicadora de si los botones arriba o abajo están sostenidos

	# Valores iniciales
	def setup(self, GC, tst = False):
		
		# Dibujante asociado
		self.GC = GC;
		
		# Permitir, a lo sumo, 18 subgrafos en el panel más 2 botones: arriba y abajo.
		self.cols = 1;
		self.rows = 20;
		self.orientation = "rl-tb";
		self.size_hint_x = None;
		self.width = 100;
		
		# Vaciar lista de nombres
		self.Sub = [];
		
		# Ir al inicio del panel
		self.first_sub_to_show = 0;
		
		# Agregar funcionalidad de los botones arriba y abajo.
		self.up_btn.bind(on_press=lambda x:self.holding_manage(True, tst));
		self.dwn_btn.bind(on_press=lambda x:self.holding_manage(False, tst));
		
		# Agregar el subgrafo por defecto
		self.add_sub('self');
		
		# Actualizar el contenido del panel periódicamente
		Clock.schedule_interval(lambda x:self.update(GC), 1.0 / 60.0);
		
		# Pintar botones
		self.reprint_subs(GC);
	
	# Actualizar panel
	def update(self, GC, tst = False):
		
		# Si el primer elemento a mostrar en el panel ha cambiado, re-imprimir los botones
		n = len(self.children); # Número de botones
		if n < 3: return;
		first = self.children[n-2].text; # primer subgrafo a mostrar en el panel
		shown = self.Sub[ int(self.first_sub_to_show) ]; # Primer elemento de la lista
		if not first == shown: self.reprint_subs(GC);
		
		# Holding de los botones/arriba abajo, por alguna razón, no se previene con on_press
		if tst and self.holding > 0: print("holding");
	
	# Visualizar subgrafo por acción del teclado
	def set_current(self, GC, n):
		
		# Cambiar el subgrafo a dibujar si es posible
		new_pos = self.current + n; # Posición destino
		if new_pos >= 0 and new_pos < len(self.Sub):
			self.current = new_pos;
		else: return;
		
		# Pasar la vista al dibujante
		self.display_subgraph(GC, self.Sub[self.current]);
	
	# Función para ignorar la duplicidad de arriba/abajo por holding
	def holding_manage(self, up, tst = False):
	
		# Holding 1: botón arriba, Holding 2: botón abajo
		if up: self.holding = 1;
		else: self.holding = 2;
	
	# Lanzar la función arriba/abajo según corresponda al soltar el clic
	def on_touch_up (self, touch):
	
		# Guardar valor del holding y usarlo para lanzar la función adecuada
		direction = self.holding;
		self.holding = 0;
		if direction == 1: self.go_up();
		elif direction == 2: self.go_down();
	
	# Función del botón arriba
	def go_up(self, tst = False):
	
		# Notificar llamada a la función
		if tst: 
			print("up");
	
		# Cambiar grafo visible
		self.set_current(self.GC, -1);
	
		# Retroceder un paso en la lista si aún no se ha llegado al inicio
		if self.first_sub_to_show == 0: return;
		else: 
			self.move_panel(-1, tst);

	# Función del botón abajo
	def go_down(self, tst = False):
		
		# Notificar llamada a la función
		if tst: 
			print("down");
		
		# Cambiar grafo visible
		self.set_current(self.GC, 1);
		
		# No hace nada si aún no hay suficientes botones almacenados
		if len(self.Sub) <= 18: return;
		
		# Avanzar un paso en la lista si aún no se ha llegado al final
		if self.first_sub_to_show == len(self.Sub) - 18: return;
		else: 
			self.move_panel(1, tst);

	# Avanzar/retroceder en la lista
	def move_panel(self, n, tst = False):
		
		# Notificar llamada a la función, puede no verse cronológicamente bien en consola
		if tst: print("moving...");
		
		# Modificar el primer elemento de la lista a ser mostrado
		self.first_sub_to_show += n;
		
		# Notificar suma
		if tst: print(self.first_sub_to_show);

	# Agregar subgrafo
	def add_sub(self, name):
	
		# Agregar el nombre del nuevo subgrafo a la lista
		self.Sub.append(name);

	# Imprimir los botones que alcancen en el panel
	def reprint_subs(self, GC):
	
		add_num = len(self.Sub) # Número de botones por agregar
		
		# limpiar botones, menos el botón arriba
		self.clear_widgets(self.children);
		self.add_widget(self.up_btn);
		
		# Si los subgrafos no caben en el panel, mostrar solo 18
		if add_num > 18: add_num = 18;
		
		# Agregar botones recursivamente
		self.add_button(0, add_num, GC);
		
		# Pintar, de último, el botón abajo
		self.add_widget(self.dwn_btn);

	# Agregar botones (recursivo). Por alguna razón, con un for no funciona.
	def add_button(self, i, b, GC):
	
		# Terminar si el índice llega hasta b (b botones)
		if i == b: return;
		
		idx = int(self.first_sub_to_show);	# Primer elemento de la lista
		
		sub_name = self.Sub[idx+i]; # Nombre del subgrafo
		
		# Crear botón, agregarle la funcionalidad y mostrarlo
		aux_btn = Button(font_size='10', text=sub_name[0:10], size_hint_y=None, height=30, size_hint_x=None, width=100);
		aux_btn.bind(on_press=lambda x:self.display_subgraph(GC, sub_name));
		self.add_widget(aux_btn);
		
		# Pasar al siguiente botón
		self.add_button(i+1, b, GC);

	# Pintar el subgrafo seleccionado en el lienzo
	def display_subgraph(self, GC, name):
	
		arr_sub = GC.G.get_sub(name); # Vértices del subgrafo seleccionado
		
		# Imponer el subgrafo al dibujante
		GC.view_V = arr_sub;
		GC.view_name = name;
	
	# Ordenar n subgrafos según el número de vértices
	def sort_subs(self, GC, max_min, tst = False):
		
		n = len(self.Sub); # Número de subgrafos
		sorted = []; # Conjunto re-ordenado
		k = 0;	# Tamaño del conjunto V
		
		# Repetir proceso hasta que el tamaño del conjunto re-ordenado sea n
		while(not len(sorted) == n):
			
			arr_aux = [];	# Subgrafos cuyo conjunto V es de tamaño k
			
			# Reunir todos los subgrafos de k vértices
			for name in self.Sub:
				sub = GC.G.get_sub(name);	# Conjunto V
				if len(sub) == k: arr_aux.append(name);
				
			# Ordenar de mayor a menor
			if max_min:
				sorted = arr_aux + sorted;
				
			# Ordenar de menor a mayor
			else: 
				sorted = sorted + arr_aux;
			
			# Seguir con k+1 vértices
			k += 1;
		
		# Imprimir orden antiguo y nuevo
		if tst:	
			print("------------------------------");
			print("old: "+str(self.Sub));
			print("sorted: "+str(sorted));
		
		# Asignar el nuevo orden a la lista
		self.Sub = sorted;
		
		# Ir al inicio de la lista de botones
		self.first_sub_to_show = 0;
		
		# Actuaizar panel con botones organizados
		self.reprint_subs(GC);

# Gestor del teclado
class MyKeyboardListener(Widget):

	subpanel = None;
	GC = None;
	toolbar = None;

	def __init__(self, GC, toolbar, subpanel, **kwargs):
		super(MyKeyboardListener, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
		self._keyboard_closed, self, 'text');
		
		# No afectar el contenido de la pantalla
		self.size_hint_x = None;
		self.width = 0;
		self.size_hint_y = None;
		self.height = 0;
		
		# Vincular el dibujante
		self.GC = GC;
		
		# Vincular al panel de subgrafos
		self.subpanel = subpanel;
		
		# Vincular al panel de subgrafos
		self.toolbar = toolbar;
		
		if self._keyboard.widget:
			
			# If it exists, this widget is a VKeyboard object which,!you can use to change the keyboard layout.
			pass
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

	# Trabajar con un grafo proveniente del portapapeles
	def paste_graph_to_work_on(self):
		
		# Vaciar salida
		self.toolbar.txt_in.text = '';
		
		# Copiar el grafo del portapapeles
		self.toolbar.txt_in.paste();
		
		# Convertir en lista sin espacios
		l = list(self.toolbar.txt_in.text.rsplit(' '));
		
		# Crear un grafo nuevo
		G = Graph();
		
		# Insetar los mismo vértices que el vértice actual
		G.insert_Vertexes(self.GC.G.vertices);
		
		# Insertar aristas
		for u in range(G.vertices):
			for v in range(G.vertices):
				src = l.pop(0);	# Fuente de la uv-ésima arista
				e = ''; #uv-ésima arista
				
				# Obtener el valor numérico de la cadena de texto
				for c in src:
					if c.isnumeric(): e += c;
				G.edge(u,v,int(e));
		
		# Enviárselo al dibujante
		self.GC.set_graph(G, self.subpanel);
		
		# Vaciar salida, de nuevo
		self.toolbar.txt_in.text = '';

	def _keyboard_closed(self):
	
		# Notificar el cese de actividad
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
	
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
	
		'''
		print('The key', keycode, 'have been pressed')
		print(' - text is %r' % text)
		print(' - modifiers are %r' % modifiers)
		'''
		
		# El keycode es int+str. Si se presiona escape, el gestor del teclado se apaga.
		if keycode[1] == 'escape':
			keyboard.release();
		
		# Ordenar bajar al panel si se presiona abajo
		if keycode[1] == 'down':
			self.subpanel.go_down();
		
		# Ordenar subir al panel si se presiona arriba
		if keycode[1] == 'up':
			self.subpanel.go_up();
		
		# Copiar la salida al clipboard al preisonar c
		if keycode[1] == 'c':
			print('out');
			self.toolbar.txt_out.copy(self.toolbar.txt_out.text);
		
		# Copiar el grafo trabajado al portapapeles al preisonar g
		if keycode[1] == 'g':
			print('graph copy');
			self.toolbar.txt_out.text = str(self.GC.G.E.data);
			self.toolbar.txt_out.copy(self.toolbar.txt_out.text);
		
		# Copiar el grafo del portapapeles al preisonar p
		if keycode[1] == 'p':
			print('graph paste');
			self.paste_graph_to_work_on();
			
		return True;

# Aplicacion gráfica
class GraphApp(App):
	
	# Montaje de la app
	def build(self):
		
		# Testeo
		tst = False;
		
		# Preparar grafo inicial
		G = Graph();
		G.insert_Vertexes(28);
		
		# Widget raíz
		root = GridLayout();
		root.cols = 3;
		
		# Lienzo del grafo
		graph_canvas = GraphCanvas();
		
		# Panel de subgrafos
		subpanel = SubPanel();
		subpanel.setup(graph_canvas);
		
		# Barra de herramientas
		toolbar = Toolbar();
		toolbar.setup(graph_canvas, subpanel);
		
		# Gestor del teclado
		key_mng = MyKeyboardListener(graph_canvas, toolbar, subpanel);
		
		# Contenido de las 3 columnas (lienzo, barra y panel)
		root.add_widget(graph_canvas);
		root.add_widget(toolbar);
		root.add_widget(subpanel);
		root.add_widget(key_mng);
		
		# Actualizar el contenido del lienzo con el grafo de la aplicación
		Clock.schedule_interval(lambda x:graph_canvas.update(toolbar, subpanel, tst, G), 1.0 / 60.0);
		
		return root;

if __name__ == '__main__':
    GraphApp().run();