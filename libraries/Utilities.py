def grabber(path,rowno=0,delfirst=False):
    with open(path,"r") as data:
        tmp=[]
        for line in data:
            tmp.append(line.split())
    if delfirst==True:
        del tmp[0]
    tmp2=[]
    for i in range(len(tmp)):
        tmp2.append(float(tmp[i][rowno]))
    return tmp2

def Ha_to_kJmol(listofenergies,negative=False):
    for i in range(len(listofenergies)):
        listofenergies[i]=listofenergies[i]*2625.5
        if negative==True:
            listofenergies[i]=listofenergies[i]*(-1)
    return listofenergies