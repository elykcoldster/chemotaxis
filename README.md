A simulation framework for *Drosophila* larvae chemotaxis in the presence of an odor gradient. This framework is an implementation of the model described by Davies et al., and also extends that model with new mechanisms from Schulze et al.

Paper with the original model that we are extending: [A Model of Drosophila Larva Chemotaxis](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004606)  
Paper with the extensions (detailed concentration detection mechanisms): [Dynamical feature extraction at the sensory periphery guides chemotaxis](https://elifesciences.org/content/4/e06694)  

# Setting Up 
The simulation is written for Python 3. It depends on multiple packages. To easily install the packages, we recommend that you use either [Anaconda for Python 3](https://www.continuum.io/downloads) or [pip](https://pip.pypa.io/en/stable/installing/). If you choose to use pip, we highly recommend you use [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) for a clean installation.

The first step is to clone the repository:
```
git clone https://github.com/elykcoldster/chemotaxis.git
cd chemotaxis
```
Then continue setting up using option (1) or (2), as discussed above:
## (1) With Anaconda
Use conda to create a new environment with all the required packages:
```
conda create -n chemotaxis_env --file requirements.txt
```
## (2) With pip + virtualenv
**NOTE:** These instructions are written for Ubuntu, however they should work with minimal modifications for other operating systems.
Create and activate a virtual environment:
```
virtualenv venv
source venv/bin/activate
```
Install all of the required packages for the simulator:
```
pip install -r pip_requirements.txt
```
If you are on Ubuntu, you may need to install python3-tk:
```
sudo apt-get install python3-tk
```
# Running
To start the simulator, simply use:
```
python main.py
```
This will begin the interactive simulator, where you can give it commands. To view a list of commands and how to use them, use the "h" command.

Over the course of your experiments, you may find it cumbersome to type the same commands over and over again. Thus, you can place those same commands that you would normally type interactively into a a file such as "experiment.in", with each command on a separate line, and run the simulator like so:
```
python main.py -f experiment.in
```
This will start the simulator and run all of the commands in "experiment.in"
