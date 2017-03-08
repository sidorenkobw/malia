init_virtualenv:
	mkdir -p env
	virtualenv env
	env/bin/pip install -f requirements.txt

# Login protocol. Writes to ~/.boto
init_gsutil_auth:
	env/bin/gsutil config

update_virtualenv:
	env/bin/pip install -f requirements.txt

sync_sound_files:
	mkdir -p sounds
	env/bin/gsutil rsync -d -r gs://malia-speech.appspot.com/ sounds/
