

def convert(fileName, HostOrder):
    f = open(fileName, 'r')
    contents = f.read()
    f.close()
    H,P,phi = contents.split(";")
    P = P.strip()
    H = H.strip()
    for key in HostOrder:
        H = H.replace(str(key), str(key) + ':' + str(HostOrder[key]))
    f = open(fileName[:-7] + '.stree', 'w')
    f.write(H + ':1;')
    f.close()
    f = open(fileName[:-7] + '.tree', 'w')
    f.write(P + ";")
    f.close