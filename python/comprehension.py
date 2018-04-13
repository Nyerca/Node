# Le comprehension sono uno strumento che ci permette di creare in modo conciso e conveniente 
# nuove liste, set, e dizionari partendo da una sequenza di valori esistenti.

# list comprehension che crea una lista di quadrati
squares = [x**2 for x in range(10) if x%2 == 0]
print(squares);

# set comprehension che crea un set di cubi
{x**3 for x in range(10)}

# dict comprehension che mappa lettere lowercase all'equivalente uppercase
{c: c.upper() for c in 'abcde'}


################## Simili ai comprehension

# map(func, seq): applica la funzione func a tutti gli elementi di seq e ritorna un nuovo iterabile;
# filter(func, seq): ritorna un iterabile che contiene tutti gli elementi di seq per cui func(elem) è true.