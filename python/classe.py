class Rectangle:
    scientific_name = 'Figura geometrica con 3 lati'
    def __init__(self, base, height):
        """Initialize the base and height attributes."""
        self.base = base
        self.height = height
    def calc_area(self):
        """Calculate and return the area of the rectangle."""
        return self.base * self.height
    def calc_perimeter(self):
        """Calculate and return the perimeter of a rectangle."""
        return (self.base + self.height) * 2
		
myrect = Rectangle(3, 5)
print(myrect.base);
print(myrect.calc_area());


from random import randrange
# creiamo una lista di 100 istanze di Rectangle con valori casuali
rects = [Rectangle(randrange(100), randrange(100)) for x in range(100)]
# iteriamo la lista di rettangoli e printiamo
# base, altezza, area, perimetro di ogni rettangolo
for rect in rects:
    print('Rect:', rect.base, rect.height)
    print('  Area:', rect.calc_area())
    print('  Perimeter:', rect.calc_perimeter())
	
	
	
########################### Attributi
# Esistono 2 tipi di attributi:
# Attributi di istanza; --> self.base = base
# Attributi di classe. --> scientific_name = 'Figura geometrica con 3 lati'
Rectangle.scientific_surname = 'Canis lupus lupus'
print(Rectangle.scientific_surname);
print(rects[0].scientific_surname);
print(Rectangle.scientific_name);
print(rects[0].scientific_name);


################### Ereditarietà
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
		
		
class Employee(Person):
    # definiamo un nuovo __init__ che accetta nome/cognome/lavoro
    def __init__(self, name, surname, job):
        # chiamiamo l'__init__ della classe base (o superclasse)
        # che assegna nome e cognome all'istanza
        super().__init__(name, surname)
        # assegniamo il lavoro all'istanza
        self.job = job
    # definiamo un metodo aggiuntivo che stampa un messaggio
    def work(self):
        print(self.name, 'is working as a', self.job)
		
e = Employee('Ezio', 'Melotti', 'developer')
p = Person('Ezio', 'Melotti')
print(e.name);
print(p.name);
e.eat('pizza')

# l'interprete stampa automaticamente il repr() dell'oggetto
# e il metodo p.__repr__() viene invocato
print(repr(p))
# se usiamo str(), print(), o format(), p.__str__() viene chiamato
# automaticamente e il nome completo viene restituito
print(str(p))