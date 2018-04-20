def is_even(n): #Funzione con documentazione:
    """Return True if n is even, False otherwise."""
    if n%2 == 0:
        return True
    else:
        return False

help(is_even);
print(is_even(4));

def calc_rect_area(width, height):
    """Return the area of the rectangle."""
    return width * height
	
# Passare argomenti
print(calc_rect_area(3, 5));
print(calc_rect_area(width=3, height=5));

# Ponendo una * di fronte all’argomento durante la chiamata, ogni elemento della sequenza viene passato 
# separatamente e associato al parametro corrispondente della funzione
size = (3, 5)
print(calc_rect_area(*size));

# dizionario, che richiede due ** di fronte all’argomento durante la 
# chiamata per poter associare ogni elemento al parametro corrispondente
size = {'width': 3, 'height': 5}
print(calc_rect_area(**size));


########################## Definizione di parametri
def say_hello():
    print('Hello World!')

say_hello()

def say_hello_to(name="Master"): #Valore di default
	print("Hello {}!".format(name));
	
say_hello_to("Enrico")
say_hello_to(name='Python')


# Tutti gli argomenti che appaiono dopo la *, dovranno essere passati per nome.
def greet(greeting, *, name):
    print('{} {}!'.format(greeting, name))
greet('Hello', name='Python')

# Permette alla funzione di accettare un numero variabile di argomenti posizionali.
def write_them(*names):
    print('Hello {}!'.format(', '.join(names)))
	
write_them('Python', 'PyPy', 'Jython', 'IronPython')


######################## Ritorno di valori
def square(n):
    return n**2
x = square(5)
print(x);


def print_twice(text):
    if not text:
        # termina immediatamente se text è una stringa vuota
        return
    print(text)
    print(text)
    # ritorna None automaticamente al termine della funzione

	
def midpoint(x1, y1, x2, y2):
    """Return the midpoint between (x1; y1) and (x2; y2)."""
    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2
    return xm, ym

x, y = midpoint(2, 4, 8, 12)
print(x);