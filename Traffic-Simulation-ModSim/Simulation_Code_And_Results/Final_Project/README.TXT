About the Project
-------------------------
	The entry of the Simulation models is:
		Run_Simulation_Experiments.py

	Three kinds of evaluations are performed:
		1) Synchronized
		2) Unsynchrnized
		3) Unsynchronized With Spillover

How to Run the Code
-------------------------------
	python Run_Simulation_Experients.py

	Run_Simulation_Experients.py imports three different scripts:
		1) Process_Synchronized.py
		2) Process_Unsynchronized_backup.py
		3) Process_Unsynchronized_And_Spillover.py

	Just uncomment the process you want to run and comment others in Run_Simulation_Experients.py
	Note: Although the methodology and approach remains the same for all the methods and files, please refer Process_Synchronized.py code as it is clean, expressive and most important.	


About the Code/Approach and Important Methods
-----------------------------------------------------------------------
	Definitely Priority Queues are used to perform entire Simulation. Although, we have created our own 	code for Priority Queue and it is working but we have used Python's inbuilt Priority Queue
 	Implementation for performance boost as we run 500 simulations with spillover.

	Important Methods:
	---------------------------
	1) FELqueueing : FEL generator for each previous FEL and state variables and other dependencies 
	based on Simulation Engine/Even handler
	2) simulatingOneEntireTrip : Basically serving each FEL/Queue and updating the state variables
	3) Simulation_Engine: Main Event handler
	4) maintainTurns : Maintain turnings with given rates from NGSIM data
	5) trafficSim : Initial FEL handler/generator
	6) processBasedSimulation : Main method, basically entry to the code
	
Approach:
--------------
processBasedSimulation calls trafficSim method which actually generates FEL with arrival events of each vehicle with a time stamp for the entire simulation period (including vehicles from sides). Once all the vehicles are gathered to be served with their individual time stamp, Simulation_Engine method is called which starts the process oriented simulation and serves vehicle by vehicle for each FEL, handles/updates the state variables using simulationOneEntireTrip (basically on FEL as we have multiple FEL, which also get updated during the course of simulation). The simulatingOneEntireTrip uses FELqueueing method which is the last method and performsy each entity.


Supporting Files
----------------------
1) creatingFutureEventLists: Used in the main method
2) genRandVel: Generates random velocities based on our inbuilt velocity generation baed on the NGSEM data
3) globalVariables: Initializes all the global variables
4) vehicleProperties: Calls vehicle properties which are then used in FEL population/arrival events
5) replace_file: A util method to maintain the output.

Experimentation
----------------------
	Total of 500 simulations are run before making a significant conclusions and performing analysis.

Output
----------
	Each experiment's results are stored in corresponding experiment folder: 
		synchronized
		unsynchronized
		unsynchronized_spillover
