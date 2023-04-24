# webove_skrabadlo
dynamic web scrapper

Jak nainstalovat Plawright na MS Windows (Python):

Playwright python dokumentace:
1. https://playwright.dev/python/docs/intro

Prerekvizity:
1. VS Code -> https://code.visualstudio.com/download
2. Python -> https://www.python.org/downloads/ (při instalaci přidat do PATH!!!)

Instalace:
1. ve VS Code otevřít cílovou složku a v ní terminál
2. optional: možnost využití virtuálního prostředí venv (vhodné při práci s více projekty/verzemi)
3. pip install playwright
4. playwright install
5. dle požadavku na synchroní/asynchroní kód můžeme začít psát

Vývojářský deník:
1. První problém na který jsem narazil, byla sugestivnost playwright dokumentace do práci v javascriptu->
okamžitě nabízí instalaci pomocí npm bez zobrazení alternativ (př. pip), tudíž jsem nejdříve nabyl názoru, že
princip práce playwright s pythonem spočívá na vnitřní konverzi či vnitřího API python->js v rámci vs code extension, později 
zjišťuji, že existuje playwright/python dokumentace, kde nalézám požadovaný postup pro python playwright.
