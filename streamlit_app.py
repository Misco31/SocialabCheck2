import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta

# Funzione per ottenere la data dell'ultimo post pubblicato negli ultimi 2 mesi
def get_last_post_date(username, loader):
    try:
        # Carica il profilo Instagram
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Ottiene i post del profilo
        posts = profile.get_posts()
        
        # Imposta la data limite a 2 mesi fa
        two_months_ago = datetime.now() - timedelta(days=60)
        
        # Cerca il post più recente che sia stato pubblicato negli ultimi 2 mesi
        for post in posts:
            if post.date >= two_months_ago:
                return post.date
        
        return None  # Nessun post recente trovato

    except Exception as e:
        return None

# Funzione per calcolare i giorni passati dall'ultimo post
def days_since_post(date):
    return (datetime.now() - date).days

# Funzione per controllare se la data è più vecchia di una settimana
def is_older_than_week(days_passed):
    return days_passed > 7

# Creazione dell'interfaccia con Streamlit
st.title('Controlla gli ultimi post su Instagram')

# Input per gli username
usernames_input = st.text_input('Inserisci gli username di Instagram separati da virgola:')

# Bottone per eseguire il controllo
if st.button('Controlla'):
    if usernames_input:
        # Crea l'istanza di Instaloader senza autenticazione
        L = instaloader.Instaloader()
        
        # Split degli username separati da virgola
        usernames = [username.strip() for username in usernames_input.split(',')]
        
        # Visualizza i risultati
        for username in usernames:
            post_date = get_last_post_date(username, L)
            if post_date:
                days_passed = days_since_post(post_date)
                if is_older_than_week(days_passed):
                    st.markdown(f"<p style='color:red;'>{username}: {days_passed} giorni dall'ultimo post</p>", unsafe_allow_html=True)
                else:
                    st.write(f"{username}: {days_passed} giorni dall'ultimo post")
            else:
                st.write(f"{username}: Nessun post recente (negli ultimi 2 mesi).")
    else:
        st.write("Per favore, inserisci almeno un nome utente.")
