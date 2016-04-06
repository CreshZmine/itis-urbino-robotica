import nodi

grafo = nodi.Grafo()

a = nodi.Nodo(0,0)
a.vicini = []
b = nodi.Nodo(1,1)
b.vicini = []
c = nodi.Nodo(2,2)
c.vicini = []
d = nodi.Nodo(3,3)
d.vicini = []
e = nodi.Nodo(4,4)
e.vicini = []
f = nodi.Nodo(5,5)
f.vicini = []

a.vicini.append(b)
a.vicini.append(c)
a.vicini.append(d)

b.vicini.append(a)
b.vicini.append(f)
b.vicini.append(e)

c.vicini.append(a)
c.vicini.append(d)

d.vicini.append(a)
d.vicini.append(c)
d.vicini.append(f)

e.vicini.append(b)
e.vicini.append(f)

f.vicini.append(e)
f.vicini.append(b)
f.vicini.append(d)

grafo.nodi.append(a)
grafo.nodi.append(b)
grafo.nodi.append(c)
grafo.nodi.append(d)
grafo.nodi.append(e)
grafo.nodi.append(f)

inizio = a
fine = f

res = grafo.calcola_strada_corta(inizio, fine)
for n in res:
    print str(n.x) + " " + str(n.y) + "\n"
