DEBUG = True

from app import app


if __name__ == "__main__":
    if DEBUG:
        app.run(debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)



"""
TODO:

    [ ] Sistemare CSS di ogni pagina
        [ ] Particolare attenzione a come viene visualizzato da telefono
    [ ] Nella pagina iniziale fare un semplice Login (solo username)
    [ ] Quando crei la via salva il tracciatore con il tuo username
    [ ] Se l'username combacia puoi eliminare le tue vie
    [ ] Le immagini dovrebbero essere convertite in jpg e scalate ad una risoluzione sensata
        [ ] Servirebbe creare un proxy 300*450 per la visualizzazione nell'index
    [ ] Possibilità di dare un titolo alla via ed eventualmente (ma non per forza) il grado
    [ ] Mostrare nell'index nome, tracciatore eventuale grado
    [ ] Il selettore delle prese dovrebbe essere più intelligente.
        [ ] Ricognizione automatica?
        [ ] Possibilità di aggiungere tag descrizione su ogni presa
        [ ] Possibilità di segnare "solo piede", "solo mano", "start", "zona", "top"
        [ ] Possibilità di segnare ordine prese
        [ ] Possibilità di spostare e eliminare prese
        
"""