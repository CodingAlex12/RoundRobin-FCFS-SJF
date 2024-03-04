class Simulacion:
    def __init__(self):
        self.num_procesos = self.obtener_numero_procesos()
        self.quantum = self.obtener_numero_quantum()
        self.nombres_procesos = []
        self.rafagas_cpu = {}
        self.lineadeltiempo = []
        self.cambios_de_contexto = 0

        for i in range(self.num_procesos):
            nombre = input(f"Ingrese el nombre del proceso {i + 1}: ")
            self.nombres_procesos.append(nombre)

    def obtener_numero_procesos(self):
        while True:
            try:
                num_procesos = int(input("Ingrese el número de procesos (entre 1 y 5): "))
                if 1 <= num_procesos <= 5:
                    return num_procesos
                else:
                    print("Error: El número de procesos debe estar entre 1 y 5.")
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")

    def obtener_numero_quantum(self):
        while True:
            try:
                num_quantum = int(input("Ingrese el número de quantum (entre 2, 3 u 4): "))
                if 2 <= num_quantum <= 4:
                    return num_quantum
                else:
                    print("Error: El número de quantum debe estar entre 2 y 4.")
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")

    def iniciar_simulacion(self):
        print("Simulación iniciada con", self.num_procesos, "procesos.")
        print("Quantum asignado:", self.quantum)
        while True:
            try:
                algoritmo_empleado = int(input("Ingrese el número de algoritmo que desee usar: \n1. RR\t 2.FCFS \t 3. SJF "))
                if 1 <= algoritmo_empleado <= 3:
                    if algoritmo_empleado == 1:
                        print('Algoritmo seleccionado : RR')
                        self.RR()
                        return
                    elif algoritmo_empleado == 2:
                        print('Algoritmo seleccionado : FCFS')
                        self.FCFS()
                        return
                    elif algoritmo_empleado == 3:
                        print('Algoritmo seleccionado : SJF')
                        self.SJF()
                        return
                else:
                    print("Error: El número de algoritmo debe estar entre 1 y 3.")
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")

    def RR(self):
        self.tiempo_finalizacion = {}
        self.tiempo_espera = {}  
        for i in range(self.num_procesos):
            rafaga = int(input(f"Ingrese la ráfaga de CPU para el proceso '{self.nombres_procesos[i]}': "))
            self.tiempo_espera[self.nombres_procesos[i]] = 0  
            self.rafagas_cpu[self.nombres_procesos[i]] = rafaga
            self.tiempo_finalizacion[self.nombres_procesos[i]] = 0  

        ciclos=0

        while any(valor != 0 for valor in self.rafagas_cpu.values()):
            for proceso in list(self.rafagas_cpu.keys()):  
                if self.rafagas_cpu[proceso] != 0:
                    self.lineadeltiempo.append(proceso)
                    self.cambios_de_contexto += 1

                if self.rafagas_cpu[proceso] <= self.quantum:
                    self.tiempo_espera[proceso] += self.rafagas_cpu[proceso]
                    self.tiempo_finalizacion[proceso] = sum(self.tiempo_espera.values())
                else:
                    self.tiempo_espera[proceso] += self.quantum
                        
                nuevo_valor = self.rafagas_cpu[proceso] - self.quantum
                self.rafagas_cpu[proceso] = max(0, nuevo_valor)
            ciclos+=1
        print("Línea de tiempo:", self.lineadeltiempo)
        print("Número de cambios de contexto:", self.cambios_de_contexto)
        print('Número de Ciclos: ', ciclos)
        print('Número de finalización: ', self.tiempo_finalizacion)
        promedio_finalizacion = sum(self.tiempo_finalizacion.values()) / self.num_procesos
        print(f"Promedio de tiempo de finalización: {promedio_finalizacion}")

    def SJF(self):
        ciclos=0
        cambios_cotexto=0
        procesos = []
        for i in range(self.num_procesos):
            tiempo_llegada = int(input(f"Ingrese el tiempo de llegada para el proceso {self.nombres_procesos[i]}: "))
            tiempo_ejecucion = int(input(f"Ingrese el tiempo de ejecución para el proceso {self.nombres_procesos[i]}: "))
            procesos.append((self.nombres_procesos[i], tiempo_llegada, tiempo_ejecucion))
        self.procesos = procesos
        sorted_processes = sorted(procesos, key=lambda x: x[2])
        current_time = 0
        total_waiting_time = 0
        n = len(sorted_processes)

        print("Proceso\tTiempo de Llegada\tTiempo de Ejecución\tTiempo de Espera")

        for i in range(n):
            process_id, arrival_time, execution_time = sorted_processes[i]
            current_time = max(current_time, arrival_time)
            waiting_time = current_time - arrival_time
            total_waiting_time += waiting_time
            print(f"{process_id}\t{arrival_time}\t\t\t{execution_time}\t\t\t{waiting_time}")
            current_time += execution_time
            ciclos+=1
            cambios_cotexto += 1

        average_waiting_time = total_waiting_time / n
        print(f"\nTiempo de espera promedio: {average_waiting_time}")
        print('Número de Cíclos;',ciclos)
        print('Número de cambios de Contexto;',cambios_cotexto)
        self.imprimir_linea_tiempo()
    
    def imprimir_linea_tiempo(self):
        events = []
        current_time = 0

        for proceso in self.procesos:
            process_id, arrival_time, execution_time = proceso
            events.append((arrival_time, 'Llegada', process_id))
            events.append((arrival_time + execution_time, 'Terminado', process_id))

        events.sort()

        print("\nLínea de Tiempo:")
        print("Tiempo: ", end="\t")
        for event_time, _, _ in events:
            print(event_time, end="\t")
        print()  

        print("Proceso: ", end="\t")
        for _, _, process_id in events:
            print(process_id, end="\t")
        print()  

    def FCFS(self):
        procesos = []
        for i in range(self.num_procesos):
            tiempo_llegada = int(input(f"Ingrese el tiempo de llegada para el proceso {self.nombres_procesos[i]}: "))
            tiempo_ejecucion = int(input(f"Ingrese el tiempo de ejecución para el proceso {self.nombres_procesos[i]}: "))
            procesos.append((self.nombres_procesos[i], tiempo_llegada, tiempo_ejecucion))
        self.procesos = procesos

        sorted_processes = sorted(procesos, key=lambda x: x[1])

        current_time = 0
        total_waiting_time = 0
        n = len(sorted_processes)

        print("Proceso\tTiempo de Llegada\tTiempo de Ejecución\tTiempo de Espera")

        for i in range(n):
            process_id, arrival_time, execution_time = sorted_processes[i]
            current_time = max(current_time, arrival_time)
            waiting_time = current_time - arrival_time
            total_waiting_time += waiting_time
            print(f"{process_id}\t{arrival_time}\t\t\t{execution_time}\t\t\t{waiting_time}")
            current_time += execution_time

        average_waiting_time = total_waiting_time / n
        print(f"\nTiempo de espera promedio: {average_waiting_time}")
        
        self.imprimir_linea_tiempo()

# Crear una instancia de la clase Simulacion
simulacion = Simulacion()

# Iniciar la simulación
simulacion.iniciar_simulacion()
