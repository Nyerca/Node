n = int(input('Inserisci un numero: '))
if n < 0:   # se il numero è negativo
	n = -n  # rendilo positivo
elif n==0:
	print(n, 'è zero')
else:
	print(n, 'è positivo')
print('Il valore assoluto è', n)