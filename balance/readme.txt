Document d�finissant le contenu de chaque fichier et sous-r�pertoire inclus:

1) /Balance
	. Dossier contenant les codes n�cessaires � la transmission du poids via une communication bluetooth. 

2) script_uuid_server.sh
	. script d'ex�cution de l'application Balance.
	. Permet de d�sassocier le smartphone du client.
	. Lance le script python Bluetooth_Balance.py

3) Bluetooth_Balance.py
	. G�re la connexion d'un client au caddie.
	. R�cup�re la valeur du poids en sortie de la ch�ine de mesure via une communication SPI (cf Rapport final)
	. Transmet le poids du caddie � l'application android du smartphone.