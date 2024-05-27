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

def distance_calc(xyz_file, A_id, B_id):
    with open(xyz_file, "r") as xyz:
        tmp = []
        for line in xyz:
            tmp.append(line.split())
    return tmp



def distance_calc(A_id, B_id, N_structures, path):
    import numpy as np
    N_iterator = list(range(1,N_structures+1))    
    distances = []

    for N in N_iterator:
        xyz_file = path + "input." + str(N).zfill(3) + ".xyz"
        with open(xyz_file, "r") as xyz:
            tmp = []
            for line in xyz:
                tmp.append(line.split())

            A_coords = np.array(tmp[A_id + 2][1:]).astype(np.float32)
            B_coords = np.array(tmp[B_id + 2][1:]).astype(np.float32)

            distances.append(np.linalg.norm(A_coords - B_coords))
    return distances
    

