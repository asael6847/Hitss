# src/actors/actor.py

# ... tus importaciones existentes ...

class Actor:
    def __init__(self, name):
        self.name = name
        self.abilities = {}

    def who_can(self, ability):
        self.abilities[type(ability)] = ability
        return self

    def can(self, ability):
        self.abilities[type(ability)] = ability
        return self

    def ability_to(self, ability_type):
        return self.abilities.get(ability_type)

    # Modifica attempts_to para aceptar **kwargs (keyword arguments)
    # y pasarlos a la interacción.
    def attempts_to(self, *tasks_or_interactions, **kwargs): # <--- CAMBIO CLAVE AQUÍ
        for item in tasks_or_interactions:
            # Pasa todos los kwargs recibidos al perform_as del item (Tarea/Interacción)
            # Esto permitirá que 'request' se pase si existe en kwargs.
            item.perform_as(self, **kwargs) # <--- CAMBIO CLAVE AQUÍ

    # ... otros métodos del Actor ...