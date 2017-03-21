# Si besoin generer une clef ssh

ssh-keygen

# Placer la clef publique dans le dossier (/!\ ne pas push sa clef sur git)

cp /home/<User>/.ssh/id_rsa.pub Path_to_repo/dockerTesting/

########################
Installer docker si nécessaire... (sur Ubuntu ajouter sudo si l'utilisateur n'a pas les droits pour docker).
########################

# build l'image docker à partir du Dockerfile

docker build -t eg_sshd .

# si besoin de supprimer le conteneur déja existant

docker rm -f test_sshd

# lancer un conteneur

docker run -d -P --name test_sshd eg_sshd

# vérifier le port hote correspondant au port 22 du docker

docker port test_sshd 22

# ssh vers le docker

ssh root@127.0.0.1 -p <numéro de port>


