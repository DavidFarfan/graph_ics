import sys

def progress(count, total, status=''): # barra de progreso, licencia MIT
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def primes_n(n): # primos hasta n
	ret = [];
	for i in range(n):
		if(i==1):
			continue;
		for j in range(i):
			if(i>2 and (j>1 and j<i) and i%j==0):
				#print(str(i) + "/" + str(j));
				break;
			if(j==i-1):
				ret.append(i);
	print(ret);
	return ret;

class ExMatrix: # Matriz expansible

	data = None;    # Arreglo filas
	rows = None;
	columns = None;
	
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

class CombinManager:  # Clase contenedora de calculos combinacionales

	matrix_sec_n_m = None;    # matriz memoria de comb. lineales naturales de n sumandos y m pasos
	matrix_sec_n_m_neg = None;  # matriz memoria de comb. lineales enteras de n sumandos y n pasos

	def __init__(self):
		self.matrix_sec_n_m = ExMatrix();
		self.matrix_sec_n_m_neg = ExMatrix();
	
	def pos_labels_bruta(self, n): # Posibles formas de etiquetar grafo de n vertices
		if(n==1):
			return [[1]];
		else:
			aux = [];
			prev = self.pos_labels_bruta(n-1);
			for i in range(n):
				for j in range(len(prev)):
					#print(str(prev[j][0:i])+" + ["+str(n)+"] + "+str(prev[j][i:n]));
					aux.append(prev[j][0:i]+ [n] + prev[j][i:n]);
			#print(aux);
			return aux;
	
	def print_memory(self, neg): # imprimir matriz natural/entera de secuencias combinacionales
		if(neg):
			self.matrix_sec_n_m_neg.print_matrix();
		else:
			self.matrix_sec_n_m.print_matrix();

	def sec_n_m(self, n, m, neg): #  Combin. lineales enteras/naturales de n sumandos y m pasos sin recalculo
	
		# Primera comprobacion en memoria
		if(neg):
			if(len(self.matrix_sec_n_m_neg.data)>n):
				if(len(self.matrix_sec_n_m_neg.data[n])>m):
					if(not self.matrix_sec_n_m_neg.data[n][m]==[]):
						#print("("+str(n)+","+str(m)+") Ya existe en memoria");
						return self.matrix_sec_n_m_neg.data[n][m];
					#else:
						#print("("+str(n)+","+str(m)+") está vacío, hay que calcularlo recursivamente.");
				#else:
					#print("la matriz de comb. enteras no alcanza las "+str(m)+" columnas, no está ("+str(n)+","+str(m)+")");
			#else:
				#print("la matriz de comb. enteras no alcanza las "+str(n)+" filas, no está ("+str(n)+","+str(m)+")");
		else:
			if(len(self.matrix_sec_n_m.data)>n):
				if(len(self.matrix_sec_n_m.data[n])>m):
					if(not self.matrix_sec_n_m.data[n][m]==[]):
						#print("("+str(n)+","+str(m)+") Ya existe en memoria");
						return self.matrix_sec_n_m.data[n][m];
					#else:
						#print("("+str(n)+","+str(m)+") está vacío, hay que calcularlo recursivamente.");
				#else:
					#print("la matriz de comb. enteras no alcanza las "+str(m)+" columnas, no está ("+str(n)+","+str(m)+")");
			#else:
				#print("la matriz de comb. enteras no alcanza las "+str(n)+" filas, no está ("+str(n)+","+str(m)+")");
		
		# Calcular si no se encuentra en memoria
		#print("----------");
		#self.print_matrix(False);
		if(n==1):
			if(m==0):
				aux = [[0]];
				self.matrix_sec_n_m_neg.intro(aux,1,0);
				self.matrix_sec_n_m.intro(aux,1,0);
				#print("!!!:"+str([[0]])+" added to memory spot ("+str(n)+","+str(m)+")");
				return aux; 
			else:
				if(neg):
					aux = [[-m], [m]];
					self.matrix_sec_n_m_neg.intro(aux,1,m);
					#print("!!!:"+str([[-m], [m]])+" added to memory spot ("+str(n)+","+str(m)+")");
					return aux;
				else:
					aux = [[m]];
					self.matrix_sec_n_m.intro(aux,1,m);
					#print("!!!:"+str([[m]])+" added to memory spot ("+str(n)+","+str(m)+")");
					return aux;
		else:
			if(m==0):
				aux = [[0]*n];
				self.matrix_sec_n_m_neg.intro(aux,n,0);
				self.matrix_sec_n_m.intro(aux,n,0);
				#print("!!!:"+str([[0]*n])+" added to memory spot ("+str(n)+","+str(m)+")");
				return aux;
			else:
				self.matrix_sec_n_m_neg.expand_matrix(n,m);
				self.matrix_sec_n_m.expand_matrix(n,m);
				ret = [];
				if(neg):
					for i in range(2*m+1):
						id = i-m;
						#print("Memory = "+str(self.matrix_sec_n_m_neg[n-1][m-abs(id)])+" on spot ("+str(n-1)+","+str(m-abs(id))+") requested by ("+str(n)+","+str(m)+")");
						aux = None;
						if(self.matrix_sec_n_m_neg.data[n-1][m-abs(id)]==[]):
							#print("lack of value, it needs to be computed");
							aux = self.sec_n_m(n-1, m-abs(id), True);
							#print("Computed Aux = "+str(aux));
						else:
							#print("avalueble on memory");
							aux = self.matrix_sec_n_m_neg.data[n-1][m-abs(id)];
						for j in range(len(aux)):
							#print(str([id]) + " + " + str(aux[j]) + " = " + str([id]+aux[j]));
							ret.append([id]+aux[j]);
							#print("acc-->"+str(ret));
					self.matrix_sec_n_m_neg.intro(ret,n,m);
					#print("!!!:"+str(ret)+" added to memory spot ("+str(n)+","+str(m)+")");
				else:
					for i in range(m+1):
						#print("Memory= "+str(self.matrix_sec_n_m[n-1][m-i])+" on spot ("+str(n-1)+","+str(m-i)+") requested by ("+str(n)+","+str(m)+")");
						aux = None;
						if(self.matrix_sec_n_m.data[n-1][m-i]==[]):
							#print("lack of value, it needs to be computed");
							aux = self.sec_n_m(n-1, m-i, False);
							#print("Computed Aux = "+str(aux));
						else:
							#print("avalueble on memory");
							aux = self.matrix_sec_n_m.data[n-1][m-i];
						for j in range(len(aux)):
							#print(str([i]) + " + " + str(aux[j]) + " = " + str([i]+aux[j]));
							ret.append([i]+aux[j]);
							#print("acc-->"+str(ret));
					self.matrix_sec_n_m.intro(ret,n,m);
					#print("!!!:"+str(ret)+" added to memory spot ("+str(n)+","+str(m)+")");
				#print("tam= "+str(len(ret)));
				return ret;

	def recalc_sec_n_m(self, n, m, neg): #  Combin. lineales enteras/naturales de n sumandos y m pasos con recalculo
		if(n==1):
			if(m==0):
				return [[0]];
			else:
				if(neg):
					return [[-m], [m]];
				else:
					return [[m]];
		else:
			if(m==0):
				return [[0]*n];
			else:
				ret = [];
				if(neg):
					for i in range(2*m+1):
						id = i-m;
						aux = self.recalc_sec_n_m(n-1, m-abs(id), True);
						for j in range(len(aux)):
							#print(str([id]) + " + " + str(aux[j]) + " = " + str([id]+aux[j]));
							ret.append([id]+aux[j]);
							#print("acc-->"+str(ret));
				else:
					for i in range(m+1):
						aux = self.recalc_sec_n_m(n-1, m-i, False);
						for j in range(len(aux)):
							#print(str([i]) + " + " + str(aux[j]) + " = " + str([i]+aux[j]));
							ret.append([i]+aux[j]);
							#print("acc-->"+str(ret));
				#print("tam= "+str(len(ret)));
				return ret;
	
	def pos_n_joins_m_grafo(self, n, m):  # Posibilidades para los n-ciclos del Km,  n<=m sin recalculo
		pos = self.sec_n_m(n+1, m-n, False);
		ret = [];
		for i in range(len(pos)):
			aux = [];
			for j in range(n+1):
				aux += [0]*pos[i][j];
				if(j<n):
					aux += [1];
			ret.append(aux);
		return ret;
	
	def recalc_pos_n_joins_m_grafo(self, n, m):  # Posibilidades para los n-ciclos del Km,  n<=m con recalculo
		pos = self.recalc_sec_n_m(n+1, m-n, False);
		ret = [];
		for i in range(len(pos)):
			aux = [];
			for j in range(n+1):
				aux += [0]*pos[i][j];
				if(j<n):
					aux += [1];
			ret.append(aux);
		return ret;
	
	def	n_joins_m_grafo(self, n, m):   # Posibles n-ciclos del Km,  n<=m sin recalculo
	
		# Calculo de ciclos contribuyentes
		pos = self.pos_n_joins_m_grafo(n, m);
		#print("pos = " + str(pos_n_joins_m_grafo(n, m)));
		ones = [];
		for i in range(len(pos)):
			aux = [];
			for j in range(m):
				if(pos[i][j]==1):
					aux += [j+1];
			ones.append(aux);
		#print("ones = " + str(ones));
		
		# Para omitir el calculo de #paso triviales
		if(n>1):
			unit = self.n_joins_m_grafo(1, m);
			#print("ciclos unitarios = " + str(unit));
			for i in range(len(pos)):
				for j in range(m):
					if(not pos[i][j]==1):
						pos[i][j] = m+1;
						for k in range(n):
							tam = unit[ones[i][k]-1][j];
							if(tam < pos[i][j]):
								pos[i][j] = tam;
							#print("i,j = " + str(i+1) + ", " + str(j+1) + " --> " + str(unit[ones[i][k]-1]) + " --> " + str(unit[ones[i][k]-1][j]) + " --> " + str(pos[i][j]));
		else:
			for i in range(len(pos)):
				for j in range(m):
					if(pos[i][j]==0):
						pos[i][j]=3;
			#print("unitarios sin corregir = " + str(pos));
		
		# Calculo de otros caminos
		for i in range(len(pos)):
			#print(str(int(i/len(pos)*100))+"% in K" + str(2*m+1));
			progress(i, len(pos), "% in K" + str(2*m+1));
			for j in range(m):
				combs = [];
				steps = 2;
				congruent = False;
				if(pos[i][j]>2):
					#print("j = "+str(j));
					#print("i,j = "+str(i)+","+str(j) + " de " +str(pos[i][j]));
					while(not congruent):
						combs = self.sec_n_m(n, steps, True);
						#print("combs = " + str(combs));
						for k in range(len(combs)):
							terminal = 0;
							for l in range(n):
								terminal += combs[k][l]*ones[i][l];
								#print(str(combs[k][l]) + "*" + str(ones[i][l]) + "=" + str(combs[k][l]*ones[i][l]));
							if((terminal%(2*m+1) == j+1) or (terminal%(2*m+1) == 2*m-j)):
								#print("comb = "+ str(combs[k]) + ", ones = " + str(ones[i]));
								#print(str(terminal) + " (mod) " + str(2*m+1) + " = " + str(terminal%(2*m+1)) + " = " + str(j+1) + " o = " + str(2*m-j));
								pos[i][j] = steps;
								congruent = True;
								break;
						steps += 1;
		#print(str(n)+"-ciclos en K"+ str(2*m+1)+ " = " + str(pos));
		return pos;
	
	def	recalc_n_joins_m_grafo(self, n, m):   # Posibles n-ciclos del Km,  n<=m con recalculo
	
		# Calculo de ciclos contribuyentes
		pos = self.recalc_pos_n_joins_m_grafo(n, m);
		#print("pos = " + str(pos_n_joins_m_grafo(n, m)));
		ones = [];
		for i in range(len(pos)):
			aux = [];
			for j in range(m):
				if(pos[i][j]==1):
					aux += [j+1];
			ones.append(aux);
		#print("ones = " + str(ones));
		
		# Para omitir el calculo de #paso triviales
		if(n>1):
			unit = self.recalc_n_joins_m_grafo(1, m);
			#print("ciclos unitarios = " + str(unit));
			for i in range(len(pos)):
				for j in range(m):
					if(not pos[i][j]==1):
						pos[i][j] = m+1;
						for k in range(n):
							tam = unit[ones[i][k]-1][j];
							if(tam < pos[i][j]):
								pos[i][j] = tam;
							#print("i,j = " + str(i+1) + ", " + str(j+1) + " --> " + str(unit[ones[i][k]-1]) + " --> " + str(unit[ones[i][k]-1][j]) + " --> " + str(pos[i][j]));
		else:
			for i in range(len(pos)):
				for j in range(m):
					if(pos[i][j]==0):
						pos[i][j]=3;
			#print("unitarios sin corregir = " + str(pos));
		
		# Calculo de otros caminos
		for i in range(len(pos)):
			#print(str(int(i/len(pos)*100))+"% in K" + str(2*m+1));
			progress(i, len(pos), "% in K" + str(2*m+1));
			for j in range(m):
				combs = [];
				steps = 2;
				congruent = False;
				if(pos[i][j]>2):
					#print("j = "+str(j));
					#print("i,j = "+str(i)+","+str(j) + " de " +str(pos[i][j]));
					while(not congruent):
						combs = self.recalc_sec_n_m(n, steps, True);
						#print("combs = " + str(combs));
						for k in range(len(combs)):
							terminal = 0;
							for l in range(n):
								terminal += combs[k][l]*ones[i][l];
								#print(str(combs[k][l]) + "*" + str(ones[i][l]) + "=" + str(combs[k][l]*ones[i][l]));
							if((terminal%(2*m+1) == j+1) or (terminal%(2*m+1) == 2*m-j)):
								#print("comb = "+ str(combs[k]) + ", ones = " + str(ones[i]));
								#print(str(terminal) + " (mod) " + str(2*m+1) + " = " + str(terminal%(2*m+1)) + " = " + str(j+1) + " o = " + str(2*m-j));
								pos[i][j] = steps;
								congruent = True;
								break;
						steps += 1;
		#print(str(n)+"-ciclos en K"+ str(2*m+1)+ " = " + str(pos));
		return pos;

def iso_grafos_bruta():
	g1 = ExMatrix();
	g2 = ExMatrix();
	
	print("numero de vertices: ");
	n = int(input());
	
	print("introducir grafo 1: ");
	print("1: arista presente");
	print("0: arista ausente");
	for i in range(n):
		for j in range(n):
			if(i>j):
				print("arista ("+str(i)+", "+str(j)+"):");
				g1.intro(int(input()), i, j);
	g1.mirror();
	g1.print_matrix();
	
	print("introducir grafo 2: ");
	print("1: arista presente");
	print("0: arista ausente");
	for i in range(n):
		for j in range(n):
			if(i>j):
				print("arista ("+str(i)+", "+str(j)+"):");
				g2.intro(int(input()), i, j);
	g2.mirror();
	g2.print_matrix();
	
	labl = CombinManager().pos_labels_bruta(g1.rows-1);
	count = 0;
	
	for l in labl:
		count += 1;
		progress(count, len(labl), "");
		search = True;
		for i in range(g1.rows-1):
			for j in range(g1.rows-1):
				#print(str(i)+", "+str(j));
				#print("labels: "+str(l)+ ", search more on label config. = "+str(search));
				if(search):
					#print("labels: "+str(l)+", elements: g1["+str(i)+"]["+str(j)+"] = g2["+str(l[i]-1)+"]["+str(l[j]-1)+"], values: "+str(g1.data[i][j])+ " = "+str(g2.data[l[i]-1][l[j]-1]));
					if(not g1.data[i][j] == g2.data[l[i]-1][l[j]-1]):
						search = False;
		if(search):
			print("label for iso: "+str(l));
			return True;
	print("no iso.");
	return False;

#f = open("ciclos.txt", "a");

#cm = CombMngr();
#table = cm.n_joins_m_grafo(1, 8);

#for row in table:
#	f.write(str(row)+'\n');

#f.close();

#f = open("ciclos.txt", "a");

#cand = [2, 6, 8, 14];
#cm = CombMngr();
#for j in cand:
#	for i in range(j):
#		#print(str(i+1)+"-ciclos del grafo completo K"+str(2*j+1));
#		#print(cm.n_joins_m_grafo(i+1,j));
#		f.write(str(i+1)+"-ciclos del grafo completo K"+str(2*j+1));
#		f.write(str(cm.n_joins_m_grafo(i+1,j)));

#f.close();

#open and read the file after the appending:
#f = open("demofile2.txt", "r")
#print(f.read())
