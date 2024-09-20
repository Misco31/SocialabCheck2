import instaloader
import streamlit as st
from datetime import datetime, timedelta
import time
import random

# Funzione per autenticarsi su Instagram
def login_instaloader(username, password):
    L = instaloader.Instaloader()
    try:
        L.login(username, password)
        return L
    except instaloader.exceptions.LoginException as e:
        st.error(f"Errore di login: {e}")
        return None

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
        st.error(f"Errore nel recupero dei dati per {username}: {e}")
        return None

# Funzione per calcolare i giorni passati dall'ultimo post
def days_since_post(date):
    return (datetime.now() - date).days

# Funzione per controllare se la data è più vecchia di una settimana
def is_older_than_week(days_passed):
    return days_passed > 7

# Interfaccia Streamlit per inserire credenziali
st.title('Socialab Instagram Checker')

# Input per username e password
insta_user = st.text_input("Inserisci il tuo username Instagram")
insta_pass = st.text_input("Inserisci la tua password Instagram", type="password")

if st.button("Accedi e Controlla"):
    if insta_user and insta_pass:
        # Autenticazione senza proxy (VPN instrada il traffico)
        L = login_instaloader(insta_user, insta_pass)

        if L:
            # Barra di stato
            progress = st.progress(0)
            total = len(usernames)

            # Visualizza i risultati
            for idx, username in enumerate(usernames):
                # Ritardo casuale maggiore per evitare di sovraccaricare i server di Instagram
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
