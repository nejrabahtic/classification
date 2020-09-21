## Script for text classification

For running the script alone, without using GUI, you need to have `python3`, `nltk` installed. Moreover, the data set should be added accordingly.

```./readData.py``` will execute the script, and show you the results in the terminal or command line.

## Basic GUI

Running the GUI version requires more packages installed. Therefore, you will have to install `flask`, together with `python3` and `nltk`.
The main script for running the server is `run.py`. However, everything that is required for running it, is defined in `__init__.py` script. `__init__.py` also contains initialization of the dictionary and messages variables, as global. 

```./run.py``` will open the server on (http://127.0.0.1:5000/)
