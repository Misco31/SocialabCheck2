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
        color: #2F4F4F;
    }
    .results-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        justify-items: center;
        margin-top: 30px;
    }
    .result-box {
        width: 150px;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    .green-box {
        background-color: #90EE90;
        color: black;
    }
    .red-box {
        background-color: #FF6347;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Titolo principale
st.markdown('<div class="main-title">Socialab Check Status</div>', unsafe_allow_html=True)

# Bottone per eseguire il controllo degli username nel database
if st.button('Controlla i profili'):
    if usernames:
        st.markdown('<div class="results-grid">', unsafe_allow_html=True)
        
        # Visualizza i risultati
        for username in usernames:
            post_date = get_last_post_date(username)
            if post_date:
                days_passed = days_since_post(post_date)
                if is_older_than_week(days_passed):
                    st.markdown(f'<div class="result-box red-box">{username}: {days_passed} giorni</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-box green-box">{username}: {days_passed} giorni</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-box red-box">{username}: Nessun post recente</div>', unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Non ci sono username nel database.")
