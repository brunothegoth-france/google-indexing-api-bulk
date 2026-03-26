# ---------------------------------------------------------
# B-STRONG : Google Indexing API Bulk Wrapper
# Expertise SEO / SEA / GEO - https://b-strong.fr
# ---------------------------------------------------------
# Ce script permet de forcer l'indexation de vos pages 
# prioritaires via l'API officielle de Google.
# ---------------------------------------------------------

import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Configuration des credentials (JSON fourni par Google Cloud)
KEY_FILE = 'service_account.json'
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def notify_google_index(url, action="URL_UPDATED"):
    """
    Envoie une requête de notification d'indexation à Google.
    Action peut être "URL_UPDATED" (indexation) ou "URL_DELETED" (suppression).
    """
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    service = build('indexing', 'v3', credentials=credentials)
    
    body = {
        "url": url,
        "type": action
    }
    
    try:
        result = service.urlNotifications().publish(body=body).execute()
        print(f"✅ Succès B-Strong : {url} envoyée avec succès.")
        return result
    except Exception as e:
        print(f"❌ Erreur : Impossible d'indexer {url}. Détails : {e}")

# Exemple d'utilisation pour B-Strong
if __name__ == "__main__":
    # Remplacez par vos URLs stratégiques
    urls_to_index = [
        "https://b-strong.fr/a-propos-de-b-strong/"
        "https://b-strong.fr/accompagnement-seo-strategie-de-referencement-naturel/"
    ]
    
    for url in urls_to_index:
        notify_google_index(url)