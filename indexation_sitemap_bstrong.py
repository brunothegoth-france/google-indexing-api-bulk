# ---------------------------------------------------------
# B-STRONG : Google Indexing API - Sitemap Automation v2
# Expertise SEO / SEA / GEO - https://b-strong.fr
# ---------------------------------------------------------
# Améliorations v2 :
#   - Gestion automatique des sitemap index (récursif)
#   - Limite de 150 URLs/jour (marge sur quota Google 200)
#   - Filtrage par date de modification (lastmod)
#   - Délai entre requêtes pour éviter les erreurs 429
#   - Rapport complet en fin de session
#   - Export CSV horodaté
# ---------------------------------------------------------

import requests
import xml.etree.ElementTree as ET
import csv
import time
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------------------------------------------------------
# CONFIGURATION — À modifier selon vos besoins
# ---------------------------------------------------------

KEY_FILE      = 'service_account.json'
SITEMAP_URL   = 'https://b-strong.fr/sitemap.xml'
SCOPES        = ["https://www.googleapis.com/auth/indexing"]

MAX_URLS      = 150        # Limite journalière (quota Google = 200, marge de sécurité)
DELAY         = 0.5        # Secondes entre chaque requête (évite les erreurs 429)
FILTER_DAYS   = None       # Nombre de jours pour filtrer par lastmod (None = toutes les URLs)

# ---------------------------------------------------------
# LECTURE DU SITEMAP (récursif pour sitemap index)
# ---------------------------------------------------------

def get_urls_from_sitemap(url, days_filter=None):
    """
    Extrait toutes les URLs d'un sitemap ou sitemap index.
    Gère automatiquement la récursion sur les sous-sitemaps.
    Si days_filter est défini, ne retourne que les URLs modifiées récemment.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Détection sitemap index
        sub_sitemaps = [loc.text for loc in root.findall('.//ns:sitemap/ns:loc', namespace)]

        if sub_sitemaps:
            print(f"\n📂 Sitemap index détecté — {len(sub_sitemaps)} sous-sitemap(s) trouvé(s) :")
            all_urls = []
            for sub in sub_sitemaps:
                print(f"   ↳ Lecture : {sub}")
                all_urls += get_urls_from_sitemap(sub, days_filter)
            return all_urls

        # Sitemap classique : extraction des URLs avec filtre lastmod optionnel
        cutoff = datetime.now() - timedelta(days=days_filter) if days_filter else None
        urls = []

        for url_el in root.findall('.//ns:url', namespace):
            loc     = url_el.find('ns:loc', namespace)
            lastmod = url_el.find('ns:lastmod', namespace)

            if loc is None:
                continue

            if cutoff and lastmod is not None:
                try:
                    mod_date = datetime.fromisoformat(lastmod.text[:10])
                    if mod_date < cutoff:
                        continue  # URL trop ancienne, on passe
                except ValueError:
                    pass  # Impossible de parser la date, on inclut quand même

            urls.append(loc.text)

        return urls

    except requests.RequestException as e:
        print(f"❌ Erreur réseau lors de la lecture du sitemap {url} : {e}")
        return []
    except ET.ParseError as e:
        print(f"❌ Erreur de parsing XML pour {url} : {e}")
        return []


# ---------------------------------------------------------
# NOTIFICATION D'INDEXATION
# ---------------------------------------------------------

def notify_google_index(url, service):
    """
    Envoie une notification URL_UPDATED à l'API Google Indexing.
    Retourne True en cas de succès, False en cas d'erreur.
    """
    body = {"url": url, "type": "URL_UPDATED"}
    try:
        service.urlNotifications().publish(body=body).execute()
        print(f"  ✅ {url}")
        return True
    except Exception as e:
        print(f"  ❌ {url}")
        print(f"     Détail : {e}")
        return False


# ---------------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------------

def export_rapport_csv(success_urls, error_urls):
    """
    Exporte un fichier CSV horodaté avec le résultat de chaque URL.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename  = f"rapport_indexation_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Statut", "Date"])
        for url in success_urls:
            writer.writerow([url, "Succes", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        for url in error_urls:
            writer.writerow([url, "Erreur", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    print(f"\n💾 Rapport exporté : {filename}")
    return filename


# ---------------------------------------------------------
# PROGRAMME PRINCIPAL
# ---------------------------------------------------------

def main():

    print("=" * 55)
    print("  B-STRONG — Google Indexing API v2")
    print("  https://b-strong.fr")
    print("=" * 55)

    # 1. Authentification
    print("\n🔑 Authentification en cours...")
    try:
        credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
        service     = build('indexing', 'v3', credentials=credentials)
        print("   Authentification réussie.")
    except Exception as e:
        print(f"❌ Impossible de s'authentifier : {e}")
        return

    # 2. Récupération des URLs
    print(f"\n🌐 Lecture du sitemap : {SITEMAP_URL}")
    if FILTER_DAYS:
        print(f"   Filtre actif : URLs modifiées dans les {FILTER_DAYS} derniers jours.")

    urls = get_urls_from_sitemap(SITEMAP_URL, FILTER_DAYS)

    if not urls:
        print("\n📭 Aucune URL trouvée. Vérifiez l'URL du sitemap et votre connexion.")
        return

    total_found = len(urls)
    print(f"\n🔍 {total_found} URL(s) détectée(s) au total.")

    # 3. Application de la limite journalière
    if total_found > MAX_URLS:
        print(f"⚠️  Limite journalière appliquée : {MAX_URLS} URLs sur {total_found} seront soumises.")
        print(f"   Relancez demain pour traiter les {total_found - MAX_URLS} URL(s) restante(s).")
        urls = urls[:MAX_URLS]
    
    print(f"\n🚀 Lancement de l'indexation pour {len(urls)} URL(s)...\n")

    # 4. Boucle d'indexation
    success_urls = []
    error_urls   = []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]", end=" ")
        result = notify_google_index(url, service)

        if result:
            success_urls.append(url)
        else:
            error_urls.append(url)

        if i < len(urls):
            time.sleep(DELAY)

    # 5. Rapport final
    print("\n" + "=" * 55)
    print("  RAPPORT D'INDEXATION B-STRONG")
    print("=" * 55)
    print(f"  URLs détectées   : {total_found}")
    print(f"  URLs soumises    : {len(urls)}")
    print(f"  Succes           : {len(success_urls)}")
    print(f"  Erreurs          : {len(error_urls)}")
    print(f"  Quota restant    : ~{MAX_URLS - len(urls)} notifications aujourd'hui")

    if error_urls:
        print("\n  URLs en erreur :")
        for url in error_urls:
            print(f"    → {url}")

    # 6. Export CSV
    export_rapport_csv(success_urls, error_urls)

    print("\n✅ Session terminée. Vérifiez la Search Console dans 24-48h.")
    print("=" * 55)


if __name__ == "__main__":
    main()
