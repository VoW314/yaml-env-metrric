# NASIM YAML GRADER

by Shreyas
version 1
-------------------------------------

## Class 

The ["Hardness Class"](https://github.com/VoW314/yaml-env-metrric/blob/main/hardness_class.py)takes in a .yaml file and reads it in for grading. It currently just does one file at a time. The code creates a grade based off the values within the topology of the 2D array. It does require that the headers of each dictionary are properly written but the order of parts of the file does not matter. 



More information ["Here"]([https://docs.google.com/presentation/d/1XRaDJQtkY0n9DoOsXBn5KaGmi1GaTiuPHxKL4vHgLPo/edit?usp=sharing](https://docs.google.com/presentation/d/1zNz78BoZ65SwHJPfSkeVozT-rVMClB7pXzyeMHtYEvE/edit?usp=sharing))

## The Kernel

below is the closest image explanation I could find online of what I designed: ![plus kernel](https://www.researchgate.net/publication/370331269/figure/fig2/AS:11431281176001065@1689992480753/Decomposed-calculation-of-cross-shaped-kernel_Q320.jpg)

--------------------------------

## Current Ideas

My current idea is to assign the arbitrary values earlier to the actual costs of "hacking" the host
This of course will require more work and developing a way to actually read from the file what a host does

For example: if we want to get through (1,0) on the medium.yaml file

the .yaml tells us:
``` os: linux
 services: [http]
 processes: []
 ```

the cost of a http exploit: 
```
 e_http:
    service: http
    os: None
    prob: 0.9
    cost: 2
    access: user
```

There is also no firewall on (1, 0)

so we would give the host at (1, 0) a difficulty factor of 2 as the total cost to get through it on 1 try
would be a 2. Also you could bring in the entire chances/probablility aspect. 

There are many ways to grade this. 
