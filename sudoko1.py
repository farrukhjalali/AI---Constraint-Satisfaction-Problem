# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:41:05 2017

@author: Farrukh Jalali

This prorgram solves the Sudoko game usig Constraint Satisfaction Prfoblem based algorithm from AI. First AC3 lgorithm is implemented on a given initial board to solve and bag all the feasible solution for all states. Then Backtracking has been implemneted using Minimum Remaining Value and Forward Checking hueristics.
"""
import numpy as np
import itertools as it
import copy as cp
import time

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]
    
    
string   = 'ABCDEFGHI'
digits   = '123456789'
rows     = string
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
            
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def c_FoundInCell(d, i, j):
    t = {}
    
    if len(d[i]) > 1 and len(d[j]) == 1:
        t = d[i] & d[j]
    return t

def Revise(csp, i, j):
    revise = False
    foundC = c_FoundInCell(csp, i, j)
    
    if foundC:
        for e in foundC:
            csp[i].discard(e)
        revise = True

    return revise
        
def ac3(csp):
    #Initial domain are made consistent with unary constraint
    queue = [(Xi, Xk) for Xi in squares for Xk in peers[Xi]]
    
    while queue:
        r = queue.pop(0)
        vi, vj = r[0], r[1]

        if Revise(csp, vi, vj):
            if not csp[vi]:
                d = np.array([{}]*81).reshape(9,9)
                for i in csp.keys():
                    d[i] = csp[i]
                return {}
            n = peers[vi]
            if n:
                for neighbor in n:
                    if neighbor != vj:
                        queue.append((neighbor, vi))
   
    return csp

#################################################

# Minimum Remianing Value
def MRV(csp, i):
    return min((len(v), i) for (i,v) in csp.items() if len(v) > 1)[1]
    

def ForwardChecking(csp, var, value, i):
    success = True
    neighborhood = peers[var] #csp.getArcs(var)

    for neighbor in neighborhood:
#        if neighbor == 'A7' and value == 1:
#            print("del %d of %s on level %d due to %s with value %d. remaining values are"%(value,neighbor,i,var,min(csp[var])))
#            print(csp[neighbor])
#        elif var == 'A7':
#            print("A7 is chosen one with %d on level %d"%(value,i))
        
        csp[neighbor].discard(value)
 
#        if neighbor == (7,4) and i == 36:
#            print(neighbor)
        if not csp[neighbor]:
            success = False
            break
    return success

def checkConsistency(csp, crd_i):
#    if csp.d[(7,0)] == {5} and csp.d[(8,0)] == {5}:
#        print(crd_i)
    unit = units[crd_i]
    
    for u in unit:
        comm = set()
        for ro in u:
            if len(csp[ro])==1:
                if comm & csp[ro]:
                    return False
                else:
                    comm.add(min(csp[ro]))
    return True

def OrderValues(csp, var, values):
    cspCopy = { key:set(value) for key,value in csp.items() }
    
    for val in values:
        cspCopy[var] = {val}
        
        f = True
        for p in peers[var]:
            if not checkConsistency(cspCopy, var):        
                f = False
                break
        return f
        
def backtrack(csp, i):
    if len(max(csp.items(), key=lambda v: len(v[1]))[1]) == 1:
        return csp

    var = MRV(csp, i)      # SELECT_UNASSIGNED_VARIABLE
    
    values = csp[var]
    
    for value in values:
        cspCopy = { key:set(value) for key,value in csp.items() }

            
        cspCopy[var] = {value}
        result = ForwardChecking(cspCopy, var, value, i)
        
        if result == False:
            continue
        
        if not checkConsistency(cspCopy, var):        
            continue
        
        res = backtrack(cspCopy, i+1)
        
        if res != False:
            return res
        
    return False
    
def backtracking_search(csp):
    return backtrack(csp, 1)

def createBoard(inp):
    board = {}
    
    for i in range(81):
        val = int(inp[i])
        if val != 0:
            board[squares[i]] = set([val])
        else:
            board[squares[i]] = set(range(1,10))  
    return board

def main():
    sTot=time.clock()
    
    f = open("sudokus_start.txt","r")
    re = open("sudokus_finish.txt","r")
    
    i=0
    
    pLines = f.read().splitlines()
    sLines = re.read().splitlines()
    
    #tt = open("t.csv","w")
    tt = open("output.csv","w")
    
    for line in pLines:
        line = 
        line = pLines[i]
        tsta = time.clock()
        c = createBoard(line)
        cpp = ac3(c)
        if cpp:
            t = backtracking_search(cpp)
        tdiff = time.clock() - tsta    
        st = ''
        if type(t) != bool:
            for sq in squares:
                st = st + str(min(t[sq]))
            
            if st == sLines[i]:
                print("No %d is solved in %d min(s) %d sec(s)"%(i,int(tdiff/60),int(tdiff%60)))
            else:
                print("No %d has Run in %d min(s) %d sec(s)"%(i,int(tdiff/60),int(tdiff%60)))
        else:
            print("No %d is not solved in %d min(s) %d sec(s)"%(i,int(tdiff/60),int(tdiff%60)))
            
            tt.write(st+'\n')
        i += 1
    f.close()
    tt.close()
    Tot = time.clock() - sTot
    
    print("Total Time for the program is %d mins %d secs "%(int(Tot/60), int(Tot%60)))

if __name__  == "__main__":
	main()
