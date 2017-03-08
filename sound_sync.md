Sounds are uploaded to google cloud storage in a bucket called
'malia-speech.appspot.com' in the project called 'malia-speech'.

To sync them to a local dir:

One-time setup:

% make init_virtualenv
% make init_gsutil_auth
What is your project-id? malia-speech

To sync the files:

% make sync_sound_files
