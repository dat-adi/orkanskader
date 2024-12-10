- Interestingly enough, there seem to be fluctuations caused in the housing market whenever a hurricane hits Florida.
- The HPI is an indicator of housing price changes. This is referenced and used in "Investigation of Florida Housing Prices using Predictive Time Series Model" by Aderibigbe et al.
- [Vital Signs](https://data.bayareametro.gov/dataset/Vital-Signs-Home-Prices-by-zip-code/8xer-7dm5/about_data) has 5082 rows in its dataset and has the change over time for specific zipcodes. Zillow (2019). Vital Signs: Home Prices – by zip code [Dataset]. https://data.bayareametro.gov/dataset/Vital-Signs-Home-Prices-by-zip-code/8xer-7dm5

- A HPI increase dataset for florida specifically may give us good info on average house hold prices raising over the entire state: (2024). All-Transactions House Price Index for Florida [Dataset]. https://fred.stlouisfed.org/series/FLSTHPI

- The Zillow Public Housing Dataset has a home value index which has a range of the prices that homes were estimated at in a time-series fashion. This dataset is in the data/ folder with the name Metro....csv

- [ ] Considering that we don't have a direct relation between zipcode and housing prices. We can work with the Zillow dataset that contains sectors within a state. For example, Florida seems to have a bunch of cities within it. Finding out which cities falling into the range of the storm when the storm is located should help in retrieving an average estimate when we link it up to the Zillow dataset.

- [ ] I have to check out insurance claims and what proceedings I can retrieve from this. Formulas from Fannie Mae and Freddie Mac should help in doing just that.

- The [miami housing dataset](https://www.kaggle.com/datasets/deepcontractor/miami-housing-dataset) from Kaggle contains the data of 13932 single-family homes sold in Miami.

- Assuming that the miami housing dataset has information of the housing on average. We can use the weekly/monthly data reports from Zillow to showcase the difference in house evalution pricing post major hurricane storms. We can also compare inflation statistics on the side while we're at it.

- Another idea that I can run by to showcase that our project is fruitful is to showcase the impact of a hurricane ONLY in Miami. This can make our data and project itself appear more fruitful since we do have data for the city of Miami.

- Looks like there's more information about a property in the miami housing dataset. Based on the properties provided in the dataset, we can make "educated" guesses about the structural integrity of the house when faced with a storm. We can essentially create another model that utilizes this information to determine whether or not the house may be damaged. If damaged, how damaged would it be? We need training data for this. Need to search for "Structural degration of houses against a storm dataset" and correlate it with the current miami housing dataset to showcase any huge updates. update: this won't work because there's not enough parameters to train the house structure integrity vs wind speed and air pressure on.

- The scope of the project has been changed to city-wide now. The calculations that now need to be performed are which houses fall in the path of storm, whether their structural integrity would increase the chances of house deterioration, and how much the damage would be worth.
