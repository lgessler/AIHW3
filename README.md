# HW3 for AI (CS 4710) at UVa, Spring 2015.
Authors: 

* Minh Nguyen (mqn2at@virginia.edu)
* Luke Gessler (ldg3fa@virginia.edu)

##USAGE
Enter driver.py and instantiate desired negotiators in the list `negotiators`.

From the shell, execute

    $ python3 driver.py {5,7,10,20}
    
##UPDATE
Our bot placed second in a class-wide, round-robin tournament!

    csh7kd	1543
    **mqn2at	1496**
    sp2cd	1443
    mmk4jq	1121
    mrs3fu	975
    apn4zaV2	975
    iam6ep	966
    gjv2wu	921
    jpm4bd	921
    zw2rf	912
    
The agent we submitted was [this one](https://github.com/lgessler/AIHW3/blob/master/submission/mqn2at_negotiator.py). Go team!

##FILE MANIFEST

Provided Files:
* negotiator_base.py
* negotiator_framework.py

Class Files:
* naive_negotiator.py
* accommodating_negotiator.py
* test_negotiators.py
  * Contains many negotiators.
    
Automation Files:
* csvgen.py
  * Used for automated generation of CSV files
* driver.py
  * Used for automated "fighting" of negotiators in the sanctioned way.

Data Files/Directories:
* 5-items/
* 7-items/
* 10-items/
* 20-items/
* test_cases/
* words
  * A *NIX file we included here.

##LICENSE
This code is released under a Sam License. You can feel free to use this code for whatever you want, with the following stipulations:

1. This code cannot be used in any product that is sold
2. You must reference the authors if you use this code
3. Don't use this code to cheat.

Copyright Luke Gessler and Minh Nguyen, 2015
