import instaloader
import streamlit as st
from datetime import datetime, timedelta
import time
import random

# Funzione per caricare la sessione salvata
def load_instaloader_session(username):
    L = instaloader.Instaloader()
    # Carica la sessione salvata
    L.load_session_from_file(username)
    return L

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
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        two_months_ago = datetime.now() - timedelta(days=60)
        for post in posts:
            if post.date >= two_months_ago:
                return post.date
        return None
    except Exception as e:
        print(f"Errore nel recupero dei dati per {username}: {e}")
        return None

# Funzione per calcolare i giorni passati dall'ultimo post
def days_since_post(date):
    return (datetime.now() - date).days

# Funzione per controllare se la data è più vecchia di una settimana
def is_older_than_week(days_passed):
    return days_passed > 7

# Interfaccia Streamlit per il controllo
st.title('Socialab Instagram Checker')

if st.button("Carica Sessione e Controlla"):
    try:
        L = load_instaloader_session("tuo_username_instagram")

        # Barra di stato
        progress = st.progress(0)
        total = len(usernames)

        # Visualizza i risultati
        for idx, username in enumerate(usernames):
            # Ritardo casuale per evitare sovraccarico
            time.sleep(random.uniform(6, 10))

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

    except Exception as e:
        st.error(f"Errore durante il caricamento della sessione: {e}")
