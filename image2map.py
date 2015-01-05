import imagelab
import sys
import getopt

def usage():
    print "image2map.py [-o output] image"

output_path = "a.map"
try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output"])
except getopt.GetoptError as e:
    print str(e)
    usage()
    sys.exit(1)

for opt, arg in opts:
    if opt in ("--help", "-h"):
        usage()
        sys.exit()
    elif opt in ("--output", "-o"):
        output_path = arg

if len(args) < 1:
    print "Inserisci path immagine"
    usage()
    sys.exit(2)

input_path = args[0]
pos, lista = imagelab.apriImmagine(input_path)
with open(output_path, "w") as output_file:
    output_file.write("r " + str(pos[0]) + " " + str(pos[1]) + "\n")
    for punto in lista:
        output_file.write(str(punto[0]) + " " + str(punto[1]) + "\n")
