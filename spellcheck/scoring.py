#import spellcheck

def score(edits):
    total_pblty =0
    for edits in multi_edits:
        res = 1
        for edit in edits:
            if edit[0]== "sub":
                res *= float(spellcheck.subMat(edit[1][0], edit[1][1]))/float(spellcheck.charCount(edit[1][1]))
            elif edit[0]== "del":
                res *= float(spellcheck.delMat(edit[1][0], edit[1][1])) / float(spellcheck.charsCooc(edit[1][0], edit[1][1]))
            elif edit[0] == "add":
                res *= float(spellcheck.addMat(edit[1][0], edit[1][1])) / float(spellcheck.charCount(edit[1][0]))
            elif edit[0] == "rev":
                res *= float(spellcheck.revMat(edit[1][0], edit[1][1])) / float(spellcheck.charsCooc(edit[1][0], edit[1][1]))
        total_pblty += res
    return total_pblty


def tranformation(T,C):
    N = len(T)
    M = len(C)
    T = '#'+T
    C = '#'+C
    dist_matrix = [[0]*(M+1) for i in range(N+1)]
    for i in range(N+1):
        dist_matrix[i][0]=i
    for j in range(M+1):
        dist_matrix[0][j] = j
    for i in range(1,N+1):
        for j in range(1,M+1):
            l = 0 if (T[i]==C[j]) else 1
            dist_matrix[i][j] = min ( (dist_matrix[i-1][j] + 1),(dist_matrix[i][j-1] + 1),(dist_matrix[i-1][j-1] + l))
	possible_transformations = get_transformations(N,M,T,C,dist_matrix)
    return possible_transformations

def get_transformations(i,j,T,C,dist_matrix):
    if(i==0 or j==0):
        return []
    list = []
    if T[i-1] == C[j] and T[i] == C[j-1]:                  #rev
        list0 = get_transformations(i-2,j-2,T,C,dist_matrix)
        if list0==[]:
            list0+=[[]]
        list0 = map (lambda p : [('rev', (T[i-1],T[i]))] + p,list0)
        list += list0
    if (dist_matrix[i][j] == dist_matrix[i - 1][j - 1]  and T[i] ==C[j]):       #diag no subs
        list1 =get_transformations(i-1,j-1,T,C,dist_matrix)
        if list1!=[]:
            list+=list1
    if((dist_matrix[i][j] == dist_matrix[i-1][j-1] + 1) and T[i]!=C[j]):        #diag with subs
        list2 =get_transformations(i-1,j-1,T,C,dist_matrix)
        if (list2 == []):
            list2 = [[]]
        list2 = map (lambda p : [('sub', (T[i] , C[j]))] + p,list2)
        list += list2
    if(dist_matrix[i][j] == dist_matrix[i-1][j] + 1 ):              #up
        list3 =get_transformations(i-1,j,T,C,dist_matrix)
        if (list3 == []):
            list3 = [[]]
        list3 = map (lambda p : [('ins',(T[i-1] , T[i]))] + p,list3)
        list += list3
    if (dist_matrix[i][j] == dist_matrix[i][j-1] + 1):          #left
        list4 = get_transformations(i , j-1 , T, C,dist_matrix)
        if (list4 == []):
            list4 = [[]]
        list4 = map(lambda p: [('del', (T[i], C[j]))] + p, list4)
        list += list4
    return list
