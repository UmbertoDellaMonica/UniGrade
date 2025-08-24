
### 📚 UniGrade

**UniGrade** è un’applicazione pensata per studenti universitari che vogliono gestire il proprio libretto digitale e calcolare la **media ponderata** dei voti in base ai CFU.
Supporta anche il voto **30 e Lode**, configurabile secondo le regole della propria università.

Con UniGrade puoi:

* Aggiungere, modificare e rimuovere esami con voto e CFU
* Calcolare la media ponderata in tempo reale
* Personalizzare il valore numerico del **30L**
* Visualizzare e organizzare il tuo libretto in un’interfaccia grafica semplice e intuitiva

### Build - Only Developers

Per poter effettuare una build del programma una volta modificato , basti scrivere questo comando sul terminale :

```sh
pyinstaller --onefile --windowed --icon=assets/unigrade-logo-icon.ico --add-data "assets;assets" app.py --name UniGrade
```
