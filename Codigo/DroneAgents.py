# Equipo Wizards
""" 
Fernanda Diaz Gutierrez |  A01639572
Miguel Angel Barrientos Ballesteros | A01637150
Carlos Iván Armenta Naranjo | A01643070
Jorge Javier Blazquez Gonzalez | A01637706
Gabriel Alvarez Arzate | A01642991
"""

# Ontologia
import random
from owlready2 import *
onto = get_ontology("file://ontology.owl")

# Model design
import agentpy as ap
import numpy as np 

# Visualization
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# Importaciones adicionales para sockets y threading
import socket
import struct
import threading
import json

# Configurar el socket servidor para recibir datos
HOST = 'localhost'
PORT = 8888  # Puerto donde el script de agentes está escuchando

# Variables globales para almacenar el estado
model_data = {
    'isEnemy': None,
    'detDrone': None,
    'detCam': None,
    'isDead': None
}
data_lock = threading.Lock()
data_event = threading.Event()


with onto: 
    class Agent(Thing):
        pass
    class droneAgentOnto(Agent):
        pass
    class guardAgentOnto(Agent):
        pass
    class cameraAgentOnto(Agent):
        pass
    class Target(Thing):
        pass
    class Partner(Agent):
        pass
    class Suspicion(Thing):
        pass
    class Path(Thing):
        pass
    class Enemy(Thing):
        pass
    class has_enemy(FunctionalProperty, ObjectProperty):
        domain = [droneAgentOnto]
        range = [Enemy]
    class has_target(FunctionalProperty, ObjectProperty):
        domain = [droneAgentOnto]
        range = [Target]
    class target_coordinates(FunctionalProperty, DataProperty):
        domain = [Target]
        range = [int]
    class has_suspicion(FunctionalProperty, ObjectProperty):
        domain = [Agent]
        range = [Suspicion]
    class suspicion_bool(FunctionalProperty, DataProperty):
        domain = [Suspicion]
        range = [bool]
    class has_partner(FunctionalProperty, ObjectProperty):
        domain = [Agent]
        range = [Partner]
    class has_id(FunctionalProperty, DataProperty):
        domain = [Agent]
        range = [int]
    class has_path(FunctionalProperty, ObjectProperty):
        domain = [droneAgentOnto]
        range = [Path]
    class path_bool(FunctionalProperty, DataProperty):
        domain = [Path]
        range = [bool]
        
    # Now we save the ontology into the file
    onto.save()



class Message():
    """
    The message class is used to wrap messages and send messages between agents.
    It also contains the environment buffer that stores all messages.
    """
    environment_buffer = [] # The environment buffer
    def __init__(self,sender=None,receiver=None,performative=None,content=None):
        """
        The _init_ function is called when the class is instantiated.
        It sets the sender, receiver, performative and content of the message.
        """
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content
        
    def __str__(self):
        1
        """
        The _str_ function is called when the class is converted to a string.
        It returns a string representation of the message.
        """
        return f"\n\
        Sender: {self.sender}, \n\
        Receiver: {self.receiver}, \n\
        Performative: {self.performative}, \n\
        Content: {self.content}"
    def send(self):
        """
        The send function is used to send a message to the environment buffer.
        """
        Message.environment_buffer.append(self)

class WindAgent(ap.Agent):
    def setup(self):
        self.x = random.randint(-1,1)
        self.y = random.randint(-1,1)
        self.z = random.randint(-1,1)
        self.wind_offset = [self.x,self.y,self.z]


class DroneAgent(ap.Agent):
    """
    State:
     1. patrolling -> looking for suspicion
     2. inspecting -> looking for enemy
     3. end -> Ignoring computer vision (any process between recieving if there was an enemy and the next patrol)


     Notes:
      On state 1. patrolling we will listen to any new changes on the global booleans sent by the comp. vision.
      While on state 2. inspecting, we will pay attention to changes only on isEnemy boolean.
      While on state 2. end, we will ignore any new changes on the global booleans.
    """
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:

                if msg.performative == "vote":
                    self.model.votesInFavor += random.randint(0, 1)
                    Message.environment_buffer.remove(msg)

                if msg.performative == "inspect":
                    self.myself.has_suspicion = onto.Suspicion(suspicion_bool = True) # Si la camara vio al enemigo
                    self.state = 2 # inspecting
                    self.inspect()
                    Message.environment_buffer.remove(msg)

                if msg.performative == "atttack":
                    self.attack()
                    Message.environment_buffer.remove(msg)

                if msg.performative == "shuu":
                    self.shu()
                    Message.environment_buffer.remove(msg)

                

                    
    def see(self):
        # Recibir de vision computacional: sospecha / enemigo
        if self.model.isDead == True:
            msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="isDead", content={"EnemyBool":True})
            self.model.isDead = None

        if(self.myself.has_suspicion.suspicion_bool == False and self.model.detDrone == True): # Aun no hay sospecha y el dron detecto algo raro
            self.myself.has_suspicion = onto.Suspicion(suspicion_bool = True) # hay sospecha
            self.recorded_detections_dron += 1
            self.state = 2 # inspecting
            self.model.detDrone = None
            self.inspect()

        elif(self.myself.has_suspicion.suspicion_bool == True and self.model.isEnemy == True): # Hay sospecha, y el dron confirmo que hay un enemigo
            msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="TrueAlarm", content={"EnemyBool":True})
            self.recorded_detections_utiles += 1
            self.state = 3 # end
            self.model.isEnemy = None
            self.attack()
            msg.send()
            
        elif(self.myself.has_suspicion.suspicion_bool == True and self.model.isEnemy == False): # Hay sospecha, y el dron confirmo que NO hay enemigo            
            msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="FalseAlarm", content={"EnemyBool":False})
            self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False) # hay sospecha

            self.recorded_detections_falsas += 1
            self.state = 3 # end
            self.model.isEnemy = None
            self.patrolling = True
            msg.send()
            # Falsa alarma
            
    def next(self):
        """
        The next function contains the decision making process, where the
        general algorithm of deductive reasoning is executed.
        """
        # For every action in the action list
        for act in self.actions:
        # For every rule in the rule list
            for rule in self.rules:
            # If the action (act) is valid by using the rule (rule)
                if rule(act):
            # return validated action
                    return act
                
    def action(self,act):
        """
        The action function will execute the chosen action (act).
        """
        # If the action exists
        if act is not None:
            act() 

    def step(self):

        """
        The agent's step function
        """
        if self.guard_partner is None:
            self.guard_partner = self.model.guard_agent[0]

        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_detections_dron = 0 # suspicions detected
        self.recorded_detections_utiles = 0 # enemies detected
        self.recorded_detections_falsas = 0 # enemies detected
        self.recorded_patrols = 0

        self.utility = 0
        self.myself = onto.droneAgentOnto(has_id = self.id)
        self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False)

        self.state = None

        self.patrolling = False

        self.guard_partner = None

        self.actions = [self.patrol, self.land] # The action list
        self.rules = [self.rule_patrol, self.rule_land] # The rule list

    def rule_patrol(self,act):
        """
        If there is no suspicion, and patrolling is not true, patrol.
        """
        rule_validation = [False, False, False]
        if self.myself.has_suspicion.suspicion_bool == False:
            rule_validation[0] = True
        if self.patrolling == False:
            rule_validation[1] = True
        if act == self.patrol:
            rule_validation[2] = True
        return all(rule_validation)
    
    def rule_land(self,act):
        """
        If there is no suspicion, and land is not true, patrol.
        """
        
        rule_validation = [False, False, False]
        if self.myself.has_suspicion.suspicion_bool == False:
            print("rule Land sus false")
            rule_validation[0] = True
        if self.patrolling == True:
            rule_validation[1] = True
        if act == self.land:
            rule_validation[2] = True
        return all(rule_validation)

    def patrol(self):
        # The drone starts following the spLine route
        self.model.agent_Actions.append("patrol")
        self.state = 1
        self.recorded_patrols += 1


    def inspect(self):
        # The drone gets out of the spLine and goes to inspect the suspicious zone
        self.model.agent_Actions.append("inspect")


    def attack(self):
        # The drone excecutes the orders sent by the guard
        self.model.agent_Actions.append("attack")
        self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False)
        self.utility += 1
        self.patrolling = True

    def shu(self):
        # The drone excecutes the orders sent by the guard
        self.model.agent_Actions.append("shu")
        self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False)
        self.patrolling = False

    def land(self):
        self.model.agent_Actions.append("land")
        self.patrolling = False
        self.model.detCam = None
        self.model.detDrone = None
        self.model.isEnemy = None


class GuardAgent(ap.Agent):
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:

                if msg.performative == "TrueAlarm":
                    msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="vote", content={"vote":True})
                    msg.send()
                    msg = Message(sender=self.id,receiver=self.camera_partner.id, performative="vote", content={"vote":True})
                    msg.send()
                    self.susObject = True
                    Message.environment_buffer.remove(msg)

                if msg.performative == "FalseAlarm":
                    self.model.agent_Actions.append("falseAlarm")
                    self.susObject = False
                    Message.environment_buffer.remove(msg)

                if msg.performative == "isDead":
                    self.model.agent_Actions.append("alarm")
                    Message.environment_buffer.remove(msg)

                    
    def see(self):
        pass
            
            
    def next(self):
        """
        The next function contains the decision making process, where the
        general algorithm of deductive reasoning is executed.
        """
        # For every action in the action list
        for act in self.actions:
        # For every rule in the rule list
            for rule in self.rules:
            # If the action (act) is valid by using the rule (rule)
                if rule(act):
            # return validated action
                    return act
                
    def action(self,act):
        """
        The action function will execute the chosen action (act).
        """
        # If the action exists
        if act is not None:
            act() 

    def step(self):
        """
        The agent's step function
        """
        if self.drone_partner is None:
            self.drone_partner = self.model.drone_agent[0]

        if self.camera_partner is None:
            self.camera_partner = self.model.camera_agents[0]

        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_attacks = 0 # 
        self.total_enemies = 3 # 
        self.susObject = False
        self.drone_partner = None
        self.camera_partner = None
        self.myself = onto.guardAgentOnto(has_id = self.id)
        

        self.actions = [self.takeControl] # The action list
        self.rules = [self.rule_takeControl] # The rule list

    def rule_takeControl(self, act):
        """
        If there is no suspicion, and land is not true, patrol.
        """
        rule_validation = [False, False]
        if self.susObject == True:
            rule_validation[0] = True
        if act == self.takeControl:
            rule_validation[1] = True
        return all(rule_validation)

    def takeControl(self):
        if self.model.votesInFavor >= 4:
            self.model.votesInFavor += random.randint(0, 1)
            self.model.votesInFavor = 0
            msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="attack", content={"attack":True})
            msg.send()
            self.recorded_attacks += 1
            self.susObject = False
        else:
            msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="shu", content={"shu":True})
            msg.send()
            self.susObject = False

     

class CameraAgent(ap.Agent):
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.performative == "vote":
                self.model.votesInFavor += random.randint(0, 1)
                Message.environment_buffer.remove(msg)

            if msg.receiver == self.id:

                Message.environment_buffer.remove(msg)

            if msg.performative == "CheckAlarm":

                Message.environment_buffer.remove(msg)
                    
    def see(self):
        if self.model.detCam == True:
            self.model.detCam = None
            msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="inspect", content={"suspicion":True})
            msg.send()
            self.recorded_detections_cameras += 1

    def next(self):
        """
        The next function contains the decision making process, where the
        general algorithm of deductive reasoning is executed.
        """
        # For every action in the action list
        for act in self.actions:
        # For every rule in the rule list
            for rule in self.rules:
            # If the action (act) is valid by using the rule (rule)
                if rule(act):
            # return validated action
                    return act
                
    def action(self,act):
        """
        The action function will execute the chosen action (act).
        """
        # If the action exists
        if act is not None:
            act() 

    def step(self):
        """
        The agent's step function
        """
        if self.drone_partner is None:
            self.drone_partner = self.model.drone_agent[0]
        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_detections_cameras = 0 # suspicions detected
        self.drone_partner = None
        self.myself = onto.cameraAgentOnto(has_id = self.id)


        self.actions = [] # The action list
        self.rules = [] # The rule list



# Función para recibir datos desde el socket
def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Agente esperando datos en:', (HOST, PORT))
        while True:
            conn, addr = s.accept()
            print('Conectado por', addr)
            try:
                with conn:
                    # Leer la longitud de los datos entrantes
                    data = conn.recv(4)
                    if not data:
                        continue
                    length = struct.unpack('>I', data)[0]

                    # Leer el JSON
                    json_data = b''
                    while len(json_data) < length:
                        more_data = conn.recv(length - len(json_data))
                        if not more_data:
                            break
                        json_data += more_data

                    received_data = json.loads(json_data.decode('utf-8'))

                    # Actualizar los datos del modelo
                    with data_lock:
                        model_data['isEnemy'] = received_data['isEnemy']
                        model_data['detDrone'] = received_data['detDrone']
                        model_data['detCam'] = received_data['detCam']
                        model_data['isDead'] = received_data['isDead']

                    print("Datos recibidos y actualizados:", model_data)

                    # Señalar que los datos han sido recibidos
                    data_event.set()
            except Exception as e:
                print("Ocurrió un error al recibir datos:", e)
            finally:
                conn.close()
                print('Conexión cerrada con', addr)



# MODELO 
class SecurityModel(ap.Model):
    def setup(self):
        # Instanciamos cada tipo de agente 
        self.drone_agent = ap.AgentList(self, self.p.drone_agent, DroneAgent)
        self.camera_agents = ap.AgentList(self, self.p.camera_agents, CameraAgent)
        self.guard_agent = ap.AgentList(self, self.p.guard_agent, GuardAgent)
        self.wind_agent = ap.AgentList(self, self.p.wind_agent, WindAgent)

        self.currentStep = 0
        self.votesInFavor = 0
        self.agent_Actions = []

        self.detCam = None
        self.detDrone = None
        self.isEnemy = None
        self.lastIsEnemy = self.isEnemy # Only for model step() logic (ignoring new data except on enemy changes)

        self.dCams = [None,True,None,None,None,None,None,True,None,None,None,None,None,True,None,None,None,None]
        self.dDrones = [None,None,None,None,True,None,None,None,None,None,True,None,None,None,None,None,True,None]
        self.isEns = [None,None,False,None,None,True,None,None,False,None,None,True,None,None,False,None,None,True]

        self.isDead = None
        print(self.model.__dict__)  # Muestra todos los atributos del modelo

        self.log_detections_cameras = []  # for detCam plot
        self.log_detections_dron = []    # for detDron plot
        self.log_detections_utiles = []  # for detections_utiles plot
        self.log_detections_falsas = []  # for detections_falsas plot
        self.log_utility = []            # for drone utility plot
        self.log_attacks = []            # for guard attacks plot

    def step(self):
        # Actualizar el estado del modelo con los datos recibidos
        with data_lock:

            if self.drone_agent[0].state == 1:

                if model_data['detDrone'] == 'True':
                    self.detDrone = True
                elif model_data['detDrone'] == 'False':
                    self.detDrone = False
                elif model_data['detDrone'] is None:
                    self.detDrone = None
                if model_data['detCam'] == 'True':
                    self.detCam = True
                elif model_data['detCam'] == 'False':
                    self.detCam = False
                elif model_data['detCam'] is None:
                    self.detCam = None
                if model_data['isEnemy'] == 'True':
                    self.isEnemy = True
                    self.lastIsEnemy = model_data['isEnemy']
                elif model_data['isEnemy'] == 'False':
                    self.isEnemy = False
                    self.lastIsEnemy = model_data['isEnemy']
                elif model_data['isEnemy'] is None:
                    self.isEnemy = None
                    self.lastIsEnemy = model_data['isEnemy']
                if model_data['isDead'] == 'True':
                    self.isDead = True
                elif model_data['isDead'] == 'False':
                    self.isDead = False
                elif model_data['isDead'] is None:
                    self.isDead = None
            
            elif self.drone_agent[0].state == 2 and model_data['isEnemy'] != None:

                if model_data['isEnemy'] == 'True':
                    self.isEnemy = True
                    self.lastIsEnemy = model_data['isEnemy']
                elif model_data['isEnemy'] == 'False':
                    self.isEnemy = False
                    self.lastIsEnemy = model_data['isEnemy']
                elif model_data['isEnemy'] is None:
                    self.isEnemy = None
                    self.lastIsEnemy = model_data['isEnemy']


            # Limpiar los datos recibidos después de procesarlos
            model_data['detDrone'] = None
            model_data['detCam'] = None
            model_data['isEnemy'] = None
            model_data['isDead'] = None
            self.detCam = None
            self.detDrone = None
            self.isEnemy = None
    

        if self.drone_agent[0].state == 1:
            self.detCam = self.dCams[current_step]
            self.detDrone = self.dDrones[current_step]
            self.isEnemy = self.isEns[current_step]
        elif self.drone_agent[0].state == 2:
            self.detCam = self.dCams[current_step]
            self.detDrone = self.dDrones[current_step]
            self.isEnemy = self.isEns[current_step]



        if self.detCam != None:
            print('detCam: ' + str(self.detCam))
        else:
            print('detCam: None')

        if self.detDrone != None:
            print('detDrone: ' + str(self.detDrone))
        else:
            print('detDrone: None')

        if self.isEnemy != None:
            print('isEnemy: ' + str(self.isEnemy))
        else:
            print('isEnemy: None')


        self.camera_agents.step()
        self.drone_agent.step()
        self.guard_agent.step()

        self.log_detections_cameras.append(self.camera_agents[0].recorded_detections_cameras)
        self.log_detections_dron.append(self.drone_agent[0].recorded_detections_dron)
        self.log_detections_utiles.append(self.drone_agent[0].recorded_detections_utiles)
        self.log_detections_falsas.append(self.drone_agent[0].recorded_detections_falsas)
        self.log_utility.append(self.drone_agent[0].utility)
        self.log_attacks.append(self.guard_agent[0].recorded_attacks)

        self.currentStep += 1

    def update(self):
        pass

    def end(self):
        """ self.camera_agents.record('recorded_detections_cameras')
        self.drone_agent.record('recorded_detections_dron')
        self.drone_agent.record('recorded_detections_utiles')
        self.drone_agent.record('recorded_detections_falsas')
        self.drone_agent.record('utility')

        print(self.agent_Actions)

        
        self.guard_agent.record('recorded_attacks','total_enemies')

        # detCam y detDrone a lo largo de los steps
        plt.figure(figsize=(10, 6))
        plt.plot(self.log_detections_dron, label='Drone Detections')
        plt.plot(self.log_detections_cameras, label='Camera Detections')
        plt.xlabel('Sim Step')
        plt.ylabel('Amount of Detections')
        plt.title('Detections Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        # detecciones útiles a lo largo del tiempo
        plt.figure(figsize=(10, 6))
        plt.plot(self.log_detections_utiles, label='Useful Detections', color='green')
        plt.xlabel('Sim Step')
        plt.ylabel('Amount of Useful Detections')
        plt.title('Useful Detections Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        # detecciones falsas a lo largo del tiempo
        plt.figure(figsize=(10, 6))
        plt.plot(self.log_detections_falsas, label='False Detections', color='red')
        plt.xlabel('Sim Step')
        plt.ylabel('Amount of False Detections')
        plt.title('False Detections Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        # utility del dron a lo largo del tiempo 
        plt.figure(figsize=(10, 6))
        plt.plot(self.log_utility, label='Drone Utility', color='purple')
        plt.xlabel('Sim Step')
        plt.ylabel('Utility')
        plt.title('Drone Utility Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        # attacks acumulativos a lo largo del tiempo
        cumulative_attacks = np.cumsum(self.log_attacks)
        plt.figure(figsize=(10, 6))
        plt.plot(cumulative_attacks, label='Cumulative Attacks', color='orange')
        plt.xlabel('Sim Step')
        plt.ylabel('Amount of Attacks')
        plt.title('Cumulative Attacks Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        # detecciones acumulativas a lo largo del tiempo
        cumulative_dron = np.cumsum(self.log_detections_dron)
        cumulative_camera = np.cumsum(self.log_detections_cameras)

        plt.figure(figsize=(10, 6))
        plt.plot(cumulative_dron, label='Cumulative Drone Detections')
        plt.plot(cumulative_camera, label='Cumulative Camera Detections')
        plt.xlabel('Sim Step')
        plt.ylabel('Cumulative Detections')
        plt.title('Cumulative Detections Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

        for elem in self.agent_Actions:
            print(elem + ", ")

        eficienciaCam = 0
        precision = 0

        if self.drone_agent[0].recorded_detections_dron != 0 and self.camera_agents[0].recorded_detections_cameras != 0:
            eficienciaCam = ((self.camera_agents[0].recorded_detections_cameras) / (self.drone_agent[0].recorded_detections_dron + self.camera_agents[0].recorded_detections_cameras))*100
        
        if self.drone_agent[0].recorded_detections_dron != 0:
            precision = self.drone_agent[0].recorded_detections_utiles / self.drone_agent[0].recorded_detections_dron
        utility = self.drone_agent[0].utility

        plt.figure(figsize=(10, 6))
        metrics = ['Camera Efficiency', 'Drone Precision']
        values = [eficienciaCam, precision * 100]
        plt.bar(metrics, values, color=['blue', 'orange'])
        plt.ylabel('Percentage')
        plt.title('Performance Metrics')
        plt.grid(axis='y')
        plt.show()

        # Print final metrics
        utility = self.drone_agent[0].utility
        alarmRate = self.guard_agent[0].recorded_attacks / self.guard_agent[0].total_enemies

        print('Final Metrics:')
        print(f'Efficiency (Camera): {eficienciaCam:.2f}%')
        print(f'Precision (Drone): {precision:.2f}')
        print(f'Utility (Drone): {utility}')
        print(f'False Alarms Rate (Guard): {alarmRate:.2f}')


        print('eficienciaCam = ' + str(eficienciaCam))
        print('precision = ' + str(precision))
        print('utility = ' + str(utility))
        print('falseAlarm = ' + str(falseAlarms))
        eficiencia = self.drone_agent[0].recorded_detections_dron / recorded_patrols """
    

parameters = {
    'wind_agent': 1,
    'camera_agents': 1,
    'drone_agent': 1,
    'guard_agent': 1,
    'steps': 18
}


if __name__ == "__main__":
    data_thread = threading.Thread(target=receive_data)
    data_thread.daemon = True  
    data_thread.start()

    model = SecurityModel(parameters)
    model.setup()

    max_steps = 100
    current_step = 0

    print("Modelo de seguridad iniciado. Esperando datos...")
    while current_step < max_steps:
        data_event.wait()
        data_event.clear()
        model.step()
        model.update()
        current_step += 1

    model.end()