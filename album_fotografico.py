import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO

    # L'album è una lista di liste. Formato: [ [anno1, [lista_foto]], [anno2, [lista_foto]] ]
    nuovo_album = []

    try:
        # Apro il file in lettura
        with open(file_path, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)

            # Salto la riga di intestazione (header)
            next(reader, None)

            # Itero riga per riga
            for riga in reader:
                # Verifico che la riga sia correttamente formattata (5 colonne)
                if len(riga) == 5:
                    # Estraggo i dati pulendoli dagli spazi bianchi iniziali e finali
                    codice = riga[0].strip()
                    titolo = riga[1].strip()
                    autore = riga[2].strip()
                    mese = int(riga[3].strip())
                    anno = int(riga[4].strip())

                    # Modello la singola foto come un dizionario
                    foto = {
                        "codice": codice,
                        "titolo": titolo,
                        "autore": autore,
                        "mese": mese,
                        "anno": anno
                    }

                    # Verifico se l'anno è già presente nel nostro album
                    anno_trovato = False
                    for elemento_anno in nuovo_album:
                        # elemento_anno[0] è l'intero dell'anno, elemento_anno[1] è la lista delle foto
                        if elemento_anno[0] == anno:
                            elemento_anno[1].append(foto)
                            anno_trovato = True
                            break

                    # Se l'anno non era presente, creiamo una nuova entry nell'album
                    if not anno_trovato:
                        nuovo_album.append([anno, [foto]])

        return nuovo_album

    except FileNotFoundError:
        # Se il file non esiste, sollevo l'eccezione restituendo None
        print(f"Errore: Il file {file_path} non è stato trovato.")
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO

    # 1. Validazione del mese (deve essere tra 1 e 12)
    if mese < 1 or mese > 12:
        print("Errore: Il mese deve essere compreso tra 1 e 12.")
        return None

    # 2. Controllo univocità del codice
    for elemento_anno in album:
        for foto in elemento_anno[1]:
            if foto["codice"] == codice:
                print(f"Errore: La foto con codice {codice} è già presente.")
                return None

    # 3. Aggiornamento del file CSV in modalità append ('a')
    try:
        with open(file_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([codice, titolo, autore, mese, anno])
    except FileNotFoundError:
        # Nel caso in cui fallisca l'accesso al file
        print("Errore: Impossibile accedere al file per l'aggiornamento.")
        return None

    # 4. Aggiornamento della struttura dati in memoria
    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    anno_trovato = False
    for elemento_anno in album:
        if elemento_anno[0] == anno:
            elemento_anno[1].append(nuova_foto)
            anno_trovato = True
            break

    # Se l'anno inserito è nuovo, creo la nuova categoria nell'album
    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO

    # Navigo attraverso le liste di anni e le rispettive liste di foto
    for elemento_anno in album:
        for foto in elemento_anno[1]:
            if foto["codice"] == codice:
                # Se la trovo, restituiso la stringa formattata
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"

    # Se il ciclo termina senza averla trovata
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO

    # Cerco l'anno richiesto nell'album
    for elemento_anno in album:
        if elemento_anno[0] == anno:
            # Estraggo tutti i titoli dalle foto appartenenti a questo anno
            titoli = [foto["titolo"] for foto in elemento_anno[1]]

            # Ordino la lista dei titoli alfabeticamente
            titoli.sort()

            return titoli

    # Se l'anno richiesto non è presente nella struttura dati
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    print("Album caricato correttamente!")
                    break
                else:
                    print("Riprova.")


        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
