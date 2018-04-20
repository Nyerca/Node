f = open('test.txt', 'w') #Il file viene creato
print(f.name);
f.write('prima riga del file\n')  # scriviamo una riga nel file
f.close()

f = open('test.txt')  # riapriamo il file in lettura
content = f.read()  # leggiamo tutto il contenuto del file
print(content)



lines = [
    'prima riga del file\n',
    'seconda riga del file\n',
    'terza riga del file\n',
]
f = open('test.txt', 'w')
f.writelines(lines);
f.close()

f = open('test.txt')
print(f.readline());
print(f.readlines());
f.close()

f = open('test.txt')  # riapriamo il file in lettura
for line in f:  # iteriamo sulle righe del file
    print("a");
f.close()

# Operazioni che vanno eseguite all'entrata e all'uscita dal contesto
# Tali operazioni non vengono definite da noi
f = open('test.txt', 'w')  # creiamo il file object
with f:  # usiamo il file object come context manager nel with
    f.write('contenuto del file')  # scriviamo il file

print(f.closed);



with open('test.txt', 'w') as f:
    f.write('contenuto del file')