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

# Crea il titolo della figura
fig.suptitle('Legge dell\'inverso del quadrato della distanza\n per l\'intensità luminosa')

# Creazione dei grafici che compongono la figura e disposizione in una griglia 2x2
ax1 = fig.add_subplot(221) # t-r
ax2 = fig.add_subplot(222) # t-I
ax3 = fig.add_subplot(223) # r-I
ax4 = fig.add_subplot(224) # 1/r**2-I

# Impostazione dei titoli e delle etichette degli assi
ax1.set_title('Test del sensore di distanza', fontsize=8) # titolo del I grafico
ax1.set_xlabel(r'$t\:(s)$') # etichetta asse x del I grafico
ax1.set_ylabel(r'$r\:(cm)$') # etichetta asse y del I grafico

ax2.set_title('Test del sensore di luminosità', fontsize=8) # titolo del II grafico
ax2.set_xlabel(r'$t\:(s)$') # etichetta asse x del II grafico
ax2.set_ylabel(r'$\frac{I}{I_0}$') # etichetta asse y del II grafico

ax3.set_title('Relazione distanza-intensità', fontsize=8) # titolo del III grafico
ax3.set_xlabel(r'$r\:(cm)$') # etichetta asse x del III grafico
ax3.set_ylabel(r'$\frac{I}{I_0}$') # etichetta asse y del III grafico

ax4.set_title('Linearizzazione della relazione\n distanza-intensità', fontsize=8) # titolo del IV grafico
ax4.set_xlabel(r'$\frac{1}{r^2}\:\left(cm^{-2}\right)$') # etichetta asse x del IV grafico
ax4.set_ylabel(r'$\frac{I}{I_0}$') # etichetta asse y del IV grafico

# Inizializzazione degli oggetti che rappresentano graficamente le serie di dati e i fit
err1 = ax1.errorbar([], [], yerr=[], fmt='-', markersize=5, elinewidth=1, color='#404d60')
err2 = ax2.errorbar([], [], yerr=[], fmt='-', markersize=5, elinewidth=1, color='#404d60')
err3 = ax3.errorbar([], [], xerr=[], yerr=[], fmt='o', markersize=5, elinewidth=1, color='#404d60')
fit3, = ax3.plot([], [], '-', lw=1, color='#ffb92d')
err4 = ax4.errorbar([], [], xerr=[], yerr=[], fmt='o', markersize=5, elinewidth=1, color='#404d60')
fit4, = ax4.plot([], [], '-', lw=1, color='#ffb92d')

# Ricalcola il layout dei grafici in modo che le etichette degli assi non si sovrappongano
fig.tight_layout(rect=[0, 0, 1, 0.9])

# Definizione del generatore di dati
def gen_data():
    t = 0
    for i in range(N):
        r = 2 + 98 * random() # genera un numero casuale nel range di sensibilità del sensore di distanza
        rerr = 0.3 # errore sulla misura di distanza
        r += 2 * rerr * (random() - 0.5) # correzione con errore casuale sulla distanza
        I = 4 / r**2 # valore teorico dell'intensità luminosa
        Ierr = (1 + I)**2 / 1024 # errore sull'intensità
        I += 2 * Ierr * (random() - 0.5) # correzione con errore casuale sull'intensità luminosa
        yield i, t, r, I, rerr, Ierr
        t += 0.1

# Definizione della funzione che aggiorna i dati
def update(data):
    i, t, r, I, rerr, Ierr = data
    ts[i], rs[i], Is[i] = t, r, I

    p1, errbars1, (ybars1, ) = err1
    p2, errbars2, (ybars2, ) = err2
    p3, errbars3, (xbars3, ybars3) = err3
    p4, errbars4, (xbars4, ybars4) = err4

    # Aggiornamento I grafico
    p1.set_data(ts[:i+1], rs[:i+1])

    yerrt1 = rs[:i+1] + rerr
    yerrb1 = rs[:i+1] - rerr

    ysegments1 = [np.array([[x, yt], [x, yb]]) for yt, yb, x in zip(yerrt1, yerrb1, ts[:i+1])]

    ybars1.set_segments(ysegments1)

    # Aggiornamento II grafico
    p2.set_data(ts[:i+1], Is[:i+1])
                
    yerrt2 = Is[:i+1] + Ierr
    yerrb2 = Is[:i+1] - Ierr

    ysegments2 = [np.array([[x, yt], [x, yb]]) for yt, yb, x in zip(yerrt2, yerrb2, ts[:i+1])]

    ybars2.set_segments(ysegments2)

    # Aggiornamento III grafico        
    p3.set_data(rs[:i+1], Is[:i+1])

    xerrt3 = rs[:i+1] + rerr
    xerrb3 = rs[:i+1] - rerr
    yerrt3 = Is[:i+1] + Ierr
    yerrb3 = Is[:i+1] - Ierr
                
    xsegments3 = [np.array([[xt, y], [xb, y]]) for xt, xb, y in zip(xerrt3, xerrb3, Is[:i+1])]
    ysegments3 = [np.array([[x, yt], [x, yb]]) for yt, yb, x in zip(yerrt3, yerrb3, rs[:i+1])]

    xbars3.set_segments(xsegments3)
    ybars3.set_segments(ysegments3)
    
    k, = np.linalg.lstsq(np.stack([1/rs[:i+1]**2], axis=-1), Is[:i+1], rcond=None)[0]
    x = np.linspace(min(rs[:i+1]), max(rs[:i+1]), 1000)
    y = k * 1 / x**2
    fit3.set_data(x, y)

    # Aggiornamento IV grafico    
    p4.set_data(1/rs[:i+1]**2, Is[:i+1])
                
    xerrt4 = 1/rs[:i+1]**2 + 2 * rerr / rs[:i+1]**3
    xerrb4 = 1/rs[:i+1]**2 - 2 * rerr / rs[:i+1]**3
    yerrt4 = Is[:i+1] + Ierr
    yerrb4 = Is[:i+1] - Ierr
                
    xsegments4 = [np.array([[xt, y], [xb, y]]) for xt, xb, y in zip(xerrt4, xerrb4, Is[:i+1])]
    ysegments4 = [np.array([[x, yt], [x, yb]]) for yt, yb, x in zip(yerrt4, yerrb4, 1/rs[:i+1]**2)]

    xbars4.set_segments(xsegments4)
    ybars4.set_segments(ysegments4)

    m = k
    fit4.set_data(1/rs[:i+1]**2, m * 1/rs[:i+1]**2)

    # Ricalcolo dei limiti sugli assi
    for ax in (ax1, ax2, ax3, ax4):
        ax.relim()
        ax.autoscale_view()
    
    return fit3, fit4, err1, err2, err3, err4,

# Creazione dell'animazione
ani = FuncAnimation(fig,
                    update,
                    frames=gen_data,
                    repeat=False)

# Mostra i grafici
plt.show()
