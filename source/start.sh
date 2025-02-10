#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    gnome-terminal -- bash -c "python3 serveur.py; exec bash"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    osascript -e "tell application \"Terminal\" to do script \"cd $SCRIPT_DIR; python3 serveur.py\""

    sleep 0.5
else
    echo "Unsupported OS"
    exit 1
fi

python3 affichage.py&
python3 IA.py --equipe joueur1&
# python3 IA.py --equipe joueur2&
# python3 IAQuentin.py --equipe joueur3&
# python3 IAQuentin.py --equipe joueur4&