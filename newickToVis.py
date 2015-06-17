def convert(fileName):
    f = open(fileName, 'r')
    contents = f.read()
    f.close()
    P,H,phi = contents.split(";")
    P = P.strip()
    H = H.strip()
    phi = phi.strip()
    print phi
    f = open('tree and smap files/' + fileName[:-7] + '.smap', 'w')
    for item in phi:
        item = item.replace(":"," ")
        f.write(item)
    f.close()
    f = open('tree and smap files/' + fileName[:-7] + '.tree', 'w')
    f.write(P)
    f.close()
    f = open('tree and smap files/' + fileName[:-7] + '.stree', 'w')
    f.write(H)
    f.close