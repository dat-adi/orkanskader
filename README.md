<div align="center">
 <img alt="orkanskader" height="200px" src="./assets/orkanskader-logo.png">
</div>

# Orkanskader

Harnessing data to forecast hurricane impact and financial losses.

### About
**_orkanskader_**, a term for "hurricane damage" in Norwegian, is a project intent on analyzing the radial impact of hurricanes based on historical data.

The project consists of a couple of segments,
1. estimating the radial impact of hurricanes based on historically observed data.
2. mapping the affected areas based on damage severity via proximity to the eye of storm.
3. estimating the overall and categorical financial losses incurred by owners of residential properties affected by the storm. 
4. if we're lucky, we may add another components to estimate loss to insurance companies!

### Team Members
- Venkata Datta Adithya Gadhamsetty
- Matthew Brownrigg
- Beatrix Wen
- Richard Zhang

### How to build
This project was built using conda environment manager so it is recommended you use a conda distribution.
With conda you can use the `orkan.yml` file with:

```
$ conda env create -f orkan.yml
```

This will install all the requisite libraries to run our files.

### Running the Predictive Model

TBA

### Running the Damage Model

Use the BASH script `run.sh` located in src to generate a hurricane damage model. 
To run `run.sh` you need the following:

```
$ bash run.sh <longitude> <latitude> <radius_64> <radius_max>
```

The diagram will be generated in `data/` as `hurricane@(<long>,<lat>&<radius>)`
The estimated damage will appear as printed text on the console.


