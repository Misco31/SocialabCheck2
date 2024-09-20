from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

# Configurazione Selenium e browser
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    return driver

# Funzione per simulare una digitazione lenta
def slow_typing(element, text, delay_min=0.1, delay_max=0.3):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(delay_min, delay_max))  # Simula digitazione umana

# Funzione per il login su Instagram
def instagram_login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(random.uniform(5, 8))  # Attesa per il caricamento della pagina
    
    # Trova gli elementi per l'inserimento di username e password
    username_input = driver.find_element_by_name("username")
    password_input = driver.find_element_by_name("password")
    
    # Inserisci le credenziali con digitazione lenta
    slow_typing(username_input, username)
    time.sleep(random.uniform(2, 4))  # Ritardo casuale
    
    slow_typing(password_input, password)
    time.sleep(random.uniform(1, 3))  # Ritardo
    
    # Clicca sul pulsante di login
    password_input.send_keys(Keys.RETURN)
    time.sleep(random.uniform(8, 12))  # Attesa per il login

# Funzione per navigare al profilo e raccogliere informazioni
def get_last_post_date(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(random.uniform(5, 9))  # Attesa per il caricamento del profilo
    
    # Scorri la pagina per simulare l'interazione umana
    for _ in range(random.randint(1, 3)):  # Scroll casuale tra 1 e 3 volte
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))  # Pausa dopo lo scroll
    
    # Estrai la data dell'ultimo post
    try:
        # Trova la data del primo post nel profilo (potrebbe essere necessario trovare l'elemento corretto)
        post_date_element = driver.find_element_by_css_selector('time')  # Selettore per la data del post
        post_date = post_date_element.get_attribute("datetime")  # Estrai l'attributo datetime
        
        print(f"L'ultimo post di {username} è stato pubblicato il {post_date}")
        return post_date
    except Exception as e:
        print(f"Errore durante la raccolta dei dati per {username}: {e}")
        return None

# Funzione per simulare ritardi casuali
def random_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

# Funzione principale per eseguire il controllo su più profili
def monitor_profiles(username, password, profile_list):
    # Imposta il driver del browser
    driver = setup_driver()
    
    # Esegui il login su Instagram
    instagram_login(driver, username, password)
    
    # Controlla ogni profilo nella lista
    for profile in profile_list:
        print(f"Controllo il profilo: {profile}")
        post_date = get_last_post_date(driver, profile)
        if post_date:
            print(f"Ultimo post di {profile}: {post_date}")
        else:
            print(f"Non è stato possibile ottenere la data dell'ultimo post per {profile}")
        
        # Introduci un ritardo casuale prima di passare al profilo successivo
        random_delay(15, 30)  # Ritardo più lungo per sembrare naturale
    
    # Chiudi il browser alla fine
    driver.quit()

# Esempio di utilizzo
if __name__ == "__main__":
    # Dati di login e lista dei profili da monitorare
    instagram_username = "tuo_username_instagram"
    instagram_password = "tua_password_instagram"
    
    profiles_to_check = [
        "hotelbellavistacavalese", "olimpionicohotel", "fondazioneFiemmePer", 
        "spartansgymasd", "carpenteria_bonelli", "zambonilattonerie", "radiofiemme", 
        "socialabtrentino", "elcalderoncavalese"
    ]
    
    # Avvia il monitoraggio dei profili
    monitor_profiles(instagram_username, instagram_password, profiles_to_check)

                # Aggiornamento della barra di caricamento
                progress.progress((idx + 1) / total)
    else:
        st.error("Per favore, inserisci username e password validi.")
