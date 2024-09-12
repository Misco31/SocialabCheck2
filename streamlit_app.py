import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time
import random
import requests

# Lista di User Agents da usare per variare le richieste
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
]

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
    attempt = 0
    max_attempts = 3  # Numero massimo di tentativi
    user_agent = random.choice(USER_AGENTS)  # Scegli un user agent casuale
    headers = {'User-Agent': user_agent}  # Aggiungi l'User Agent all'header

    while attempt < max_attempts:
        try:
            # Crea l'istanza di Instaloader senza autenticazione
            L = instaloader.Instaloader()

            # Usa headers personalizzati (per Instagram se possibile)
            L.context._default_http_headers.update(headers)

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

        except instaloader.exceptions.ConnectionException:
            attempt += 1
            wait_time = 2 ** attempt + random.uniform(0, 1)  # Backoff esponenziale
            time.sleep(wait_time)
        except Exception:
            return None
    return None  # Fallisce dopo aver superato il numero massimo di tentativi

# Funzione per calcolare i giorni passati dall'ultimo post
def days_since_post(date):
    return (datetime.now() - date).days

# Funzione per ottenere i dati dei profili in parallelo con throttling
def fetch_profile_data(username):
    post_date = get_last_post_date(username)
    if post_date:
        days_passed = days_since_post(post_date)
        if days_passed > 7:
            return (username, f"<p class='red-text'>{username}: {days_passed} giorni dall'ultimo post</p>")
        else:
            return (username, f"<p class='green-text'>{username}: {days_passed} giorni dall'ultimo post</p>")
    else:
        return (username, f"<p class='red-text'>{username}: Nessun post recente</p>")

# Funzione principale di Streamlit
def main():
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

    # Bottone per eseguire il controllo degli username
    with st.container():
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button('Controlla i profili'):
            st.markdown('</div>', unsafe_allow_html=True)

            if usernames:
                # Barra di stato
                progress = st.progress(0)
                total = len(usernames)

                # Uso di ThreadPoolExecutor per processare le richieste in parallelo
                with ThreadPoolExecutor(max_workers=3) as executor:  # Limita a 3 thread
                    results = list(executor.map(fetch_profile_data, usernames))

                for idx, result in enumerate(results):
                    username, status_message = result
                    st.markdown(status_message, unsafe_allow_html=True)

                    # Aggiornamento barra di caricamento
                    progress.progress((idx + 1) / total)

                    # Ritardo maggiore e casuale tra le richieste per evitare di sovraccaricare Instagram
                    time.sleep(random.uniform(3, 5))  # Aumento del tempo di attesa

            else:
                st.write("Non ci sono username nel database.")

# Avvio di Streamlit
if __name__ == "__main__":
    main()
