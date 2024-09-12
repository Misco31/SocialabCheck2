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

# Creazione dell'interfaccia con Streamlit
st.title('Controlla gli ultimi post su Instagram')

# Creazione della tabella se non esiste già
create_table()

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

# Bottone per eseguire il controllo degli username nel database
if st.button('Controlla'):
    usernames = get_usernames()
    if usernames:
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
        st.write("Non ci sono username nel database.")
