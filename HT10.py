# Hoja de trabajo 10
# Rodrigo Urrutia 16139
# Solo yo trabaje en esto

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

gdb = GraphDatabase("http://localhost:7474/", username="neo4j", password="12345")
doctores = gdb.labels.create("Doctores")
pacientes = gdb.labels.create("Pacientes")
medicinas = gdb.labels.create("Medicinas")

#Menu
opcion = 0
while opcion != "8":
    print(" 1. Ingresar doctor\n 2. Ingresar paciente\n 3. Visita medica\n 4. Consultar especialidad de doctor\n 5. Ingresar que una persona conoce a otra\n 6. Recomendacion para paciente que busca doctor\n 7. Recomendacion de un doctor a su paciente\n 8. Salir")
    opcion = input("Ingresar numero de opcion\n")

    if(opcion == "1"):
        nombre = input("Nombre: \n")
        colegiado = input("Colegiado: \n")
        especialidad = input("Especialidad: \n")
        telefono = input("Telefono: \n")
        doctor = gdb.nodes.create(Nombre = nombre, Colegiado = colegiado, Especialidad = especialidad, Telefono = telefono)
        doctores.add(doctor)
        print("Se ha ingresado un nuevo doctor\n")

    if(opcion == "2"):
        nombre = input("Nombre: \n")
        telefono = input("Telefono: \n")
        paciente = gdb.nodes.create(Nombre = nombre, Telefono = telefono)
        pacientes.add(paciente)
        print("Se ha ingresado un nuevo paciente\n")

    if(opcion == "3"):
        colegiado1 = input("Numero de colegiado del doctor: \n")
        telefono2 = input("Nombre de telefono del paciente: \n")
        q1 = 'MATCH (d:Doctores) WHERE d.Colegiado="'+colegiado1+'" RETURN d'
        q1Node = gdb.query(q1, returns = (client.Node))
        q2 = 'MATCH (p:Pacientes) WHERE p.Telefono="'+telefono2+'" RETURN p'
        q2Node = gdb.query(q2, returns = (client.Node))
        #print(type(q2Node))
        for r in q1Node:
            for i in q2Node:
                #print(type(r[0]))
                r[0].relationships.create("conoce", i[0])
                i[0].relationships.create("conoce", r[0])

        nombre = input("Nombre de la medicina: \n")
        desdeFecha = input("Tomar desde (Fecha): \n")
        hastaFecha = input("Tomar hasta (Fecha): \n")
        dosis = input("Dosis: \n")
        medicina = gdb.nodes.create(Nombre = nombre, DesdeFecha = desdeFecha, HastaFecha = hastaFecha, Dosis = dosis)
        medicinas.add(medicina)
        print("Se ha ingresado una prescripcion\n")
        for r in q1Node:
            r[0].relationships.create("prescribes", medicina)
        for i in q2Node:
            i[0].relationships.create("takes", medicina)

    if(opcion == "4"):
        espe = input("Especialidad a buscar: \n")
        q =  'MATCH (d:Doctores) WHERE d.Especialidad="'+espe+'" RETURN d'
        qNode = gdb.query(q, returns=(client.Node))
        for r in qNode:
            print(("Nombre: %s " % (r[0]["Nombre"])) + "| " + ("Colegiado: %s" % (r[0]["Colegiado"])) + "| " + ("Telefono: %s" % (r[0]["Telefono"])))

    if(opcion == "5"):
        print("Puede ingresar la informacion correspondiente de un doctor o de un paciente")
        num1 = input("Numero de colegiado del doctor o telefono del paciente: \n")
        num2 = input("Nombre de colegiado del doctor o telefono del paciente: \n")
        q1 = 'MATCH (d:Doctores) WHERE d.Colegiado="'+num1+'" RETURN d'
        q1Node = gdb.query(q1, returns = (client.Node))
        q2 = 'MATCH (p:Pacientes) WHERE p.Telefono="'+num1+'" RETURN p'
        q2Node = gdb.query(q2, returns = (client.Node))
        q3 = 'MATCH (d:Doctores) WHERE d.Colegiado="'+num2+'" RETURN d'
        q3Node = gdb.query(q3, returns = (client.Node))
        q4 = 'MATCH (p:Pacientes) WHERE p.Telefono="'+num2+'" RETURN p'
        q4Node = gdb.query(q4, returns = (client.Node))

        if len(q1Node)==0:
            if len(q3Node)==0:
                # Paciente-Paciente
                for r in q2Node:
                    for i in q4Node:
                        r[0].relationships.create("conoce", i[0])
                        i[0].relationships.create("conoce", r[0])
            else:
                # Paciente-Doctor
                for r in q2Node:
                    for i in q3Node:
                        r[0].relationships.create("conoce", i[0])
                        i[0].relationships.create("conoce", r[0])
        else:
            if len(q3Node)==0:
                # Doctor-Paciente
                for r in q1Node:
                    for i in q4Node:
                        r[0].relationships.create("conoce", i[0])
                        i[0].relationships.create("conoce", r[0])
            else:
                # Doctor-Doctor
                for r in q1Node:
                    for i in q3Node:
                        r[0].relationships.create("conoce", i[0])
                        i[0].relationships.create("conoce", r[0])
        

    if(opcion == "6"):
        telefono1 = input("Ingrese el telefono del paciente que busca la recomendacion: \n")
        espe = input("Especialidad a buscar: \n")

        q1= 'MATCH(p:Pacientes {Telefono:"'+telefono1+'"})-[:conoce]->(c:Pacientes)-[:conoce]->(d:Doctores) WHERE d.Especialidad="'+espe+'" RETURN d'
        q1Node = gdb.query(q1, returns = (client.Node))

        if len(q1Node)!=0:
            for r in q1Node:
                print(("Doctor de un conocido recomendado - Nombre: %s " % (r[0]["Nombre"])) + "| " + ("Colegiado: %s" % (r[0]["Colegiado"])) + "| " + ("Telefono: %s" % (r[0]["Telefono"])))

        q2 = 'MATCH(p:Pacientes {Telefono:"'+telefono1+'"})-[:conoce]->(c:Pacientes)-[:conoce]->(e:Pacientes)-[:conoce]->(d:Doctores) WHERE d.Especialidad="'+espe+'" RETURN d'
        q2Node = gdb.query(q2, returns = (client.Node))
        
        if len(q2Node)!=0:
            for r in q2Node:
                print(("Doctor de un conocido del conocido recomendado - Nombre: %s " % (r[0]["Nombre"])) + "| " + ("Colegiado: %s" % (r[0]["Colegiado"])) + "| " + ("Telefono: %s" % (r[0]["Telefono"])))


    if(opcion == "7"):
        colegiado1 = input("Ingrese el numero de colegiado del doctor que quiere recomendar a su paciente: \n")
        espe = input("Especialidad a buscar: \n")

        q1= 'MATCH(p:Doctores {Colegiado:"'+colegiado1+'"})-[:conoce]->(d:Doctores) WHERE d.Especialidad="'+espe+'" RETURN d'
        q1Node = gdb.query(q1, returns = (client.Node))

        if len(q1Node)!=0:
            for r in q1Node:
                print(("Doctor conocido recomendado - Nombre: %s " % (r[0]["Nombre"])) + "| " + ("Colegiado: %s" % (r[0]["Colegiado"])) + "| " + ("Telefono: %s" % (r[0]["Telefono"])))

        q2 = 'MATCH(p:Doctores {Colegiado:"'+colegiado1+'"})-[:conoce]->(e:Doctores)-[:conoce]->(d:Doctores) WHERE d.Especialidad="'+espe+'" RETURN d'
        q2Node = gdb.query(q2, returns = (client.Node))
        
        if len(q2Node)!=0:
            for r in q2Node:
                print(("Doctor conocido de un conocido recomendado - Nombre: %s " % (r[0]["Nombre"])) + "| " + ("Colegiado: %s" % (r[0]["Colegiado"])) + "| " + ("Telefono: %s" % (r[0]["Telefono"])))


    if(opcion == "8"):
        print("Usted ha salido del programa")
        
