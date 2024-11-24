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
    class target_coordinates(FunctionalProperty, ObjectProperty):
        domain = [Target]
        range = [list]
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

