# Project

### Requirements
* I have attached an environment.yml file in this repo.
* You need to create an Anaconda environment from that file.

### Steps
* Step 1 - Open anaconda navigator and click on environments
* Step 2 - Click on import located on the bottom of the screen
* ![alt text](http://url/to/img.png)
* Step 3 - Give the environment a new name and click the folder icon and select the environment.yml file you exported in the last section
* Step 4 - Then click import and wait a few minutes and the environment will be imported along with it’s dependencies.
* ![alt text](http://url/to/img.png)


### Training the model
* Run the preprocess.py file. Command to run - python preprocess.py
* Running the above python file, would create dictionaries and training and validation dialogues in /data/ directory
* Now run the train.py file. Command to run - python train.py (after running this command, model checkpoints would be generated in /model/model/ directory)
* Now run the test.py file. Command to run - python test.py (after running this command, two more files would be generated in /data/ directory)
* Now run the results.py file. (You would receive results after this)
