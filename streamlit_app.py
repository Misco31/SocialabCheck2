import instaloader
import streamlit as st
from datetime import datetime, timedelta
import time
import random

# Lista di profili da controllare
usernames = [
    "hotelbellavistacavalese", "olimpionicohotel", "fondazioneFiemmePer", 
    "spartansgymasd", "carpenteria_bonelli", "zambonilattonerie", "radiofiemme", 
    "socialabtrentino", "elcalderoncavalese", "kaiserstubecanazei", "kaiserkellercanazei", 
    "hexenklub", "bertignoll1910", "chalet44alpinelounge", "poldopub.predazzo", 
    "in.treska", "carpanospeck", "osteria_da_carpano", "coopcavalese"
]

# Funzione per ottenere la data dell'ultimo post pubblicato negli ultimi 2 mesi
def get_last_post_date(username, loader):
    attempt = 0
    max_attempts = 3  # Numero massimo di tentativi
    while attempt < max_attempts:
        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            posts = profile.get_posts()
            two_months_ago = datetime.now() - timedelta(days=60)
            for post in posts:
                if post.date >= two_months_ago:
                    return post.date
            return None
        except instaloader.exceptions.ConnectionException:
            # Backoff esponenziale per gestire problemi di connessione
            attempt += 1
            wait_time = 2 ** attempt + random.uniform(3, 5)  # Attendi tra 3 e 5 secondi
            time.sleep(wait_time)
        except Exception as e:
            # Stampa o registra l'errore per debug
            print(f"Errore nel recupero dei dati per {username}: {e}")
            return None
    return None

# Funzione per calcolare i giorni passati dall'ultimo post
def days_since_post(date):
    return (datetime.now() - date).days

# Funzione per controllare se la data è più vecchia di una settimana
def is_older_than_week(days_passed):
    return days_passed > 7

# Funzione per autenticarsi con Instagram
def login_instaloader(username, password):
    L = instaloader.Instaloader()
    L.login(username, password)
    return L

# Interfaccia Streamlit per inserire credenziali
st.title('Socialab Instagram Checker')

insta_user = st.text_input("Inserisci il tuo username Instagram")
insta_pass = st.text_input("Inserisci la tua password Instagram", type="password")

if st.button("Accedi e Controlla"):
    if insta_user and insta_pass:
        L = login_instaloader(insta_user, insta_pass)

        # Barra di stato
        progress = st.progress(0)
        total = len(usernames)

        # Visualizza i risultati
        for idx, username in enumerate(usernames):
            # Applica un ritardo casuale maggiore tra le richieste per evitare di sovraccaricare i server di Instagram
            time.sleep(random.uniform(6, 10))  # Attendi tra 6 e 10 secondi

            post_date = get_last_post_date(username, L)
            if post_date:
                days_passed = days_since_post(post_date)
                if is_older_than_week(days_passed):
                    st.markdown(f"<p class='red-text'>{username}: {days_passed} giorni dall'ultimo post</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='green-text'>{username}: {days_passed} giorni dall'ultimo post</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='red-text'>{username}: Nessun post recente (negli ultimi 2 mesi)</p>", unsafe_allow_html=True)

            # Aggiornamento della barra di caricamento
            progress.progress((idx + 1) / total)
    else:
        st.error("Per favore, inserisci username e password validi.")
