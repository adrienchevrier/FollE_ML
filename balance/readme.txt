Document définissant le contenu de chaque fichier et sous-répertoire inclus:

1) /Balance
	. Dossier contenant les codes nécessaires à la transmission du poids via une communication bluetooth. 

2) script_uuid_server.sh
	. script d'exécution de l'application Balance.
	. Permet de désassocier le smartphone du client.
	. Lance le script python Bluetooth_Balance.py

3) Bluetooth_Balance.py
	. Gère la connexion d'un client au caddie.
	. Récupère la valeur du poids en sortie de la châine de mesure via une communication SPI (cf Rapport final)
	. Transmet le poids du caddie à l'application android du smartphone.