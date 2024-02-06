## Sijoitussalkku - sovellus sijoitusten hallintaan
Sovelluksen tarkoitus on säilyttää tietoja sijoituksista ja hyödyntää näitä tietoja veroilmoituksen 
täyttämisessä sekä sijoitusten hallinnoinnissa ja suunnittelussa. 

### Toiminnallisuuksia, joita sovellukseen pyritään saamaan
- Käyttäjä pystyy lisäämään sovellukseen (sijoitusten) omistajia
- Käyttäjä pystyy lisäämään sovellukseen tilejä
- Käyttäjä pystyy lisäämään sovellukseen osakkeita
- Käyttäjä pystyy lisäämään nimetyn omistajan nimetylle tilille osakkeen osto- tai myyntitapahtuman
- Käyttäjä pystyy hakemaan tiedon kunkin omistajan sijoituksista
- Käyttäjä pystyy hakemaan tiedon kaikkien omistajien yhteisistä sijoituksista
- Käyttäjä pystyy lisäämään sovellukseen lisätyille osakkeille näiden vuotuisen osingon määrän
- Käyttäjä pystyy hakemaan tiedon kunkin omistajan saamista vuotuisista osingoista
- Käyttäjä pystyy näkemään, mitkä osto- ja myyntitapahtumat liittyvät toisiinsa

### Sovelluksen tämänhetkinen tilanne
Sovellus on aivan alkutekijöissään, eikä siinä ole juurikaan toiminnallisuutta. Ainoa toiminnallisuus
on osto- tai myyntitapahtuman lisääminen. Toiminnallisuuteen liittyvät, vielä puuttuvat osat (omistajan,
tilin ja osakkeen lisääminen) on korvattu kovakoodauksella. Tietokantaan talletettuja tietoja ei saa
vielä näkyviin selaimeen, ne ovat nähtävissä vain psql-tulkilla. 

### Sovelluksen käyttö
Sovelluksen käyttö edellyttää projektin lataamista omalle koneelle. Sovellus vaatii toimiakseen myös
Postgres-tietokannan. Lisäksi projektin juureen pitää lisätä tiedosto .env jonka sisällöksi tulee:
DATABASE_URL=postgresql:///<käyttäjätunnus>
SECRET_KEY=<oma salasana>

Virtuaaliympäristö käynnistetään komennoilla 
bash```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
Tietokanta alustetaan komennolla
```
psql < schema.sql
```
ja sovellus käynnistyy flaskapp-hakemistotasolta komennolla
```
flask run
```

