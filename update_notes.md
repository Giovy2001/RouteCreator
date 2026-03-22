UPDATE #2.5 - GitHub Restyling
    this will be merged to main with update #3

    [x] Create readme
    [x] Rename to PalaEnrosadira - Chalk & Track


TODO UPDATE #3 - App sections rework

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

    # OUT of branch unstable

    [ ] Creare palette comune
        [ ] :root{} dovrebbe funzionare (cerca su internet)

    [ ] Implementare le quattro diverse sezioni
        [ ] Esplora
            [ ] Per ora non porta a nulla
            [ ] Magari under construction page
        [ ] Crea
            [ ] Fai in modo che sia visibile solo se username è salvato nel local_storage
        [ ] Archivio
            [ ] l'attuale index
        [ ] Profilo
            [ ] Icona del profilo
            [ ] Colore del profilo
                
    [ ] Manca l'icona del sito (favicon)
    [x] Cambiare nome a salvataggio nel local storage "chalk_and_track_username" 


TODO UPDATE #4 - Rework Route creation

    [ ] Provare a vedere se è possibile processare l'immagine lato client in modo da rendere più leggero il caricamento
    
    [ ] Scrap dell'idea delle tre fasi
        [ ] Fase unica con la pagina lunga come da stitch

    [ ] Riattivare lo scroll ma non lo zoom
    [ ] Valutare possibilità di ingrandire e rimpicciolire la presa con lo zoom (gesture pizzicata)
    [ ] Valutare possibilità di cambiare tipo di presa tenendo premuto su di essa

    [ ] Copri l'immagine con un qualcosa di semitrasparente che la renda più scura/desaturata
        [ ] le prese al posto di colorare l'interno dei tre colori, all'interno hanno i colori originale della foto
        [ ] colora dei tre colori le outline dei cerchi
        [ ] le label dei constraint dovrebbero avere una targhetta in modo che siano visibili sempre
        
    [ ] Far si che una volta selezionata una presa tu possa scrollare in qualsiasi punto dello schermo per spostarla
        [ ] Valutare differenza tra de-selezione e hold-drag


TODO UPDATE #5 - Archivio
    
    [ ] Possibilità di filtrare nell'index, per autore / nome / difficoltà
        [ ] Controlla come si fa la ricerca intelligente (lettera sbagliata ma comunque simile)
        

TODO UPDATE #6 - Esplora

    [ ] Pagina per trovare blocchi in evidenza
    [ ] Filtra solo i blocchi che non hai completato
    [ ] In base alla data, quelli più recenti prima
    [ ] Con un po' di randomicità
    [ ] Fullscreen tiktok feed
    [ ] Se non ci sono blocchi in evidenza cosa succede?


TODO UPDATE #7 - pulizia del codice

    [ ] Controllare durante l'esecuzione se ci sono errori nella console 
    [ ] Mettere ordine nel codice
    [ ] Aggiungere in python le tipologie delle variabili
    [ ] Commentare tutte le funzioni
    [ ] Rimuovere commenti relativi al precedente modo di passare le variabili con i cookies in create.py
    [ ] Valutare di rinominare i file per seguire una convenzione migliore
    [ ] Rimuovere da git i file di cache di python
