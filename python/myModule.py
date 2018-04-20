def add(a, b):
    return a + b
 
def sub(a, b):
    return a - b
 
def mul(a, b):
    return a * b
 
def div(a, b):
    return a / b

# Equivale a main se il file è stato eseguito direttamente e non è stato importato
if __name__ == '__main__':
    import sys  # importiamo il modulo sys della libreria standard
    # definiamo un dict di operazioni che mappa i nomi con le funzioni corrispondenti
    ops = dict(add=add, sub=sub, mul=mul, div=div)
    # chiediamo all'utente di scegliere l'operazione
    choice = input("Seleziona un'operazione [add/sub/mul/div]: ")
    if choice not in ops:
        # se la scelta non è valida terminiamo il programma con un messaggio d'errore
        sys.exit('Operazione non valida!')
    # assegnamo a op la funzione scelta dall'utente
    op = ops[choice]
    try:
        # chiediamo all'utente di inserire i due valori, e proviamo a convertirli in float
        a = float(input('Inserisci il primo valore: '))
        b = float(input('Inserisci il secondo valore: '))
    except ValueError as err:
        # se la conversione fallisce terminiamo il programma con un messaggio d'errore
        sys.exit('Valore non valido: {}'.format(err))
    # stampiamo il risultato dell'operazione
    print('Il risultato è:', op(a, b))