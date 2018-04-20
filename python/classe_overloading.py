class Person:
    # definiamo un __init__ che assegna nome e cognome all'istanza
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    # definiamo un metodo "eat" che stampa un messaggio
    def eat(self, food):
        print(self.name, 'is eating', food)
    # definiamo un metodo "sleep" che stampa un messaggio
    def sleep(self):
        print(self.name, 'is sleeping')
	# definiamo uno __str__ che restituisce nome e cognome
    def __str__(self):
        return '{} {}'.format(self.name, self.surname)
    # definiamo uno __repr__ che restituisce il tipo dell'istanza
    def __repr__(self):
        return '<Person object ({} {})>'.format(self.name, self.surname)

class Team:
    # definiamo un __init__ che assegna i membri all'istanza
    def __init__(self, members):
        self.members = members
    # definiamo un __repr__ che restituisce il tipo dell'oggetto
    # e i nomi dei membri del team
    def __repr__(self):
        names = ', '.join([p.name for p in self.members])
        return '<Team object [{}]>'.format(names)
    # definiamo un __contains__ che restituisce True se un membro
    # fa parte del team, altrimenti False
    def __contains__(self, other):
        return other in self.members
    # definiamo un __add__ che restituisce un nuovo team creato
    # dall'aggiunta di una nuova persona o dall'unione di 2 team
    def __add__(self, other):
        if isinstance(other, Person):
            return Team(self.members + [other])
        elif isinstance(other, Team):
            return Team(self.members + other.members)
        else:
            raise TypeError("Can't add Team with {!r}.".format(other))
    # definiamo un __radd__ che è uguale ad __add__, visto che
    # l'addizione è un'operazione commutativa
    __radd__ = __add__
    # definiamo un __iadd__ che modifica il team aggiungendo una
    # nuova persona o i membri di un altro team al team corrente
    def __iadd__(self, other):
        if isinstance(other, Person):
            self.members.append(other)
            return self
        elif isinstance(other, Team):
            self.members.extend(other.members)
            return self
        else:
            raise TypeError("Can't add {!r} to the team.".format(other))



guido = Person('Guido', 'van Rossum')
tim = Person('Tim', 'Peters')
alex = Person('Alex', 'Martelli')
ezio = Person('Ezio', 'Melotti')

# creiamo 2 team da 2 persone per team
t1 = Team([guido, tim])
t2 = Team([alex, ezio])

print(guido in t1);
t1 + ezio;
print(repr(t1));
t1 += ezio;
print(repr(t1));