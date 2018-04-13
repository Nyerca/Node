seq = [1, 2, 3, 4, 5]
for n in seq:
    print('Il numero', n, 'è', end=' ')
    if n%2 == 0:
        print('pari')
    else:
       print('dispari')
	   
print(list(range(0, 10, 2)));

for n in range(1, 6):
    print('Il quadrato di', n, 'è', n**2)
	
seq = [10, 20, 30, 40, 50, 60]
while len(seq) > 3:
    print(seq.pop())

	
# break: interrompe il ciclo;
seq = ['alpha', 'beta', 'gamma', 'delta']
for elem in seq:
    print('Sto controllando', elem)
    if elem == 'gamma':
        print('Elemento trovato!')
        break  # elemento trovato, interrompi il ciclo
	

# continue: interrompe l’iterazione corrente e procede alla successiva	
seq = ['alpha', 'beta', 'gamma', 'delta']
for elem in seq:
    if len(elem) == 5:
        continue  # procedi all'elemento successivo
    print(elem)
	
	

# Il blocco di codice nell’else viene eseguito se il ciclo termina tutte le iterazioni. 
# Se invece il ciclo è interrotto da un break, l’else non viene eseguito.
n = 8
for x in range(3):
    guess = int(input('Inserisci un numero da 1 a 10: '))
    if guess == n:
        print('Hai indovinato!')
        break  # numero indovinato, interrompi il ciclo
else:
    print('Tentativi finiti. Non hai indovinato')