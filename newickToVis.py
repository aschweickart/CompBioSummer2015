def convert(fileName):
    f = open(fileName, 'r')
    contents = f.read()
    f.close()
    H,P,phi = contents.split(";")
    P = P.strip()
    H = H.strip()
    H = H.replace(',', ':1,')
    H = H.replace(')', ':1)')
    H = H + ":1;"
    f = open('tree and smap files/' + fileName[:-7] + '.stree', 'w')
    f.write(H)
    f.close()
    f = open('tree and smap files/' + fileName[:-7] + '.tree', 'w')
    f.write(P + ";")
    f.close