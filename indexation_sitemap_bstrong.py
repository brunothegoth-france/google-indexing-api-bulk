# ---------------------------------------------------------
# B-STRONG : Google Indexing API - Sitemap Automation
# Expertise SEO / SEA / GEO - https://b-strong.fr
# ---------------------------------------------------------
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
KEY_FILE = 'service_account.json'
SITEMAP_URL = 'https://b-strong.fr/sitemap.xml' # À remplacer par le vôtre
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_urls_from_sitemap(url):
    """Extraire toutes les URLs d'un sitemap XML."""
    try:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        # Gestion des namespaces XML fréquents dans les sitemaps
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls
    except Exception as e:
        print(f"❌ Erreur lecture Sitemap : {e}")
        return []

def notify_google_index(url, service):
    """Envoie la requête d'indexation."""
    body = {"url": url, "type": "URL_UPDATED"}
    try:
        service.urlNotifications().publish(body=body).execute()
        print(f"✅ Indexation demandée : {url}")
    except Exception as e:
        print(f"⚠️ Erreur pour {url} : {e}")

def main():
    # 1. Authentification
    print("🔑 Authentification B-Strong en cours...")
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    service = build('indexing', 'v3', credentials=credentials)

    # 2. Récupération des URLs
    print(f"🌐 Lecture du sitemap : {SITEMAP_URL}")
    urls = get_urls_from_sitemap(SITEMAP_URL)
    
    if not urls:
        print("📭 Aucune URL trouvée.")
        return

    print(f"🚀 {len(urls)} URLs détectées. Lancement de l'indexation...")

    # 3. Boucle d'indexation
    for url in urls:
        notify_google_index(url, service)

if __name__ == "__main__":
    main()