from selenium import webdriver
from google.cloud import bigquery
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Spécifiez les options pour se connecter à Selenium Grid

option = webdriver.ChromeOptions()

# Remplacez l'URL ci-dessous par l'URL de votre hub Selenium Grid
grid_url = 'http://10.188.72.37:4444/wd/hub'

driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=DesiredCapabilities.CHROME, options=option)

# Instanciation du pilote Selenium avec Selenium Grid
# driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)


driver.get('https://www.linkedin.com')

wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.presence_of_element_located((By.ID, 'session_key')))
username_input.send_keys('elianalyse3@gmail.com')
password_input = driver.find_element(By.ID, 'session_password')
password_input.send_keys('Eliana07@')

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
login_button.click()

driver.get('https://www.linkedin.com/company/avisia/mycompany/coworkercontent')

SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_count = 10

for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

##############################

post_messages = []

message_elements = driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2__description-wrapper')
voir_plus_links = driver.find_elements(By.XPATH, ".//span[contains(text(), '…voir plus')]")

# Collecter tous les textes des publications
post_messages = [element.text for element in message_elements]

# Cliquer sur les boutons "voir plus" en séquence
for link in voir_plus_links:
    driver.execute_script("arguments[0].click();", link)
    time.sleep(1)

# Mettre à jour les messages avec le texte complet, si disponible
full_text_elements = driver.find_elements(By.CLASS_NAME, 'feed-shared-inline-show-more-text')
for i, element in enumerate(full_text_elements):
    post_messages[i] = element.text

# Afficher les messages
for message in post_messages:
    print(message)
    print('------------------------')

##############################

post_messages_filtred = []

for message in post_messages:
    if "AVISIA" in message.upper() or "AVISIA" in message.lower() or "#AVISIA" in message.upper() or "#AVISIA" in message.lower() or "#Avisia" in message:
        post_messages_filtred.append("OUI")
    else:
        post_messages_filtred.append("NON")
        
#############################


post_messages_filtred_challenge = []


for message2 in post_messages:
    if "AVISIAFACE" in message2.upper() or "Avisiaface" in message2.lower() or "#AVISIAFACE" in message2.upper() or "#Avisiaface" in message2.lower() or "#Avisiaface" in message2 or "#AvisiaFace" in message2 :
        post_messages_filtred_challenge.append("OUI")
    else:
        post_messages_filtred_challenge.append("NON")

for resultat2 in post_messages_filtred_challenge:
    print(resultat2)
        
##############################


personnes = []

for j in range(80):
    try:
        personne_element = driver.find_elements(By.CLASS_NAME, 'update-components-actor__title')[j]
        personne = personne_element.text.split('\n')[0]  # Récupérer uniquement la première ligne du texte
        personnes.append(personne)  
    except IndexError:
        print("Terminé")
        
#############################   

profiles = []

for j in range(80):
    try:
        profile_element = driver.find_elements(By.CLASS_NAME, 'update-components-actor__description')[j]
        profile = profile_element.text.split('\n')[0]  # Récupérer uniquement la première ligne du texte
        profiles.append(profile)  
    except IndexError:
        print("Terminé")
        
#############################   


likes = []
publications = driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2')

for i in range(min(len(publications), 80)):
    publication = publications[i]
    
    like_element_int = publication.find_elements(By.CLASS_NAME, 'social-details-social-counts__reactions-count')
    like_element_text = publication.find_elements(By.CLASS_NAME, 'social-details-social-counts__social-proof-text')
    
    if len(like_element_int) > 0:
        likes.append(int(like_element_int[0].text))
    elif len(like_element_text) > 0:
        text = like_element_text[0].text
        if "et" in text:  # Vérifie si le texte contient "et"
            Like2_number = int(''.join(filter(str.isdigit, text))) + 1
            likes.append(Like2_number)
        else:
            likes.append(int(text))
    else:
        likes.append(0)
        
############################# 

commentaires = []
publications = driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2')

for i in range(min(len(publications), 80)):
    publication = publications[i]
    commentaire_element = publication.find_elements(By.CLASS_NAME, 'social-details-social-counts__comments')  
    if len(commentaire_element) > 0:
        for commentaire in commentaire_element:
            text = commentaire.text
            commentaires.append(''.join(filter(str.isdigit, text)))
    else:
        commentaires.append("0")
        
#############################   


photoprofile = []

for j in range(80):
    try:
        photo_element = driver.find_elements(By.CLASS_NAME,'update-components-actor__avatar-image')[j]
        photo_url = photo_element.get_attribute('src')  # Récupérer la valeur de l'attribut 'src'update-components-actor__avatar-image
        photoprofile.append(photo_url)
    except IndexError:
        print("Terminé")

############################# 


from datetime import datetime, timedelta

dates = []

# Obtention de la date actuelle
date_actuelle = datetime.now().date()

for j in range(80):
    try:
        date_element = driver.find_elements(By.CLASS_NAME, 'update-components-actor__sub-description')[j]
        duree_relative = date_element.text.split('\n')[0]

        # Estimation de la date de publication en fonction de la durée relative
        if 'h' in duree_relative:
            heures = int(duree_relative.split()[0])
            date_publication = date_actuelle - timedelta(hours=heures)
        elif 'j' in duree_relative:
            jours = int(duree_relative.split('j')[0].strip())
            date_publication = date_actuelle - timedelta(days=jours)
        elif 'sem.' in duree_relative:
            semaines = int(duree_relative.split('sem.')[0].strip())
            date_publication = date_actuelle - timedelta(weeks=semaines)
        elif 'mois' in duree_relative:
            mois = int(duree_relative.split('mois')[0].strip())
            date_publication = date_actuelle - timedelta(days=mois * 30)

        date_formattee = date_publication.strftime("%Y-%m-%d")
        dates.append(date_formattee)
    except IndexError:
        print("Terminé")
        
#############################

# Créer une liste de tuples contenant le message et le résultat du filtrage
data_to_export = list(zip(personnes,post_messages,profiles,post_messages_filtred,post_messages_filtred_challenge,likes,commentaires,photoprofile,dates))

# Configuration de l'accès à BigQuery
project_id = 'avisia-fivetran-sandbox'
dataset_id = 'View_SL'
table_name = 'Testee'

# Charger les données dans BigQuery
client = bigquery.Client(project=project_id)
dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_name)

schema = [
    bigquery.SchemaField("Personne", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Message", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Profil", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AVISIA", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("AVISIAFACE", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Likes", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Commentaires", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("Photo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("Dates", "DATE", mode="NULLABLE"),

]

job_config = bigquery.LoadJobConfig(schema=schema, write_disposition="WRITE_TRUNCATE")

data_to_export_dict = []
for personne,message,profil,avisia, avisiaface,like, commentaire, photo, date in data_to_export:
    data_to_export_dict.append({
        
        "Personne": personne,
        "Message": message,
        "Profil": profil,
        "AVISIA": avisia,
        "AVISIAFACE": avisiaface,
        "Likes": like,
        "Commentaires": commentaire,
        "Photo": photo,
        "Dates": date
    })

# Charger les données dans BigQuery
job = client.load_table_from_json(data_to_export_dict, table_ref, job_config=job_config)
job.result()
print("Les données sont bien chargé sur bigquery")
