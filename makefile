VIRTUALENV=virtualenv
NPM=npm
NODE=nodejs
PHP=php

init_packages:
	sudo apt-get install graphviz

init_virtualenv:
	mkdir -p env
	$(VIRTUALENV) env
	env/bin/pip install -r requirements.txt

# requirements.txt asks for a gpu-using tensorflow build. Follow with
# this to downgrade to the cpu one.
turn_off_tensorflow_gpu:
	env/bin/pip install tensorflow

# Login protocol. Writes to ~/.boto
init_gsutil_auth:
	env/bin/gsutil config

update_virtualenv:
	env/bin/pip install -r requirements.txt

sync_sound_files:
	mkdir -p sounds
	env/bin/gsutil rsync -d -r gs://malia-speech.appspot.com/ sounds/

update_js_packages:
	$(NPM) install

update_bower_components:
	mkdir -p public_html/lib/bower_components
	$(NODE) node_modules/bower/bin/bower install

run_learn_server:
	env/bin/python learn/server.py

run_php_server:
	(cd public_html; $(PHP) -S localhost:9999)

record_timelapse:
	ffmpeg -framerate .1 -f x11grab -s 1920,1080 -i :0.0+0,0 -vf settb=\(1/30\),setpts=N/TB/30 -r 30 -vcodec libx264 -crf 0 -preset ultrafast -threads 0 makeathon-timelapse-`date +%s`.mkv
