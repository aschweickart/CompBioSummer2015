
import orderGraph

def convert(fileName, HostOrder):
    f = open(fileName, 'r')
    contents = f.read()
    f.close()
    H,P,phi = contents.split(";")
    P = P.strip()
    H = H.strip()
    f = open('tree and smap files/' + fileName[:-7] + '.stree', 'w')
    f.write(H)
    f.close()
    f = open('tree and smap files/' + fileName[:-7] + '.tree', 'w')
    f.write(P + ";")
    f.close