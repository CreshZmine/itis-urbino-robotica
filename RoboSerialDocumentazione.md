# RoboSerial | Documentazione #

# Paramentri base: #
### Porta Primaria: ###
> /dev/ttyAMA0 (Porta usata su Raspberry PI)
### Porta Alternativa: ###
> COM2 (Porta usata per simulazione su Windows)
### Baudrate: ###
115200 baud
### Carattere terminatore della comunicazione: ###
> `*`


# Funzioni: #

### init (costruttore della classe) ###
Nessun parametro richiesto. Si occupa solo di istanziare e valorizzare la variabili base per la comunicazione.

### OpenConnection ###
Nessun parametro richiesto. Apre una connessione seriale tramite le porte prestabilite della classe. Prima prova la porta primaria e se non è disponibile prova la porta alternativa.

### OpenConnectionPort ###
Richede una striga contenente la porta da utilizzare per la connessione. SApre  una connessione seriale tramite le porte passata per argomento.

### CloseConnection ###
Nessun parametro richiesto. Chiude la connessione seriale se aperta.