import pandas as pd
import instaloader
import streamlit as st
from datetime import datetime, timedelta
import sqlite3

# Funzione per la creazione e connessione al database
def create_connection():
    conn = sqlite3.connect('instagram_profiles.db')
    return conn

# Funzione per creare la tabella degli username (se non esiste già)
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Funzione per ottenere tutti gli username dal database
def get_usernames():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM profiles")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Funzione per aggiungere un username al database
def add_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

# Funzione per rimuovere un username dal database
def remove_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE username = ?", (username,))
    conn.commit()
    conn.close()

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

# Creazione della tabella se non esiste già
create_table()

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
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        justify-items: center;
        margin-top: 30px;
    }
    .result-box {
        width: 200px;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        font-size: 20px;
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

# Layout con colonne
col1, col2 = st.columns([1, 3])

# Colonna laterale con il database
with col1:
    st.subheader("Gestione del database")
    
    # Sezione per aggiungere un nuovo username
    new_username = st.text_input('Aggiungi un nuovo username di Instagram:')
    if st.button('Aggiungi'):
        if new_username:
            add_username(new_username)
            st.success(f"Username {new_username} aggiunto.")
        else:
            st.error("Inserisci un nome utente valido.")

    # Sezione per rimuovere un username
    remove_username_input = st.text_input('Rimuovi un username di Instagram:')
    if st.button('Rimuovi'):
        if remove_username_input:
            remove_username(remove_username_input)
            st.success(f"Username {remove_username_input} rimosso.")
        else:
            st.error("Inserisci un nome utente valido da rimuovere.")

    # Visualizzazione degli username nel database
    st.subheader("Username nel database")
    usernames = get_usernames()
    st.write(usernames)

# Colonna centrale per i risultati del controllo
with col2:
    # Bottone per eseguire il controllo degli username nel database
    if st.button('Controlla i profili'):
        usernames = get_usernames()
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

