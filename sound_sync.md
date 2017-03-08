Sounds are uploaded to google cloud storage in a bucket called 'malia-speech.appspot.com' in the project called 'malia-speech'.

To sync them to a local dir:

One-time setup:

% mkdir sounds
% mkdir env
% virtualenv env
% env/bin/pip install gsutil

% env/bin/gsutil config
What is your project-id? malia-speech

To sync the files:

% env/bin/gsutil rsync -d -r gs://malia-speech.appspot.com/ sounds/
