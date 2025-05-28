

def calcular_first(producciones, terminales, no_terminales):
    FIRST = {nt: set() for nt in no_terminales}
    cambio = True
    while cambio:
        cambio = False
        for nt in no_terminales:
            for prod in producciones[nt]:
                for simbolo in prod:
                    if simbolo in terminales:
                        if simbolo not in FIRST[nt]:
                            FIRST[nt].add(simbolo)
                            cambio = True
                        break
                    elif simbolo in no_terminales:
                        antes = len(FIRST[nt])
                        FIRST[nt].update(FIRST[simbolo] - {"ε"})
                        if "ε" not in FIRST[simbolo]:
                            break
                        if len(FIRST[nt]) > antes:
                            cambio = True
                    elif simbolo == "ε":
                        if "ε" not in FIRST[nt]:
                            FIRST[nt].add("ε")
                            cambio = True
                        break
    return FIRST


def calcular_follow(producciones, terminales, no_terminales, first, simbolo_inicial):
    FOLLOW = {nt: set() for nt in no_terminales}
    FOLLOW[simbolo_inicial].add("$")
    cambio = True
    while cambio:
        cambio = False
        for nt in no_terminales:
            for prod in producciones[nt]:
                for i, simbolo in enumerate(prod):
                    if simbolo in no_terminales:
                        siguiente = prod[i+1:] if i+1 < len(prod) else []
                        first_siguiente = set()
                        for s in siguiente:
                            if s in terminales:
                                first_siguiente.add(s)
                                break
                            elif s in no_terminales:
                                first_siguiente.update(first[s] - {"ε"})
                                if "ε" not in first[s]:
                                    break
                            elif s == "ε":
                                first_siguiente.add("ε")
                                break
                        else:
                            first_siguiente.add("ε")
                        antes = len(FOLLOW[simbolo])
                        FOLLOW[simbolo].update(first_siguiente - {"ε"})
                        if "ε" in first_siguiente or not siguiente:
                            FOLLOW[simbolo].update(FOLLOW[nt])
                        if len(FOLLOW[simbolo]) > antes:
                            cambio = True
    return FOLLOW