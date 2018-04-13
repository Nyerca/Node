d = {20: ['Jack', 'Jane'], 28: ['John', 'Mary']}  # int come chiavi, list come valori
print(d);
e = {(0, 10): 'primo intervallo'}; # le tuple sono hashabili
print(e);

letters = {'a': 1, 'b': 2, 'c': 3};
letters2 = {'k': 180};
print(letters['a']);
print('x' not in letters);  # la chiave 'x' non è presente in d

letters['d'] = 4;
print(letters);

print("Items");
print(letters.items());
print(letters.keys());
print(letters.values());
print(letters.get('a', 0)); #Restituisce il valore corrispondente a chiave se presente, altrimenti il valore di default
print(letters.pop('a', 0)); #Rimuove e restituisce il valore corrispondente a chiave se presente, altrimenti il valore di default
print(letters.popitem()); #Rimuove e restituisce un elemento arbitrario da d

letters.update(letters2); #Aggiunge gli elementi del dizionario d2 a quelli di d
print(letters);