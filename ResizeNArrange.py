import pyautogui


# TODO Considerare overscan, per ora fix usando min_elementi_per_riga a 5 o 6


class ResizeNArrange:

    def __init__(self):

        self.risoluzione_w, self.risoluzione_h = pyautogui.size()

        self.min_larghezza = 300    # Minima larghezza del singolo elemento
        self.min_altezza = 500
        
        self.min_elementi_riga = 6  # Opzioanle


        # Valori di offset per gestire barra delle app e barre laterali
        self.offset_x = 15
        self.offset_y = 32

    def individua_finestre(self):
        '''Trova e ritorna una lista contenente le finestre che ci interessa sistemare'''
        
        lista_finestre = []
        for denominazione in ['File Explorer']:
             lista_tmp = pyautogui.getWindowsWithTitle(denominazione)
             lista_finestre += lista_tmp

        return lista_finestre

    def calcola_larghezza(self, num_finestre):
        '''Calcola la larghezza della singola finestra basandosi sul numero di finestre da porre sulla stessa riga'''
        return int(self.risoluzione_w/num_finestre) + self.offset_x
    
    
    def calcola_stime(self, lista_finestre):
        '''Calcola delle stime provvisorie dei valori di larghezza e altezza della finestra singola'''
        num_finestre = len(lista_finestre)
        risoluzione_larghezza, risoluzione_altezza = pyautogui.size()   # Risoluzione dello schermo attuale
        larghezza_stimata = int(risoluzione_larghezza/num_finestre) + self.offset_x   # Larghezza per dividere lo schermo equamente
        altezza_stimata = int(risoluzione_altezza) - self.offset_y

        return larghezza_stimata, altezza_stimata


    def calcola_dimensioni_corrette(self, larghezza_singolo, altezza_singolo, num_elementi):
        
        # All'inizio abbiamo che il numero di elementi in una singola riga è il massimo
        
        num_elementi_per_riga = num_elementi  # Calcoliamo quanti elementi in una riga ci sono. Al momento son tutti su una singola riga
        altezza_singola_corretta = altezza_singolo   # Modificheremo l'altezza, variabile di copia



        while larghezza_singolo < self.min_larghezza:
            num_elementi_per_riga -= 1  # Eliminiamo un elemento dalla riga. Potenzialmente se ne crea un'altra
            larghezza_singolo = self.calcola_larghezza(num_elementi_per_riga)
            
            if num_elementi_per_riga <= self.min_elementi_riga:
                break # TODO da testare
    
    
        # Calcolato il numero di elementi che ci stanno correttamente in una riga, partendo da un minimo, ora possiamo calcolare l'altezza delle finestre
            

        # for step in range(0,num_elementi, num_elementi_per_riga):
        #     pass # Otteniamo variabile
            
        # numero_elementi_ultima_riga = num_elementi - step
        num_righe = round(num_elementi/num_elementi_per_riga)   # Arrotondiamo, potenzialmente ultima riga non completa, da gestire
        altezza_singola_corretta /= num_righe   # Abbiamo l'altezza corretta sapendo quante righe ci sono
        
        return larghezza_singolo, altezza_singola_corretta
            
    

    def definisci_tuple_posizioni(self, lista_windows, larghezza_singolo, altezza_singolo):
        '''Calcola le tuple contenenti le posizioni sullo schermo delle singole finestre'''
        
        lista_tuple = [(0,0)]
        inc = 0   # offset per la barra laterale
        contatore_elementi = 1      # Forzato
        altezza_riga = 0

        for i in range(0, len(lista_windows)):
            inc += larghezza_singolo - 15

            if (larghezza_singolo * contatore_elementi) >=  self.risoluzione_w:
                contatore_elementi =0  # Resetta
                altezza_riga += altezza_singolo - 8     # Altro offset casuale, da capire why 8
                inc = 0

            tupla = (inc, int(altezza_riga))
            lista_tuple.append(tupla)
            contatore_elementi += 1

        return lista_tuple


    def effettua_resize_e_arrange(self,lista_finestre, lista_tuple, larghezza, altezza):
        '''Operazione master. Da effettuare dopo aver precalcolato posizioni e dimensioni'''
        indice = 0

        for finestra in lista_finestre:

            finestra.resizeTo(int(larghezza), int(altezza))
            finestra.moveTo(int(lista_tuple[indice][0]) - 10, int(lista_tuple[indice][1]))
            finestra.restore()
            indice += 1


def main():

    resizer = ResizeNArrange()
    lista_finestre = resizer.individua_finestre()
    larghezza_stimata, altezza_stimata = resizer.calcola_stime(lista_finestre)
    larghezza_corretta, altezza_corretta = resizer.calcola_dimensioni_corrette(larghezza_stimata, altezza_stimata, len(lista_finestre))
    lista_posizioni = resizer.definisci_tuple_posizioni(lista_finestre, larghezza_corretta, altezza_corretta)
    resizer.effettua_resize_e_arrange(lista_finestre, lista_posizioni, larghezza_corretta, altezza_corretta)



if __name__ == "__main__":
    main()
