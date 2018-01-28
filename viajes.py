# -*- coding: utf-8 -*-

import math


class C_Trayecto:
    Km = 0.0
    Transporte = ""
    Coste = 0

    def __init__(self):
        self.Km = 0.0
        self.Transporte = "Coche"
        self.Coste = 0

    def Calcular_Coste(self):
        # El precio es calculado teniendo en cuenta que cada 100 km se gastan 7 litros y que el precio del litro se pone a 1,2.
        # Se suman 50 km de excursiones.
        if self.Transporte == "Coche":
            self.Coste = (float(self.Km) + 50.0) * 7.0 / 100.0 * 1.3

    def Calcula_Trayecto(self, V_Km, V_Transporte, V_Coste):
        self.Km = V_Km
        self.Transporte = V_Transporte
        self.Coste = V_Coste
        self.Calcular_Coste()

    def Imprimir(self):
        print("El viaje es en: " + self.Transporte + ".\n")
        if self.Transporte == "Coche":
            print("Hay:" + str(self.Km) + " km.\n")
            print("Se calcula que cuesta:" + str(self.Coste) + " euros en total.\n")
        else:
            print("El vuelo cuesta:" + str(self.Coste) + " euros en total.\n")


class C_Viaje:
    Lugar = ""
    Coste_Alojamiento_Por_Persona = 0
    Coste_Excursiones_Por_Persona = 0
    Coste_Trayecto_Por_Persona = 0
    Duracion = 0
    Trayecto_Viaje = C_Trayecto()
    Personas = 0
    Coches = 0
    Gastos_Diarios_Por_Persona = 0

    def __init__(self):
        self.Lugar = ""
        self.Coste_Trayecto_Por_Persona = 0
        self.Coste_Alojamiento_Por_Persona = 0
        self.Coste_Excursiones_Por_Persona = 0
        self.Gastos_Diarios_Por_Persona = 0
        self.Duracion = 0
        self.Personas = 0
        self.Coches = 0

    def Imprimir(self):
        print("El viaje es a: " + self.Lugar + ". En " + self.Trayecto_Viaje.Transporte)
        print("Duracion     : " + str(self.Duracion))
        print("Van          : " + str(self.Personas) + " personas")
        if self.Trayecto_Viaje.Transporte == "Coche":
            print("Iran         : " + str(int(self.Coches)) + " coches.\n" + "Se calculan  : " + str(
                self.Trayecto_Viaje.Km) + " km.\n"
                                          "El coste del trayecto en coche es un total de: " + str(
                self.Trayecto_Viaje.Coste) + " euros")
        else:
            print("El vuelo cuesta: " + str(self.Trayecto_Viaje.Coste))
        print(
            "El precio del alojamiento por noche es de    : " + str(self.Calcula_Precio_Noche_Alojamiento()) + " euros")

        print("El viaje cuesta por persona: " + str(self.Precio_Por_Persona()) + ".\n" +
              "De los cuales:\n" + "Alojamiento: " + str(self.Coste_Alojamiento_Por_Persona) +
              "\nTransporte : " + str(self.Coste_Trayecto_Por_Persona) + "\nExcursiones: " +
              str(self.Coste_Excursiones_Por_Persona) + "\nGastos     : " + str(
            (float(self.Duracion) + 1) * float(self.Gastos_Diarios_Por_Persona)))

    def Calcula_Precio_Noche_Alojamiento(self):
        return float(float(self.Coste_Alojamiento_Por_Persona) * float(self.Personas) / float(self.Duracion))

    def Precio_Por_Persona(self):
        return float(self.Coste_Alojamiento_Por_Persona) + float(self.Coste_Trayecto_Por_Persona) + float(
            self.Coste_Excursiones_Por_Persona) + (float(self.Gastos_Diarios_Por_Persona) * (float(self.Duracion) + 1))

    def Calcula_Coste_Alojamiento(self, V_Precio_Noche):
        self.Coste_Alojamiento_Por_Persona = float(V_Precio_Noche) * float(self.Duracion) / float(self.Personas)

    def Calcula_Coste_Trayecto(self):
        if self.Trayecto_Viaje.Transporte == "Coche":
            self.Coches = math.ceil(float(self.Personas) / float(4))
            self.Coste_Trayecto_Por_Persona = float(self.Trayecto_Viaje.Coste) * self.Coches / float(self.Personas)
        else:
            self.Coste_Trayecto_Por_Persona = self.Trayecto_Viaje.Coste

    def Calcula_Viaje(self, V_Lugar, V_Duracion, V_Personas, V_Trayecto, V_Coste_Excursiones, V_Precio_Noche,
                      V_Gastos_Diarios):
        self.Trayecto_Viaje = V_Trayecto
        self.Lugar = V_Lugar
        self.Duracion = V_Duracion
        self.Personas = V_Personas
        self.Gastos_Diarios_Por_Persona = V_Gastos_Diarios
        self.Coste_Excursiones_Por_Persona = V_Coste_Excursiones
        self.Calcula_Coste_Trayecto()
        self.Calcula_Coste_Alojamiento(V_Precio_Noche)

    def Cumple_Requisito(self, Requisito):
        V_Cumple = False
        if (int(self.Duracion) == int(Requisito.Duracion)):
            V_Cumple = self.Precio_Por_Persona() < float(Requisito.Presupuesto)
        return V_Cumple


class C_Lugar_Prohibido:
    Lugar = ""
    Veces = 0

    def __init__(self):
        self.Lugar = ""
        self.Veces = 0

    def Imprimir(self):
        print(self.Lugar + "," + self.Veces)


class C_Requisito:
    Duracion = 0
    Presupuesto = 0

    def __init__(self):
        self.Duracion = 0
        self.Presupuesto = 0

    def Imprimir(self):
        print(str(self.Duracion) + "," + str(self.Presupuesto))


def Imprime_Lista_Viajes(V_Viajes, V_Lugares_Prohibidos):
    V_Personas = 0
    for V_Viaje in V_Viajes:
        V_Viaje.Imprimir()
        print("\n\n")
        V_Personas = Cuantas_Personas_Han_Estado(V_Viaje, V_Lugares_Prohibidos)
        if V_Personas != 0:
            print("En el lugar han estado: " + str(V_Personas) + " personas")
            print("\n")


def Imprime_Lista_Requisitos(V_Requisitos):
    for V_Requisito in V_Requisitos:
        V_Requisito.Imprimir()


def Obtener_Requisitos_Dias(V_Requisitos, V_Duracion):
    V_Requisitos_Dias = []
    for V_Requisito in V_Requisitos:
        if int(V_Requisito.Duracion) == V_Duracion:
            V_Requisitos_Dias.append(V_Requisito)
    return V_Requisitos_Dias


def Media_Presupuesto(V_Requisitos):
    V_Requisito_Media = C_Requisito()
    V_Total = 0
    for V_Requisito in V_Requisitos:
        V_Total = V_Total + int(V_Requisito.Presupuesto)
    V_Requisito_Media.Duracion = V_Requisitos[0].Duracion
    V_Requisito_Media.Presupuesto = V_Total / len(V_Requisitos)
    return V_Requisito_Media


def Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Requisitos):
    V_Viajes_Cumplen_Requisitos = []
    for V_Viaje in V_Viajes:
        # V_Viaje.Imprimir()
        V_Cumple = True
        for V_Requisito in V_Requisitos:
            if not V_Viaje.Cumple_Requisito(V_Requisito):
                V_Cumple = False
        if V_Cumple:
            V_Viajes_Cumplen_Requisitos.append(V_Viaje)
    return V_Viajes_Cumplen_Requisitos


def Cuantas_Personas_Han_Estado (V_Viaje, V_Lugares_Prohibidos):
    V_Personas = 0
    for V_Lugar_Prohibido in V_Lugares_Prohibidos:
        if V_Viaje.Lugar == V_Lugar_Prohibido.Lugar:
            V_Personas = V_Lugar_Prohibido.Veces
    return V_Personas


F_viajes = open('viajes.txt')
F_Lugares = open('lugares_prohibidos.txt')
F_Requisitos = open('requisitos.txt')

V_Viajes = []

outfile = open('resultado.txt', 'w')

# Obtener la lista de viaje
for V_Linea in F_viajes:
    V_Viaje = C_Viaje()
    V_Trayecto = C_Trayecto()
    if not V_Linea.startswith('#') and not V_Linea.startswith('\n'):
        V_Linea_Splitted = V_Linea.rstrip('\n').split(',')

        V_Trayecto.Calcula_Trayecto(V_Linea_Splitted[3], V_Linea_Splitted[2], V_Linea_Splitted[4])

        V_Viaje.Calcula_Viaje(V_Linea_Splitted[0], V_Linea_Splitted[1], V_Linea_Splitted[7], V_Trayecto,
                              V_Linea_Splitted[5], V_Linea_Splitted[6], V_Linea_Splitted[8])

        V_Viajes.append(V_Viaje)  # Obtener la lista de lugares prohibidos

V_Lugares_Prohibidos = []
for V_Linea in F_Lugares:
    V_Lugar_Prohibido = C_Lugar_Prohibido()
    if not V_Linea.startswith('#'):
        V_Linea_Splitted = (V_Linea.rstrip('\n').split(','))
        V_Lugar_Prohibido.Lugar = V_Linea_Splitted[0]
        V_Lugar_Prohibido.Veces = V_Linea_Splitted[1]
        V_Lugares_Prohibidos.append(V_Lugar_Prohibido)

# for V_Lugar_Prohibido in V_Lugares_Prohibidos:
#	V_Lugar_Prohibido.Imprimir()

# Obtener la lista de requisitos
V_Requisitos = []
for V_Linea in F_Requisitos:
    V_Requisito = C_Requisito()
    if not V_Linea.startswith('#'):
        V_Linea_Splitted = (V_Linea.rstrip('\n').split(','))
        V_Requisito.Duracion = V_Linea_Splitted[0]
        V_Requisito.Presupuesto = V_Linea_Splitted[1]
        V_Requisitos.append(V_Requisito)

# Imprime_Lista_Requisitos(V_Requisitos)

V_Requisitos_3_Dias = Obtener_Requisitos_Dias(V_Requisitos, 2)
V_Requisitos_4_Dias = Obtener_Requisitos_Dias(V_Requisitos, 3)

V_Lista_Media_3 = []
V_Lista_Media_3.append(Media_Presupuesto(V_Requisitos_3_Dias))

V_Lista_Media_4 = []
V_Lista_Media_4.append(Media_Presupuesto(V_Requisitos_4_Dias))

V_Viajes_Sin_Lugares_Visitados = []
for V_Viaje in V_Viajes:
    V_Existe = False
    for V_Lugar_Prohibido in V_Lugares_Prohibidos:
        if V_Viaje.Lugar == V_Lugar_Prohibido.Lugar:
            V_Existe = True
    if not V_Existe:
        V_Viajes_Sin_Lugares_Visitados.append(V_Viaje)

print("-----------------------------------------------------------------------------")
print("4 DIAS EN SITIOS QUE NADIE HA ESTADO Y QUE CUMPLEN TODOS LOS REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

print(Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes_Sin_Lugares_Visitados, V_Requisitos_4_Dias),
                           V_Lugares_Prohibidos))

print("-----------------------------------------------------------------------------")
print("4 DIAS EN SITIOS QUE NADIE HA ESTADO Y QUE CUMPLEN MEDIA DE REQUISITOS:")
print("-----------------------------------------------------------------------------")

print("Presupuesto Media: " + str(V_Lista_Media_4[0].Presupuesto) + "\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes_Sin_Lugares_Visitados, V_Lista_Media_4),
                     V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("3 DIAS EN SITIOS QUE NADIE HA ESTADO Y QUE CUMPLEN TODOS LOS REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes_Sin_Lugares_Visitados, V_Requisitos_3_Dias),
                     V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("3 DIAS EN SITIOS QUE NADIE HA ESTADO Y QUE CUMPLEN MEDIA DE REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

print("Presupuesto Media: " + str(V_Lista_Media_3[0].Presupuesto) + "\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes_Sin_Lugares_Visitados, V_Lista_Media_3),
                     V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------\n\n\n\n")
#######################################

print("-----------------------------------------------------------------------------")
print("4 DIAS Y QUE CUMPLEN TODOS LOS REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Requisitos_4_Dias), V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("4 DIAS QUE CUMPLEN MEDIA DE REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

print("Presupuesto Media: " + str(V_Lista_Media_4[0].Presupuesto) + "\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Lista_Media_4), V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("3 DIAS Y QUE CUMPLEN TODOS LOS REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Requisitos_3_Dias), V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("3 DIAS Y QUE CUMPLEN MEDIA DE REQUISITOS:")
print("-----------------------------------------------------------------------------\n\n")

print("Presupuesto Media: " + str(V_Lista_Media_3[0].Presupuesto) + "\n\n")

Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Lista_Media_3), V_Lugares_Prohibidos)

print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------\n\n\n\n")

print("La lista de posibles viajes era:")
print("-----------------------------------------------------------------------------\n")
V_Requisitos_Vacios = []
Imprime_Lista_Viajes(Lista_De_Viajes_Cumple_Requisitos(V_Viajes, V_Requisitos_Vacios), V_Lugares_Prohibidos)
