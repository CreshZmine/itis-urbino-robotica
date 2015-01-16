import nodi

a = nodi.nodo(0,0)
a.vicini = []
b = nodi.nodo(1,1)
b.vicini = []
c = nodi.nodo(2,2)
c.vicini = []
d = nodi.nodo(3,3)
d.vicini = []
e = nodi.nodo(4,4)
e.vicini = []
f = nodi.nodo(5,5)
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

inizio = a
fine = f

res = nodi.calcola_strada_corta(inizio, fine)
for n in res:
    print str(n.x) + " " + str(n.y) + "\n"
