import sys
from io import StringIO
from random import *
import inspect 

FAR = "FAR" # fonction arguments résultat
FAO = "FAO" # fonction argument output
FCC = "FCC" # fonction context context
CIO = "CIO" # code input output
CCC = "CCC" # code context context 


def clean(ligne):
    return ligne.strip().replace(' ','')



def get_type(t):
    i = 0
    while i < 4:
        if t[i][0:4] == "TYPE":
            return clean(t[0])[5:]



def get_sign(t):
    i = 0
    while i < 4:
        if t[i][0:4] == "SIGN":
            
            sign = {}
            tab = clean(t[i])[5:].split("->")
            
            sign['f_type'] = tab[1]
            
            tab = tab[0].replace(')', '(').replace(" ","").split('(')
            sign['f_name'] = tab[0]
            
            tab = tab[1].split(",")

            sign["args"] = {}
            if tab != [""]:
                for i in range(len(tab)):
                    tab[i] = tab[i].split(':')

                sign['args'] = [{'var_name': tab[i][0], 'var_type': tab[i][1]} for i in range(len(tab))]
            return sign 
        i+=1

def get_ctxt_info(t):
    i = 0
    while i < 4:
        if t[i][0:4] == "CTXT":
            context1 = {}
            context2 = {}
            tab = clean(t[i])[5:].split("->")

            tab[0] = tab[0].split(";")
            tab[1] = tab[1].split(";")

            for s in tab[0]:
                var = s.split(":")
                context1[var[0]] = var[1]

            for s in tab[1]:
                var = s.split(":")
                context2[var[0]] = var[1]

            return context1, context2
        i+=1



def get_info(t):
    info = {}
    info["TYPE"] = get_type(t)

    if info["TYPE"][0] == "F": 
        info["SIGN"] = get_sign(t)

    if info["TYPE"][1] == "C": 
        info["CTXT1"], info["CTXT2"] = get_ctxt_info(t)
    
    return info

def get_DATA_FAR(t):
    info = get_info(t)
    assert info["TYPE"] == FAR, "mauvais get_DATA"
    i = 0
    while t[i][0:4] != "DATA":
        i = i+1
    i = i+1
    arguments = []
    resultats = []
    for k in range(i, len(t)):
        t[k] = clean(t[k])
        if t[k] != "":
            t[k] = t[k].split("->")

            print(t[k][0])

            arguments.append( [eval(x) for x in t[k][0].split(";") ])
            resultats.append( eval(t[k][1]))
    return arguments, resultats
        
    
    

def get_DATA_FCC(t):
    info = get_info(t)
    assert info["TYPE"] == FCC, "mauvais get_DATA"
    i = 0
    while t[i][0:4] != "DATA":
        i = i+1
    i = i+1
    CL1 = []
    CL2 = []
    for k in range(i, len(t)):
        t[k] = clean(t[k])
        if t[k] != "":
            t[k] = t[k].split("->")
            
            CL1.append( {x.split("=")[0]:eval(x.split("=")[1]) for x in t[k][0].split(";")} )
            CL2.append( {y.split("=")[0]:eval(y.split("=")[1]) for y in t[k][1].split(";")} )

    return CL1, CL2




def get_DATA_CCC(t):
    info = get_info(t)
    assert info["TYPE"] == CCC, "mauvais get_DATA"
    i = 0
    while t[i][0:4] != "DATA":
        i = i+1
    i = i+1
    CL1 = []
    CL2 = []
    for k in range(i, len(t)):
        t[k] = clean(t[k])
        if t[k] != "":
            t[k] = t[k].split("->")
            
            CL1.append( {x.split("=")[0]:eval(x.split("=")[1]) for x in t[k][0].split(";")} )
            CL2.append( {y.split("=")[0]:eval(y.split("=")[1]) for y in t[k][1].split(";")} )

    return CL1, CL2


def get_DATA_CIO(t):
    info = get_info(t)
    assert info["TYPE"] == CIO, "mauvais get_DATA"
    i = 0
    while t[i][0:4] != "DATA":
        i = i+1
    i = i+1
    arguments = []
    resultats = []
    for k in range(i, len(t)):
        t[k] = clean(t[k])
        if t[k] != "":
            t[k] = t[k].split("->")
            arguments.append( [x for x in t[k][0].split(";")] )
            resultats.append( t[k][1])
    return arguments, resultats


def get_DATA_FAO(t):
    info = get_info(t)
    assert info["TYPE"] == FAO, "mauvais get_DATA"
    i = 0
    while t[i][0:4] != "DATA":
        i = i+1
    i = i+1
    arguments = []
    resultats = []
    for k in range(i, len(t)):
        t[k] = clean(t[k])
        if t[k] != "":
            t[k] = t[k].split("->")
            arguments.append( [eval(x) for x in t[k][0].split(";")] )
            resultats.append( eval(t[k][1]))
    return arguments, resultats



def convert(data, rec_type):
    return eval(data)
       



""" 
def test_fonction(fichier_test, f):
    # DEP
    fichier_test = fichier_test.replace(' ', '')
    fichier_test = fichier_test.split("\n")[:-1]


    info = get_info(fichier_test[0])

    res_type = info['f_type']

    n = len(info['args'])
    
    for i in range(1, len(fichier_test)):
        fichier_test[i] = fichier_test[i].split(";")

        args = []
        for j in range(n):
            x = convert(fichier_test[i][j], info['args'][j]['var_type'])
            args.append(x)

        res = convert(fichier_test[i][n], info['f_type'])

        res_calc = f(*args)
        assert res_calc == res, "Echec du test "+str(i)+" sur "+str(len(fichier_test)-1)+" : \n    Arguments donnés : "+str(args)[1:-1]+"\n    Résutat calculé : "+str(res_calc)+"\n    Résultat attendu : "+str(res)+"\n"

    print(f"\nTous les tests ({len(fichier_test)-1}/{len(fichier_test)-1}) ont été passés avec succès !\n")
    return True
"""        
    
def test_FAR(arguments, resultats, f):  # ça a l'air de fonctionner
    n = len(arguments)
    
    for i in range(n):

        args = arguments[i]
        res = resultats[i]
        res_calc = f(*args)

        assert res_calc == res, "Echec du test "+str(i+1)+" sur "+str(n)+" : \n    Arguments donnés : "+str(args)+"\n    Résutat calculé : "+str(res_calc)+"\n    Résultat attendu : "+str(res)+"\n"

    print(f"\nTous les tests ({n}/{n}) ont été passés avec succès !\n")
    return True
        
   


### Fonctions print ###

def test_FAO(arguments, resultats,  f): # ça a l'air de fonctionner
    #ça marche /o/

    old = sys.stdout
    n = len(arguments)
  
    for i in range(n):

        sys.stdout = StringIO()
        args = arguments[i]
        res = resultats[i]
        f(*args)
        res_calc = sys.stdout.getvalue()
        
        assert res_calc == res, "Echec du test "+str(i+1)+" sur "+str(n)+" : \n    Arguments donnés : "+str(args)+"\n    Résutat calculé : "+str(res_calc)+"\n    Résultat attendu : "+str(res)+"\n"

    sys.stdout = old
    print(f"\nTous les tests ({n}/{n}) ont été passés avec succès !\n")
    return True





### Code input / affichage ###

def test_CIO(arguments, resultats, s): # ça a l'air de fonctionner

    old = sys.stdout
    n = len(arguments)

    
    for i in range(n):

        sys.stdout = StringIO()

        
        args = arguments[i]
        args.reverse()
        res = eval(resultats[i])

        def get_input(*prompt):
            return convert(args.pop(), None)

        context = {"input": get_input}
        exec(s, context)

        res_calc = sys.stdout.getvalue()

        print(res_calc)
        print(res)
        
        assert res_calc == res, "Echec du test "+str(i+1)+" sur "+str(n)+" : \n    Arguments donnés : "+str(args)+"\n    Résutat calculé  : "+str(res_calc)+"    Résultat attendu : "+str(res)+"\n"

    sys.stdout = old
    print(f"\nTous les tests ({n}/{n}) ont été passés avec succès !\n")
    return True






### Fonctions context ###

def test_FCC(CL1, CL2, f): # ça marche pas 
    #ça marche aussi \o\
    n = len(CL1)

    for i in range(n):

        context = CL1[i].copy()
        exec(inspect.getsource(f), context) # définit f dans le contexte 
        exec("f()", context)                # exécute f dans le contexte 
        

        context_res = {}
        for v in CL1[i]:
            context_res[v] = context[v]

        assert context_res == CL2[i], "Echec du test "+str(i+1)+" sur "+str(n)+" : \n    Arguments donnés : "+str(CL1[i])+"\n    Résutat calculé : "+str(CL2[i])+"\n    Résultat attendu : "+context+"\n"

    print(f"\nTous les tests ({n}/{n}) ont été passés avec succès !\n")
    return True





### Code context ###

def test_CCC(CL1, CL2, s): # ça a l'air de fonctionner
    #ça marche aussi \o\
    n = len(CL1)
    
    for i in range(n):
        
        context = CL1[i].copy()
        exec(s, context)
        
        context_res = {}
        for v in CL1[i]:
            context_res[v] = context[v]


        assert context_res == CL2[i], "Echec du test "+str(i+1)+" sur "+str(n)+" : \n    Arguments donnés : "+str(CL1[i])+"\n    Résutat calculé : "+str(context_res)+"\n    Résultat attendu : "+str(CL2[i])+"\n"


    print(f"\nTous les tests ({n}/{n}) ont été passés avec succès !\n")
    return True





