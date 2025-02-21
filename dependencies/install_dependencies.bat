@echo off
setlocal enabledelayedexpansion

echo Installation des dépendances...
for %%f in (*.whl) do (
    echo Installation de %%f...
    python -m pip install --no-index --find-links=. %%f
)

echo Installation terminée !
pause
