import numpy.polynomial.polynomial as poly
import numpy as np

def polyKofaktor(M):
    # M adalah sebuah matriks persegi
    # Mengembalikan determinan matriks M (polinom karakteristik matriks M)
    # dengan metode kofaktor rekursif

    # KAMUS LOKAL
    # minorMat : polynomial[][]
    # polyEq, polyTmp : polynomial
    # dim : int
    # i, j, k = int

    # ALGORITMA
    dim = len(M)
    if(dim == 1):
        return M[0][0]
    else:
        minorMat = [[0 for i in range(dim-1)] for i in range(dim-1)]
        polyEq = 0
        for i in range(dim):
            # Copy matriks minor
            for j in range(1, dim):
                for k in range(i):
                    minorMat[j-1][k] = M[j][k]

            for j in range(1, dim):
                for k in range(i+1, dim):
                    minorMat[j-1][k-1] = M[j][k]

            # hitung polynomial
            polyTmp = poly.polymul(M[0][i], polyKofaktor(minorMat))
            if(i%2 == 0):
                polyTmp = [(-x) for x in polyTmp]
            polyEq = poly.polyadd(polyEq, polyTmp)

        return polyEq
    #


def eigenValue(A):
    # A adalah sebuah matriks persegi
    # Mengembalikan nilai-nilai eigen melalui akar-akar
    # persamaan karakteristik dari A dengan metode kofaktor

    # KAMUS LOKAL
    # eigMat : polynomial[][]
    # charPol : polynomial
    # i : int
    # roots : float[]

    # ALGORITMA
    eigMat = [[El for El in ROW] for ROW in A]  # buat matriks A - λI
    for i in range(0,len(eigMat)):  # Karena eigMat adalah matriks persegi, jumlah baris dan kolom sama
        eigMat[i][i] = (eigMat[i][i], -1)
    
    charPol = polyKofaktor(eigMat)
    roots =  poly.polyroots(charPol)
    # round to nearest 16
    roots = np.round_(roots, decimals = 16)
    roots = [*set(roots)]
    return roots



def eigenVectors(A, eigVal):
    # A adalah sebuah matriks persegi
    # mengembalikan vektor-vektor basis eigen A
    # dari nilai eigen eigVal

    # KAMUS LOKAL
    # M, lmdI, ret : float[][]
    # R : (float[][], int[])    # value hasil method sp.rref()
    # n, i, j, t : int
    # r, c, rpivot : int
    # prec = int


    # ALGORITMA
    dim = len(A)
    lmdI = np.identity(dim) * eigVal
    M = [[El for El in ROW] for ROW in A]
    M = np.array(M)
    M = M - lmdI
    M = np.round_(M, decimals = 16)

    prec = 16
    while True:
        # Eliminasi Gauss-Jordan
        Mtemp = [[El for El in ROW] for ROW in M]
        r=0; c=0
        while(r < dim and c < dim):
            rpivot = r
            while(rpivot < dim-1 and Mtemp[rpivot][c] == 0):
                rpivot = rpivot + 1
            # rpivot = dim-1 or m[rpivot][c] != 0
            if(Mtemp[rpivot][c] != 0):
                # tukar baris dengan pivot
                if(r != rpivot):
                    temp = Mtemp[r]
                    Mtemp[r] = Mtemp[rpivot]
                    Mtemp[rpivot] = temp
                
                # bagi baris pivot dengan elemen bukan 0 pertama
                Mtemp[r] = Mtemp[r]/Mtemp[r][c]

                # eliminasi turun
                for i in range(r+1,dim):
                    Mtemp[i] = Mtemp[i] - Mtemp[r]*Mtemp[i][c]
                
                # eliminasi naik
                for i in range(r):
                    Mtemp[i] = Mtemp[i] - Mtemp[r]*Mtemp[i][c]

                
                Mtemp = np.round_(Mtemp, decimals = prec)
                r = r+1
            c = c+1
        # r == dim or c == dim
        
        if (r != dim):
            break
        else:
            prec = prec - 1
        
    n = dim-r   # jumlah vektor basis adalah dimensi matriks - jumlah baris bukan 0
    ret = [[0 for i in range(dim)] for j in range(n)]
    t = 0
    for i in range(dim):
        if(Mtemp[i][i] == 0):
            ret[t] = [-Mtemp[j][i] for j in range(dim)]
            ret[t][i] = 1

    return ret
    #





























# EIGENVALUE CALCULATIONS BY THE BOOK!!!
# + NO QR DECOMPOSITION!!!
# + NAIVE IMPLEMENTATION POSSIBLE WITH BASIC KNOWLEDGE OF EIGEN VALUE!!!
# + IKUT KELAS ALGEO 100% WORK NO HACK REQUIRED!!!
# - require built-in polynomial function to solve polynomial roots
# - computationally expensive