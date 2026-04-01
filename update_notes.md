# UPDATE #2.5 - GitHub Restyling
    this will be merged to main with update #3

    [x] Create readme
    [x] Rename to PalaEnrosadira - Chalk & Track


# TODO UPDATE #3 - Unstable branch

    [x] IMPORTANTE: Sono state fatte molte modifiche agli script del database, bisogna controllare tutte le volte che venivano chiamate le funzioni
    [x] Aggiungere abilità di usare progression_id "zone" e constraint_id "only_hand","only_foot","foot","only_volume","no_volume","normal"

    [x] Inserire nel databse tutte le cose necessarie per la nuova app
        [x] users
            [x] creare una nuova table users
            [x] user_id, user_name, user_icon, user_color, creation_date, last_seen_date, points, serialized_completed_routes
            [x] Test delle funzionalità
        [x] betas
            [x] creare una nuova table betas
            [x] beta_id, route_id, title, body
            [x] Foreign reference alla route (come holds)
        [x] routes
            [x] aggiungere difficoltà (opzionale)
            [x] Foreign reference a user_id
        [x] holds
            [x] rinominare use e type per essere più comprensibili
            [x] valutare di aggiungere altre informazioni

# TODO UPDATE #3.1 - App sections rework
    [x] rimuovere tutti i css a button object (perché sfanculano tutto)
        [x] vanno sostituiti con le modifiche al class name specifico

    [x] l'elemento selezionato della bar deve avere un riguardo di selezione (come stitch)
    [x] su iphone quando metti il nome senza riavviare la pagina le scritte sono sfalsate

    [ ] Implementare le quattro diverse sezioni
        [x] Esplora 
            [x] Per ora non porta a nulla
            [x] Magari under construction page
        [x] Crea
            [x] Fai in modo che sia visibile solo se username è salvato nel local_storage
            [x] Collega creazine al pulsante
        [x] Archivio
            [x] l'attuale index
            [x] sposta l'index su un nuovo file
            [x] Togli cose del profilo 
        [ ] Profilo
            [ ] Crea back end
                [x] Importante: trova un modo di evitare tutti i redirect delle pagine. Sono sicuro che con gli endpoint backend (come per il colore) si possa risolvere tutto
                [ ] Inoltre si può cambiare con lo script update bottom nav il link href così che se non c'è username nel local storage manda direttamente alla creazione
                [x] Quando l'user non esiste nel database, redirecta ad un altra pagina in cui ti fa accettare le condizioni e confermare la creazione dell'utente. Poi crea nel database
                [x] Crea profilo entry quando viene messo un nome che non esiste già
                [x] Se esiste già load il profilo esistente
                    [x] salta il check quando viene caricato da local storage (esiste per forza)
                [ ] Load
                    [ ] serialized completed routes per la sezione completati
                    [ ] load di tutti i blocchi dove autore è username (per la sezione blocchi tuoi e per le statistiche di blocchi creati e grado più alto)
            [ ] Front end logic
                [x] Nascondi stat se non ci sono da mostrare
                [ ] Nascondi blocchi completati se non ce ne sono
                [ ] (i miei blocchi non è mai nascosto perché volendo c'è il pulsantino per aggiungerli)
                [x] Tag sulla base di quanti blocchi hai completato
                    NEW — 0 → 200
                    BEG — 200 → 500
                    INT — 500 → 1.000
                    ADV — 1.000 → 2.500
                    EXP — 2.500 → 5.000
                    PRO — 5.000+
            [x] Icona del profilo
            [x] Colore del profilo
                
    [x] Icona sito
        [x] L'icona piccola dovrebbe essere solo logo (senza scritta e con bordi arrotondati)
        [x] Inserire su ogni head le informazioni dell'icona
        [x] Magari potrei avere diverse icone (quelle che vengono esportate sulla home iphone) una per colore del profilo così da poter customizzare l'icona
            [x] Non così facile, magari bisogna riavviare la pagina ma dovrebbe essere possibile
    [x] Cambiare nome a salvataggio nel local storage "chalk_and_track_username"

    [ ] Re inizializzare databases, sia local che turso (applicare le modifiche alle tables)
        [ ] Droppare le tabelle su turso prima per far si che vengano ricreate in modo corretto.
        [ ] Rimettere i due blocchi.
        [ ] Non so se conveine droppare le tabelle
        [ ] Magari modifico a mano routes e holds dove serve (potrebbe essere un problema per il linked author nelle routes)

    [ ] Usare la bottom nav come navigazione ovunque (anche condition va messa la bottom nav per tornare indietro)

    [ ] Creare palette comune
        [x] :root{} dovrebbe funzionare (cerca su internet)
        [ ] sostituire tutti i colori nel css con il riferimento alla variabile


# TODO UPDATE #4 - Rework Route creation

    [ ] Provare a vedere se è possibile processare l'immagine lato client in modo da rendere più leggero il caricamento
    
    [ ] Scrap dell'idea delle tre fasi, è fattibile?
        [ ] Fase unica con la pagina lunga come da stitch
        [ ] Riattivare lo scroll ma non lo zoom
        [ ] Si può rendere utilizzabile?

        [ ] L'idea migliore forse è:
            sempre solo una fase, ma la selezione è a parte
            [ ] Inizio sulla pagina di creazione (stitch),
            [ ] Possibilità di caricare l'immagine da li
            [ ] Una volta caricata rischiacciarci ti fa entrare nella modalità modifica prese
                [ ] Foto a tutto schermo, no zoom, no scroll, ecc...
    [ ] Usare la bottom nav come navigazione

    [ ] Valutare possibilità di ingrandire e rimpicciolire la presa con lo zoom (gesture pizzicata)
    [ ] Valutare possibilità di cambiare tipo di presa tenendo premuto su di essa

    [ ] Copri l'immagine con un qualcosa di semitrasparente che la renda più scura/desaturata
        [ ] le prese al posto di colorare l'interno dei tre colori, all'interno hanno i colori originale della foto
        [ ] colora dei tre colori le outline dei cerchi
        [ ] le label dei constraint dovrebbero avere una targhetta in modo che siano visibili sempre
        
    [ ] Far si che una volta selezionata una presa tu possa scrollare in qualsiasi punto dello schermo per spostarla
        [ ] Valutare differenza tra de-selezione e hold-drag
        [ ] Valutare possibilità di uno zoom?


# TODO UPDATE #5 - Archivio
    
    [ ] Possibilità di filtrare nell'index, per autore / nome / difficoltà
        [ ] Controlla come si fa la ricerca intelligente (lettera sbagliata ma comunque simile)
        

# TODO UPDATE #6 - Esplora

    [ ] Pagina per trovare blocchi in evidenza
    [ ] Filtra solo i blocchi che non hai completato
    [ ] In base alla data, quelli più recenti prima
    [ ] Con un po' di randomicità
    [ ] Fullscreen tiktok feed
    [ ] Se non ci sono blocchi in evidenza cosa succede?


# TODO UPDATE #7 - pulizia del codice

    [ ] Controllare durante l'esecuzione se ci sono errori nella console 
    [ ] Mettere ordine nel codice
    [ ] Aggiungere in python le tipologie delle variabili
    [ ] Commentare tutte le funzioni
    [ ] Rimuovere commenti relativi al precedente modo di passare le variabili con i cookies in create.py
    [ ] Valutare di rinominare i file per seguire una convenzione migliore
    [ ] Rimuovere da git i file di cache di python
