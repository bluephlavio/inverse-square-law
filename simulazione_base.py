import numpy as np # libreria per calcolo numerico
from numpy.random import * # importa tutte le funzioni per la generazione casuale di numeri da numpy.random
import matplotlib.pyplot as plt # libreria per il plotting dei dati
from matplotlib.animation import FuncAnimation # importa la classe FuncAnimation per la creazione di un'animazione basata su una funzione 

N = 100 # numero di dati

# Inizializzazione delle serie di dati come array vuoti di dimensione N
ts = np.empty(N) # tempi
rs = np.empty(N) # distanze
Is = np.empty(N) # intensità

# Crea la figura impostando il titolo della finestra
fig = plt.figure('Simulazione')

# Creazione degli assi
ax = fig.add_subplot(111)

# Impostazione del titolo e delle etichette degli assi
ax.set_title('Relazione distanza-intensità', fontsize=8) # titolo
ax.set_xlabel(r'$r\:(cm)$') # etichetta asse x
ax.set_ylabel(r'$\frac{I}{I_0}$') # etichetta asse

# Inizializzazione dell'oggetto grafico che rappresenta la serie di dati
p, = ax.plot([], [], 'bo')

# Definizione del generatore di dati
def gen_data():
    t = 0
    for i in range(N):
        r = 2 + 398 * random() # genera un numero casuale nel range di sensibilità del sensore di distanza
        I = 4 / r**2 # valore teorico dell'intensità luminosa
        yield i, t, r, I
        t += 0.1

# Definizione della funzione che aggiorna i dati
def update(data):
    i, t, r, I = data
    ts[i], rs[i], Is[i] = t, r, I
    
    p.set_data(rs[:i+1], Is[:i+1])

    ax.relim()
    ax.autoscale_view()
    
    return p,

# Creazione dell'animazione
ani = FuncAnimation(fig,
                    update,
                    frames=gen_data,
                    repeat=False)

# Mostra i grafici
plt.show()
