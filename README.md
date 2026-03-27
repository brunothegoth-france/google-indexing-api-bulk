# 🚀 Google Indexing API Bulk & Sitemap - by B-Strong

![SEO](https://img.shields.io/badge/Expertise-SEO-blue) ![GEO](https://img.shields.io/badge/Expertise-GEO-green) ![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen) ![Version](https://img.shields.io/badge/Version-2.0-orange)

Bienvenue sur l'outil d'indexation haute performance développé par l'agence **B-Strong**.
Cet outil permet de forcer l'indexation de vos contenus par Google en quelques secondes, court-circuitant les délais habituels de crawl (plusieurs jours/semaines).

---

## 🛠️ Deux modes d'indexation pour votre croissance

Ce repository contient deux scripts adaptés à vos besoins de performance :

1. **`indexation_bstrong.py` (Mode Unitaire) :** Idéal pour indexer précisément une liste d'URLs stratégiques (nouvelles Landing Pages, articles chauds).
2. **`indexation_sitemap_bstrong.py` (Mode Automatique v2) :** Scanne l'intégralité de votre `sitemap.xml` — y compris les sitemap index — et soumet toutes vos pages à Google en un seul clic.

---

## ✨ Pourquoi l'utiliser en 2026 ?

* **Vitesse :** Réduisez le temps d'indexation de 90%.
* **SEO Technique :** Assurez-vous que vos mises à jour (balises meta, contenu) sont prises en compte immédiatement.
* **GEO (Generative Engine Optimization) :** Soyez le premier cité par les IA (Gemini, SGE) en garantissant la fraîcheur de votre indexation.

---

## 🆕 Nouveautés v2 — Mode Automatique

| Fonctionnalité | Détail |
|---|---|
| 🗂️ Sitemap index récursif | Dépile automatiquement tous les sous-sitemaps |
| 🛡️ Limite quota sécurisée | 150 URLs/jour (marge sur le quota Google de 200) |
| ⏱️ Délai anti-429 | Pause de 500ms entre chaque requête |
| 📅 Filtre par lastmod | Option pour n'indexer que les pages modifiées récemment |
| 📊 Rapport terminal | Résumé complet succès / erreurs en fin de session |
| 💾 Export CSV horodaté | Fichier `rapport_indexation_YYYYMMDD_HHMM.csv` généré automatiquement |

---

## 🚀 Installation & Utilisation

### 1. Prérequis

* Python 3.x installé.
* Un fichier `service_account.json` (Clé API Google Cloud) placé dans le même dossier que le script.
* Accès **Propriétaire** sur la Google Search Console du site cible.
* L'**Indexing API** activée sur Google Cloud Console.

### 2. Installation des dépendances
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests
```

### 3. Configuration

Ouvrez `indexation_sitemap_bstrong.py` et modifiez uniquement ces variables :
```python
SITEMAP_URL  = 'https://votresite.com/sitemap.xml'  # URL de votre sitemap
MAX_URLS     = 150       # Limite journalière (ne pas dépasser 200)
DELAY        = 0.5       # Secondes entre chaque requête
FILTER_DAYS  = None      # None = toutes les URLs | 7 = modifiées cette semaine
```

### 4. Lancement
```bash
cd H:\Python\Indexing
py indexation_sitemap_bstrong.py
```

### 5. Résultat attendu
```
📂 Sitemap index détecté — 3 sous-sitemap(s) trouvé(s)
   ↳ Lecture : page-sitemap.xml
   ↳ Lecture : glossary-sitemap.xml
   ↳ Lecture : category-sitemap.xml

🔍 147 URL(s) détectée(s) au total.
🚀 Lancement de l'indexation...

[1/147] ✅ https://votresite.com/page-1/
[2/147] ✅ https://votresite.com/page-2/
...

══════════════════════════════════════════
  RAPPORT D'INDEXATION B-STRONG
  URLs soumises  : 147
  Succès         : 147
  Erreurs        : 0
💾 Rapport exporté : rapport_indexation_20260327_1430.csv
```

---

## ⚠️ Points de vigilance

* **Quota Google :** L'API Indexing est limitée à **200 notifications/jour** par projet Google Cloud. Le script est configuré à 150 pour conserver une marge de sécurité.
* **service_account.json :** Ne commitez jamais ce fichier sur GitHub. Il est protégé par le `.gitignore`.
* **Droits Search Console :** Un accès simple ne suffit pas — le compte de service doit avoir le rôle **Propriétaire**.

---

## 📁 Structure du projet
```
Indexing/
│
├── indexation_bstrong.py           # Mode unitaire — liste d'URLs manuelle
├── indexation_sitemap_bstrong.py   # Mode automatique v2 — sitemap complet
├── service_account.json            # ⚠️ Non versionné (.gitignore)
├── rapport_indexation_*.csv        # Rapports générés automatiquement
└── README.md
```

---

## 🤝 Contact B-Strong

| | |
|---|---|
| 🌐 Site | [b-strong.fr](https://b-strong.fr) |
| 📧 Email | contact@b-strong.fr |
| 💼 LinkedIn | [linkedin.com/company/b-strong-marketing-digital](https://linkedin.com/company/b-strong-marketing-digital) |

*Besoin d'un accompagnement sur mesure pour industrialiser l'indexation, auditer votre visibilité ou renforcer vos performances sur Google ? Parlons-en.*
docs: mise à jour README v2 - nouvelles fonctionnalités sitemap automation
