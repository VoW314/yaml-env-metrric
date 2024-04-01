# NASIM YAML GRADER
-----
by Shreyas B
Version 2
Last Updated: 2/6/24
-------------------------------------

## Classes

**Validation:** The validation class is responsible for validating the .yaml files before they are ready for grading. It checks all components of the yaml file to make sure that if run on NASIM, a proper environment can be made for the simulation. 

**Unpack:** The unpack class is responsible for unpacking from the .yaml files and converting them into more readable variables and types into which can be read in and graded.

---------

## Current Idea

The current Idea for how to grade this can be found in the ".cog" files in the project. 

The grader will grade mainly based off the number
of exploitable services, the costs of scans and exploits, and 
how much the network is segmented. 

#### Exploitable Services
Exploitable services includes: schtask, daclsvc, and tomcat. These are services that hosts have that can be exploited in the NASIM environment. Less exploitable services means that agents would likely have a longer initial learning time. 

#### Cost of Scans
This is a similar concept to our 2023 paper. 

#### Network Segmentation

More segmentation mean a smaller attack surface or potential entry points for an attacker attempting to breach the network environment. These calculations will also attempt to use how networks are connected to each other for the final grading.

For example: **If we are given the subnet array of [1,5,2]. Also the sensitive host is in subnet 3.** 

Subnet 1 is always the DMZ. If we were to connect the DMZ to 
the subnet 2 and 3 directly, then this would be less secure than just connecting the DMZ to subnet 2. This is due to the nature of the DMZ being a buffer zone between the internet and the internal network. 

---
### Updated Slides

https://docs.google.com/presentation/d/1SuRPHGwO-Lcoj1oZTQPTOEVT97nqyIbn7Nkk72cqkH0/edit?usp=sharing


----
### Related Repositories

This repository is currently a WIP that uses tensorflow to generate YAML environments to be validated by this repository. This would allow for more automated generation of YAML files. 
https://github.com/VoW314/yaml_environmental_generation 

------
### References

1) https://github.com/Jjschwartz/NetworkAttackSimulator/blob/master/nasim/scenarios/benchmark/medium-multi-site.yaml

2) https://networkattacksimulator.readthedocs.io/en/latest/tutorials/creating_scenarios.html

3) https://networkattacksimulator.readthedocs.io/en/latest/tutorials/scenarios.html

