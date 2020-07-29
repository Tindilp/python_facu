import PySimpleGUI as sg
import random
from pattern.text.es import lexicon, spelling, verbs
from itertools import permutations
from funciones import funciones

def validar_palabra(permutaciones, permutaciones_validas):
    """
        Valida palabras que esten dentro de las permutaciones
        pasadas por parametro y las agrega a una lista de palabras
        validas
    """
    for pal in permutaciones:
        if pal in lexicon and spelling or pal in verbs:
            # if pal in verbs or ((pal in lexicon) and (pal in spelling)):
            # si la palabra es valida va a la lista de permutaciones
            permutaciones_validas.append(pal)
    return permutaciones_validas

def buscar_palabras_rival(letras_atril_rival):
    """
        recibe el las fichas del atril del rival y genera una lista de
        palabras validas
    """
    # lista vacia para guardar las permutaciones validas
    permutaciones_validas = []
    for i in range(len(letras_atril_rival)):
        # este if es para empezar a armar permutaciones de al menos dos
        #  caracteres generamos permutaciones con i+1 caracteres
        if (i+1 >= 2):
            permutaciones_temp = {
                "".join(p) for p in permutations(letras_atril_rival, i+1)}
            # vemos cuales de esas permutaciones son validas, y las vamos
            # guardando en una lista
            validar_palabra(permutaciones_temp, permutaciones_validas)
    return permutaciones_validas

def todas_los_posiciones_validas(tamanio_pal, lugar, lugar_aux,
                                 lugares_no_disponibles, orientacion):
    """
        Aca validamos que todos los lugares que van a ir las letras
        en el tablero sean validos. En caso de que haya lugares ocupados,
        nos devolvera False
    """
    ok = True
    for i in range(tamanio_pal):
        if (orientacion == 0):
            lugar_aux = lugar[0], lugar[1]+i
        else:
            lugar_aux = lugar[0]+i, lugar[1]
        # print('verificando lugar...', lugar_aux) #test
        # print('lugares no disponibles ',lugares_no_disponibles) #test
        if lugar_aux in lugares_no_disponibles:
            ok = False
    # print('Se puede poner?.....', ok)  # test
    return ok

def colocar_en_tablero(window, palabra_a_colocar, letras_usadas_en_tablero,
                       lugar, letras_atril_rival, lugares_no_disponibles, x,
                       y, orientacion, tamanio_pal, l2_guar):
    """
        En este metodo colocamos las letras de las palabras en el tablero,
        recorremos la palabra y por cada letra, la agregamos al tablero,
        la removemos del atril, y guardamos los lugares no disponibles a
        la lista de lugares ocupados en el tablero
    """
    for i, l in zip(range(tamanio_pal), palabra_a_colocar):
        if (orientacion == 0):
            lugar_aux = lugar[0], lugar[1]+i
        else:
            lugar_aux = lugar[0]+i, lugar[1]
        # print(lugar, ': lugar=lugar_aux :', lugar_aux) # test
        letras_usadas_en_tablero.append(l)
        # print('poniendo en el lugar...', lugar_aux)
        window[lugar_aux].update(l.upper(), button_color=('black', 'oldlace'))
        letras_atril_rival.remove(l.upper())
        lugares_no_disponibles.append(lugar_aux)
        l2_guar.extend(l.upper())

def chequeo_y_colocacion(tamanio_pal, x, y, lugar, lugar_aux,
                         lugares_no_disponibles, orientacion, window,
                         palabra_a_colocar, letras_usadas_en_tablero,
                         letras_atril_rival, l2_guar):
    """
        Metodo general en el cual se chequean las palabras y se colocan en el
        tablero
    """
    print('lugar que va a chequear...', lugar)
    print('cordenadas check...', x, ' ', y, ' orientacion ', orientacion)
    ok = todas_los_posiciones_validas(
        tamanio_pal, lugar, lugar_aux, lugares_no_disponibles, orientacion)
    if (ok):
        colocar_en_tablero(
            window, palabra_a_colocar, letras_usadas_en_tablero, lugar,
            letras_atril_rival, lugares_no_disponibles, x, y, orientacion,
            tamanio_pal, l2_guar)

    return ok

def seteando_orientacion(tamanio_pal, cord1, cord2, lugar, lugar_aux,
                         lugares_no_disponibles, orientacion, window,
                         palabra_a_colocar, letras_usadas_en_tablero,
                         letras_atril_rival, l2_guar):
    """
       En este metodo nos llegaran el lugar, la palabra a colocar y la
       orientacion, y  se analizan los casos posibles para colocarla en
       el tablero.
       Primero verifica que entre en la orientacion deseada, luego en caso de
       no poder se intentara poner desde el mismo lugar que se deseaba
       pero en la orientacion contraria, y en caso de no poder nos avisara
       que no se puedo colocar
    """
    print('palabra_a_colocar.....', palabra_a_colocar)
    print('x...', cord1, ', y...', cord2)
    print('orientacion...', orientacion)
    print('lugar que llega...', lugar)
    ok = False
    if orientacion == 0:
        print(tamanio_pal-1, '+', cord2, '< 15')
        # si es horizontal chequeamos que y sea valida
        if (((tamanio_pal-1)+cord2) < 15):
            print('cordenadas horziontal...', cord1, ' ',
                  cord2, ' orientacion ', orientacion)
            ok = chequeo_y_colocacion(tamanio_pal, cord1, cord2, lugar,
                                      lugar_aux, lugares_no_disponibles,
                                      orientacion, window,
                                      palabra_a_colocar,
                                      letras_usadas_en_tablero,
                                      letras_atril_rival, l2_guar)
        else:
            print('cordenadas horziontal NO ENTRAN, VEAMOS SI ENTRAN DE FORMA',
                  'VERTICAL...', tamanio_pal-1, '+', cord2, '< 15')
            orientacion = 1
            if (((tamanio_pal-1)+cord1) < 15):
                ok = chequeo_y_colocacion(tamanio_pal, cord2, cord1, lugar,
                                          lugar_aux, lugares_no_disponibles,
                                          orientacion, window,
                                          palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)

    elif orientacion == 1:
        print(tamanio_pal-1, '+', cord1, '< 15')
        # si es vertical chequeamos que x sea valida
        if (((tamanio_pal-1)+cord1) < 15):
            print('cordenadas vertical...', cord1, ' ',
                  cord2, ' orientacion ', orientacion)
            ok = chequeo_y_colocacion(tamanio_pal, cord1, cord2, lugar,
                                      lugar_aux, lugares_no_disponibles,
                                      orientacion, window,
                                      palabra_a_colocar,
                                      letras_usadas_en_tablero,
                                      letras_atril_rival, l2_guar)
        else:
            print('cordenadas vertical NO ENTRAN, VEAMOS SI ENTRAN DE FORMA',
                  'HORIZONTAL...', tamanio_pal-1, '+', cord2, '< 15')
            orientacion = 0
            print(tamanio_pal-1, '+', cord2, '< 15')
            if (((tamanio_pal-1)+cord2) < 15):
                ok = chequeo_y_colocacion(tamanio_pal, cord2, cord1, lugar,
                                          lugar_aux, lugares_no_disponibles,
                                          orientacion, window,
                                          palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)
    else:
        sg.popup('No entra la palabra')

    if (not ok):
        sg.popup('No entra la palabra')
    return ok

def buscar_lugar_disponible(window, letras_atril_rival, lugar,
                            lugares_no_disponibles, cant,
                            bolsa_total, letras_usadas_en_tablero,
                            dificultad, l2_guar):
    """
        Para el turno de la maquina Buscamos un lugar en el tablero de forma
        aleatoria en el cual colocaremos la palabra, en caso de no tener
        palabras validas, pasa el turno
    """
    # pasa la lista a minusculas xq las permutaciones no las reconocen las
    # letras en mayuscula
    letras_atril_rival_aux = [x.lower() for x in letras_atril_rival]
    # obtenemos una lista con las posibles palabras
    palabras_posibles = buscar_palabras_rival(
        letras_atril_rival_aux)
    # intentamos obtener alguna palabra de la lista, en caso que la lista no
    # tenga palabras validas
    # se pasa el turno
    puntos_npc = 0
    try:
        # obtenemos alguna de las palabras posibles de la lista al azar si es
        # posible
        palabra_a_colocar = random.choice(palabras_posibles)
        # Ya tenemos la palabra, ahora buscamos lugar disponible
        ok = False
        while (not ok) & (cant < 3):
            x = random.choice(range(0, 15))
            y = random.choice(range(0, 15))
            lugar = (x, y)
            cant += 1
            # Primero vemos si el lugar seleccionado esta disponible
            if lugar not in lugares_no_disponibles:
                # orientacion si la variable es 0 , va a intentar primero
                # poner la palabra horizontalnen caso contrario, si es 1 va
                # intentar ponerla en vertical
                orientacion = random.choice(range(0, 2))
                tamanio_pal = len(palabra_a_colocar)
                lugar_aux = lugar
                # Segundo vemos si la palabra no se va de los limites
                ok = seteando_orientacion(tamanio_pal, x, y, lugar, lugar_aux,
                                          lugares_no_disponibles, orientacion,
                                          window, palabra_a_colocar,
                                          letras_usadas_en_tablero,
                                          letras_atril_rival, l2_guar)
        ##########################################################################################################################################
        # necesito una lista de coords que son los ultimos de lugares_no_disponibles
        lista_coords = []
        for i in range(1, tamanio_pal+1):
            element = lugares_no_disponibles[-i]
            lista_coords.append(element)
        lista_coords.reverse()
        # ahora tengo "letras_usadas_en_tablero" y "lista_coords" si esta bien hecho puedo recorrer las dos listas y usar las funciones de
        # que ya tenemos y no nececitams hacer otro
        for i in range(tamanio_pal):
            aux = funciones.puntos_de_letra(letras_usadas_en_tablero[i], dificultad,
                                  lista_coords[i])
            # print('valor de letra...',aux, 'letra',letras_usadas_en_tablero[i])
            puntos_npc = puntos_npc + aux
        # print('valor de total...',puntos_npc)
        for i in range(tamanio_pal):
            puntos_npc2 = funciones.puntos_de_palabra(
                dificultad, lista_coords[i], puntos_npc)
        # print('valor de total con modificador...',puntos_npc2)
        ##########################################################################################################################################
        for i in range(len(letras_usadas_en_tablero)):
            letra = funciones.crear_atril(bolsa_total)
            letras_atril_rival.append(letra)
        letras_usadas_en_tablero.clear()
        return puntos_npc
    except (IndexError):
        sg.Popup('La maquina no tiene palabras validas para',
                 'colocar pasa el turno')
        return 0

def turno_maquina(window, letras_atril_rival, lugar, lugares_no_disponibles,
                  turno, bolsa_total, letras_usadas_en_tablero, dificultad, l2_guar):
    """
        Comienza el turno de la maquina:
        - La maquina tendra 3 intentos para buscar lugar disponible,
          en caso de no encontrarlo debera pasar el turno
        - en la funcion buscar_lugar_disponible se desarrolla la parte
          de buscar una palabra valida, un lugar disponible, y colocar
          la palabra en el tablero
    """
    sg.Popup('Turno de la maquina')
    cant = 0  # intentos para buscar palabras en cada turno inicializa en 0
    puntos = buscar_lugar_disponible(window, letras_atril_rival,
                                     lugar, lugares_no_disponibles, cant,
                                     bolsa_total, letras_usadas_en_tablero,
                                     dificultad, l2_guar)

    return puntos, 'player_1'