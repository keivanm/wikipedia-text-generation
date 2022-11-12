# wikipedia-text-generation

Code for the experiments in my master thesis.

## Running the code

To run the code follow the instructions below. Keep in mind that the ```linkoping.pgf```file is the GF source code compiled into PGF in order to be used in the Python scripts. If you make any changes to the GF code you need to recompile the code into PGF as well. 

### Generating text for one urban area

To generate a text for an urban area, e.g. Stockholm, run the command

```python3 linkoping.py "Stockholm"```

### Generating text for 100 random urban areas

To generate the texts for 100 random urban areas as seen in the thesis, run the command

```python3 linkoping100_2.py```

Keep in mind that the script can fail because of various inconsistencies in the queried data. 


TODO: 
- Proper naming conventions: the naming in the code isn't the best and could use some work.
- Add grammars for names
