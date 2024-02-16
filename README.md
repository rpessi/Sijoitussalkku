## Sijoitussalkku - sovellus sijoitusten hallintaan
Sovelluksen tarkoitus on säilyttää tietoja sijoituksista ja hyödyntää näitä tietoja veroilmoituksen 
täyttämisessä sekä sijoitusten hallinnoinnissa ja suunnittelussa. 

### Toiminnallisuuksia, joita sovellukseen pyritään saamaan
- Käyttäjä pystyy luomaan käyttäjätunnuksen ja kirjautumaan sovellukseen - toteutettu
- Käyttäjä pystyy lisäämään sovellukseen (sijoitusten) omistajia - toteutettu
- Käyttäjä pystyy lisäämään sovellukseen valitulle omistajalle arvo-osuustilejä - toteutettu 
- Käyttäjä pystyy lisäämään sovellukseen osakkeita - toteutettu
- Käyttäjä pystyy lisäämään nimetyn omistajan nimetylle tilille nimetyn osakkeen osto- tai myyntitapahtuman - toteutettu
- Käyttäjä pystyy hakemaan tiedon kunkin omistajan sijoituksista
- Käyttäjä pystyy hakemaan tiedon kaikkien omistajien yhteisistä sijoituksista
- Käyttäjä pystyy lisäämään sovellukseen lisätylle osakkeelle vuotuisen osingon määrän
- Käyttäjä pystyy hakemaan tiedon kunkin omistajan saamista vuotuisista osingoista
- Käyttäjä pystyy näkemään, mitkä osto- ja myyntitapahtumat liittyvät toisiinsa

### Sovelluksen tämänhetkinen tilanne
Sovellukseen voi luoda käyttäjätunnuksen ja kirjautua. Sovellukseen voi lisätä omistajia, arvo-osuustilejä ja osakkeita.
Arvo-osuustilin lisääminen edellyttää, että ainakin yksi omistaja on lisätty. Kun sovelluksessa on lisättyjä omistajia,
arvo-osuustilejä ja osakkeita, voi käyttäjä lisätä joko osto- tai myyntitapahtuman. Tapahtuman omistaja, tili ja osake
valitaan tietokantaan tallennetuista vaihtoehdoista. Myynti- ja ostotapahtumien paritus FIFO-periaatteen mukaisesti on
toteutettu tietokantatasolla. Valtaosasta käyttäjän antamien syötteiden arvoista puuttuu validointi ja virheilmoitukset.
Kunnollinen käyttöohje sovelluksen etusivulta puuttuu.

### Sovelluksen käyttö
Sovelluksen käyttö edellyttää projektin lataamista omalle koneelle. Sovellus vaatii toimiakseen myös
Postgres-tietokannan. Lisäksi projektin juureen pitää lisätä tiedosto .env jonka sisällöksi tulee:
```bash
DATABASE_URL=postgresql+psycopg2:///<oma käyttäjätunnus>
SECRET_KEY=<itsemuodostettu salasana>
```
Virtuaaliympäristö käynnistetään komennoilla 
```
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
