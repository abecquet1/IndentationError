def get_info(s):

    info = {}
    
    tab = s.split("->")
    info['f_type'] = tab[1]
    
    
    tab = tab[0].split('(')
    info['f_name'] = tab[0]
    tab = tab[1][:-1].split(",")

    for i in range(len(tab)):
        tab[i] = tab[i].split(':')

    info['args'] = [{'var_name': tab[i][0], 'var_type': tab[i][1]} for i in range(len(tab))]
    
    return info

def convert(data, rec_type):
    """
    Convertit le str data en donnée de de type rec_type.
    
    Pour l'instant, ne marche qu'avec :
    --- les types de base : int | float | str | bool
    --- petits types composés : List[type de base] | Set[type de base]
    """
    
    # Types de base
    if rec_type == 'str':
        return data
    if rec_type == 'int':
        return int(data)
    if rec_type == 'float':
        return float(data)
    if rec_type == 'bool':
        if data == "True":
            return True
        else:
            return False
    if rec_type == 'None':
        return None

    # Types composés
    data = data[1:-1]
    print(data)
    data = data.split(',')
    print(data)
    
    if rec_type[0:3] == "Lis":
        rec_type = rec_type[5:-1]
        return [convert(x, rec_type) for x in data]
    if rec_type[0:3] == "Set":
        rec_type = rec_type[4:-1]
        return set(convert(x, rec_type) for x in data)
       



    
def test_fonction(fichier_test, f):
    
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
        
    

