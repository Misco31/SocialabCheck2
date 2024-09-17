import pandas as pd
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
            wait_time = 2 ** attempt + random.uniform(1, 3)  # Attendi tra 1 e 3 secondi
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

# Stile personalizzato per il titolo e il pulsante
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #8e6d7a;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .red-text {
        color: #FF6347;
        font-weight: bold;
    }
    .green-text {
        color: #90EE90;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Titolo principale
st.markdown('<div class="main-title">Socialab Check Status</div>', unsafe_allow_html=True)

# Bottone centrato per eseguire il controllo
with st.container():
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button('Controlla'):
        st.markdown('</div>', unsafe_allow_html=True)

        # Crea l'istanza di Instaloader senza autenticazione
        L = instaloader.Instaloader()

        # Barra di stato
        progress = st.progress(0)
        total = len(usernames)

        # Visualizza i risultati
        for idx, username in enumerate(usernames):
            # Applica un ritardo casuale tra le richieste per evitare di sovraccaricare i server di Instagram
            time.sleep(random.uniform(4, 6))  # Attendi tra 2 e 4 secondi

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
