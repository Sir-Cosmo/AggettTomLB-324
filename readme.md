# LB 324

# Tagebuch-App — CI/CD (Render)

**Live URL:** [https://aggetttomlb-324.onrender.com](https://aggetttomlb-324.onrender.com/)

## Branch-Konzept
- main: stets produktionsgleich; jeder Merge triggert eine Auslieferung (Render Deploy Hook)
- dev: stabil getesteter Code; PRs von feature/* nach dev
- feature/*: Entwicklungs-Äste pro Feature

## pre-commit verwenden
```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push



## Aufgabe 2
Erklären Sie hier, wie man `pre-commit` installiert.

## pre-commit verwenden

Installieren und Hooks aktivieren:
```bash
pip install pre-commit
pre-commit install                  # aktiviert commit-Hooks (Black, Ruff, isort)
pre-commit install --hook-type pre-push   # aktiviert push-Hook (pytest)
```
Hooks manuell ausführen:
```
pre-commit run --all-files   # format/lint über alle Dateien
pytest -q                    # Tests lokal starten
```


**Goal:** Every PR targeting `dev` runs tests, nothing else.

Create file **`.github/workflows/pr-tests.yml`**:

```yaml
name: PR tests (to dev)

on:
  pull_request:
    branches: [ "dev" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
```



## Aufgabe 4
Erklären Sie hier, wie Sie das Passwort aus Ihrer lokalen `.env` auf Azure übertragen.
Aufgabe 4 – Passwort sicher auf Render übertragen 

Hinweis zur Plattformwahl:
Da ich kein Guthaben für Azure zur Verfügung habe, habe ich die Anwendung auf Render deployed. Render bietet für diese LB dieselben benötigten Funktionen: Umgebungsvariablen (für PASSWORD/SECRET_KEY) als sichere Secrets, automatisches Deployment per Deploy Hook/GitHub Action auf main, sowie eine öffentliche URL für die laufende App. Die in der Aufgabe geforderten Schritte (Secrets übertragen, Auslieferung einrichten, automatisches Redeploy auf main) wurden entsprechend auf Render umgesetzt.

Meine App liest das Passwort über Umgebungsvariablen (os.getenv) ein. Lokal kommt es aus der .env, in Produktion (Render) wird es direkt in den Service-Einstellungen gesetzt. Die .env wird nicht mitgitten.

1) Lokal (.env) nur für Entwicklung

Lege im Projektordner eine Datei .env an:

PASSWORD="deinLokalesPasswort"
SECRET_KEY="lange_zufaellige_zeichenkette"


Stelle sicher, dass .env nicht committet wird (steht in .gitignore).

2) Produktion: Secrets in Render setzen

Öffne Render → dein Web Service → Environment.

Klicke Add Environment Variable und trage ein:

PASSWORD = dein GitHub-Benutzername (gemäß Aufgabenstellung)

SECRET_KEY = lange zufällige Zeichenkette

Save Changes und dann Deploy (oder Manual Deploy → Clear build cache & deploy).

Hinweis: In Produktion wird keine .env verwendet. Render stellt die Werte als echte Umgebungsvariablen bereit; der Code greift via os.getenv("PASSWORD") und os.getenv("SECRET_KEY") darauf zu.

3) Start-Befehl auf Render

In den Service-Einstellungen:

Build Command: pip install -r requirements.txt

Start Command: gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app

4) Funktion prüfen

App-URL öffnen (Render zeigt sie in der Service-Übersicht).

/login aufrufen und mit dem in Render gesetzten PASSWORD einloggen.

Ein Eintrag erstellen; die App sollte normal funktionieren.

5) (optional) Automatische Auslieferung von main

Wenn bei jedem Merge nach main automatisch ausgeliefert werden soll:

In Render Settings → Deploy Hooks → Create Deploy Hook (Branch main) und die URL kopieren.

In GitHub: Settings → Secrets and variables → Actions → New repository secret

Name: RENDER_DEPLOY_HOOK_URL

Value: (die kopierte Hook-URL)

Das Workflow-File .github/workflows/deploy-on-main.yml triggert dann bei jedem Push auf main eine Auslieferung.

