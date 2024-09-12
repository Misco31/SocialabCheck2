import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta

# Funzione per ottenere la data dell'ultimo post
def get_last_post_date(username):
    L = instaloader.Instaloader()

    # Disabilitare la cache per ottenere sempre dati aggiornati
    L.download_pictures = False
    L.save_metadata = False
    L.post_metadata_txt_pattern = ""

    try:
        # Carica il profilo Instagram
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Ottiene i post del profilo
        posts = profile.get_posts()
        
        # Ottieni il primo post (il più recente)
        last_post = next(posts)
        
        # Formatta la data del post
        last_post_date = last_post.date
        return last_post_date
    except Exception as e:
        return None

# Funzione per controllare se la data è più vecchia di una settimana
def is_older_than_week(date):
    return date < datetime.now() - timedelta(weeks=1)

# Creazione dell'interfaccia con Streamlit
st.title('Controlla gli ultimi post su Instagram')

# Input per inserire gli username separati da virgola
usernames_input = st.text_input('Inserisci gli username di Instagram separati da virgola:')

# Bottone per eseguire il controllo
if st.button('Controlla'):
    if usernames_input:
        # Split degli username separati da virgola
        usernames = [username.strip() for username in usernames_input.split(',')]
        
        # Visualizza i risultati
        for username in usernames:
            post_date = get_last_post_date(username)
            if post_date:
                if is_older_than_week(post_date):
                    st.markdown(f"<p style='color:red;'>L'ultimo post di {username} è stato pubblicato il {post_date.strftime('%d %B %Y, %H:%M:%S')}</p>", unsafe_allow_html=True)
                else:
                    st.write(f"L'ultimo post di {username} è stato pubblicato il {post_date.strftime('%d %B %Y, %H:%M:%S')}")
            else:
                st.write(f"Errore nel recupero delle informazioni per {username}.")
    else:
        st.write("Per favore, inserisci almeno un nome utente.")


