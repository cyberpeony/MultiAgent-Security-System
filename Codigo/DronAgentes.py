# Equipo Wizards
""" 
Fernanda Diaz Gutierrez |  A01639572
Miguel Angel Barrientos Ballesteros | A01637150
Carlos Iván Armenta Naranjo | A01643070
Jorge Javier Blazquez Gonzalez | A01637706
Gabriel Alvarez Arzate | A01642991
"""

# Ontologia
from owlready2 import *
onto = get_ontology("file://ontology.owl")

# Model design
import agentpy as ap
import numpy as np 

# Visualization
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class Message():
    """
    The message class is used to wrap messages and send messages between agents.
    It also contains the environment buffer that stores all messages.
    """
    environment_buffer = [] # The environment buffer
    def __init__(self,sender=None,receiver=None,performative=None,content=None):
        """
        The __init__ function is called when the class is instantiated.
        It sets the sender, receiver, performative and content of the message.
        """
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content
    def __str__(self):
        1
        """
        The __str__ function is called when the class is converted to a string.
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


class DroneAgent(ap.Agent):
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:
                if msg.performative == "inspect":
                    self.myself.has_suspicion = onto.Suspicion(suspicion_bool = True) # Si la camara vio al enemigo
                    self.inspect()
                    Message.environment_buffer.remove(msg)

                if msg.performative == "attack":
                    self.Attack()
                    Message.environment_buffer.remove(msg)

                    
    def see(self):
        # Recibir de vision computacional: sospecha / enemigo
        if(self.myself.has_suspicion.suspicion_bool == False and self.model.droneSawSomething == True): # Aun no hay sospecha y el dron detecto algo raro
            self.myself.has_suspicion = onto.Suspicion(suspicion_bool = True) # hay sospecha
            self.droneSawSomething = None
            self.inspect()
        elif(self.myself.has_suspicion.suspicion_bool == True and self.model.droneSawEnemy == True): # Hay sospecha, y el dron confirmo que hay un enemigo
            # self.myself.has_suspicion = onto.Suspicion(suspicion_bool = True) # si el dron vio al enemigo
            msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="CheckAlarm", content={"enemyBool":True})
            self.model.droneSawEnemy = None
            msg.send()
            
        elif(self.myself.has_suspicion.suspicion_bool == True and self.model.droneSawEnemy == False): # Hay sospecha, y el dron confirmo que NO hay enemigo            
            msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="CheckAlarm", content={"enemyBool":False})
            self.model.droneSawEnemy = None
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
        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_detections = 0 # suspicions detected
        self.recorded_patrols = 0 # each time the drone lands
        self.utility = 0
            
        self.myself = onto.droneAgentOnto(has_id = self.id)
        self.myself.has_path = onto.Path(path_bool = True)
        self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False)
        self.myself.has_target = onto.Target(target_coordinates = None)
        self.land = False

        self.guard_partner = self.model.guard_agent[0]
        self.camera0_partner = self.model.camera_agents[0]
        self.camera1_partner = self.model.camera_agents[1]
        self.camera2_partner = self.model.camera_agents[2]
        self.camera3_partner = self.model.camera_agents[3]
        self.camera4_partner = self.model.camera_agents[4]
        self.camera5_partner = self.model.camera_agents[5]
        self.camera6_partner = self.model.camera_agents[6]

        self.actions = [self.patrol, self.land] # The action list
        self.rules = [self.rule_patrol, self.rule_land] # The rule list

    def rule_patrol(self,act):
        """
        If there is no suspicion, and land is not true, patrol.
        """
        rule_validation = [False, False, False]
        if self.myself.has_suspicion.suspicion_bool == False:
            rule_validation[0] = True
        if self.land == False:
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
            rule_validation[0] = True
        if self.land == True:
            rule_validation[1] = True
        if act == self.land:
            rule_validation[2] = True
        return all(rule_validation)
    
    def rule_patrol(self,act):
        pass

    def patrol(self):
        # The drone starts following the spLine route
        self.model.droneAgent_actions.append("patrol")

    def land(self):
        # The drone returns to 0,0 and lands on the platform
        self.model.droneAgent_actions.append("land")

    def inspect(self):
        # The drone gets out of the spLine and goes to inspect the suspicious zone
        self.model.droneAgent_actions.append("inspect")
        msg = Message(sender=self.id,receiver=self.guard_partner.id, performative="SoundAlarm", content={"suspicion":True})
        msg.send()

    def Attack(self):
        # The drone excecutes the orders sent by the guard
        self.model.droneAgent_actions.append("attack")
        self.myself.has_suspicion = onto.Suspicion(suspicion_bool = False)
        self.land = True


class GuardAgent(ap.Agent):
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:
                if msg.performative == "SoundAlarm":
                    self.soundAlarm()
                    Message.environment_buffer.remove(msg)

                if msg.performative == "CheckAlarm":
                    self.enemy = msg.content["enemyBool"]  
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
        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_attacks = 0 # suspicions detected
        self.utility = 0
        self.enemy = False

        self.actions = [self.takeControl] # The action list
        self.rules = [self.rule_takeControl] # The rule list

    def rule_takeControl(self, act):
        """
        If there is no suspicion, and land is not true, patrol.
        """
        rule_validation = [False, False]
        if self.enemy == True:
            rule_validation[0] = True
        if act == self.takeControl:
            rule_validation[1] = True
        return all(rule_validation)

    def soundAlarm(self):
        self.mode.guardAgent_actions.append("SoundAlarm")

    def takeControl(self, enemy):
        if(enemy == True):
            self.mode.guardAgent_actions.append("TrueAlarm")
            msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="attack", content={"attack":True})
            msg.send()
        else:
            self.mode.guardAgent_actions.append("FalseAlarm")


class CameraAgent(ap.Agent):
    def take_msg(self):
        """
        The take_msg function will interpret incoming messages.
        If there is a message for this agent, it will update its beliefs
        about its own wealth, based on the message content.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:

                Message.environment_buffer.remove(msg)

            if msg.performative == "CheckAlarm":

                Message.environment_buffer.remove(msg)

                    
    def see(self):
        if self.model.cameraSawSomething == True:
            self.model.cameraSawSomething = None
            msg = Message(sender=self.id,receiver=self.drone_partner.id, performative="inspect", content={"suspicion":True})
            msg.send()
            self.recorded_detections += 1

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
        self.take_msg()

        self.see() # Perception function
        
        a = self.next() # next function (return chosen action (a))
        self.action(a) # action function (executes action (a))

    def setup(self):
        self.recorded_detections = 0 # suspicions detected
        self.utility = 0
        self.enemy = False

        self.actions = [] # The action list
        self.rules = [] # The rule list


class SecurityModel(ap.Model):
    def setup(self):
        # Instanciamos cada tipo de agente 
        self.camera_agents = ap.AgentList(self, self.p.camera_agents, CameraAgent)
        self.drone_agent = ap.AgentList(self, self.p.drone_agent, DroneAgent)
        self.guard_agent = ap.AgentList(self, self.p.guard_agent, GuardAgent)

        self.droneAgent_actions = []
        self.guardAgent_actions = []
        #self.camera_actions = []

        self.cameraSawSomething = None
        self.droneSawSomething = None
        self.droneSawEnemy = None
        
    def step(self):
        self.camera_agents.step()
        self.drone_agents.step()
        self.guard_agent.step()

    def update(self):
        pass

    def end(self):
        self.camera_agents.record('recorded_detections', 'utility')
        self.drone_agents.record('recorded_detections', 'recorded_patrols', 'utility')
        self.guard_agents.record('recorded_attacks','utility')