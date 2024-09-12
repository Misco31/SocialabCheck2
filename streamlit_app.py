import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta

# Funzione per ottenere la data dell'ultimo post pubblicato negli ultimi 2 mesi
def get_last_post_date(username):
    try:
        # Crea l'istanza di Instaloader senza autenticazione
        L = instaloader.Instaloader()
        
        # Carica il profilo Instagram
        profile = instaloader.Profile.from_username(L.context, username)
        
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
        usernames = [username.strip() for username in usernames_input.split(',')]
        
        # Barra di progresso
        progress_bar = st.progress(0)
        total_usernames = len(usernames)
        
        # Visualizza i risultati
        for idx, username in enumerate(usernames):
            post_date = get_last_post_date(username)
            if post_date:
                days_passed = days_since_post(post_date)
                if is_older_than_week(days_passed):
                    st.markdown(f"<p style='color:red;'>Sono passati {days_passed} giorni dall'ultimo post di {username}.</p>", unsafe_allow_html=True)
                else:
                    st.write(f"Sono passati {days_passed} giorni dall'ultimo post di {username}.")
            else:
                st.write(f"Non ci sono post recenti per {username} (negli ultimi 2 mesi).")
            
            # Aggiorna la barra di progresso
            progress_bar.progress((idx + 1) / total_usernames)
    else:
        st.write("Per favore, inserisci almeno un nome utente.")

