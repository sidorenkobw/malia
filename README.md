# Malia Speech
A web app for helping people with disabilities to be understood by the others

Tensorboard Visualization

  1. Logfile is being saved on line 130 of train.py with:
    callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    and the log file for each run for train is saved in 'malia/logs'.
  2. The tensorboard is already installed in env of malia, so the command:
    env/bin/tensorboard --logdir=logs
    in the shell takes log files from the directory 'malia/logs', and visualizes on Tensorboard.
  3. Go to localhost:6006 to look at the visualization of tensorboard.
  
  *It can helpful to modify the neural network layer to 5 in line 14 of speechmodel.py in order to understand how the neural network is working.
