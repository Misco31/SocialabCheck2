import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta

# Lista di profili da controllare
usernames = [
    "hotelbellavistacavalese", "olimpionicohotel", "fondazioneFiemmePer", 
    "spartangymasd", "carpenteria_bonelli", "zambonilattonerie", "radiofiemme", 
    "socialabtrentino", "elcalderoncavalese", "kaiserstubecanazei", "kaiserkellercanazei", 
    "hexenklub", "bertignoll1910", "chalet44alpinelounge", "poldopub.predazzo", 
    "in.treska", "carpanospeck", "osteria_da_carpano", "coopcavalese"
]

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

# Layout della pagina
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 50px;
        color: #8e6d7a;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
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

# Bottone centrato per eseguire il controllo degli username
with st.container():
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button('Controlla i profili'):
        st.markdown('</div>', unsafe_allow_html=True)

        if usernames:
            # Barra di stato
            progress = st.progress(0)
            total = len(usernames)

            for idx, username in enumerate(usernames):
                post_date = get_last_post_date(username)
                if post_date:
                    days_passed = days_since_post(post_date)
                    if is_older_than_week(days_passed):
                        st.markdown(f'<p class="red-text">{username}: {days_passed} giorni dall\'ultimo post</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="green-text">{username}: {days_passed} giorni dall\'ultimo post</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="red-text">{username}: Nessun post recente</p>', unsafe_allow_html=True)

                # Aggiornamento barra di caricamento
                progress.progress((idx + 1) / total)

        else:
            st.write("Non ci sono username nel database.")
