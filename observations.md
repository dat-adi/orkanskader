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

- I'm still concerned that the Miami housing dataset, Vital Signs, and even Zillow is too sparse for the data we need. I think we need to increase the scope and create some assumptions to really understand pricing. It's my bias that price should be in the millions for any hurricane. So I found this dataset that find median [home prices by county](https://www.nar.realtor/sites/default/files/documents/2024-q1-county-median-prices-and-monthly-mortgage-payment-by-state-07-09-2024.pdf) (unfortunately its in pdf only so we need to do some scraping) and I also found [housing unit estimates by county](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-housing-units.html)
    - All we need to do is multiply median price (dataset 1) * housing estimate (dataset 2) and that should be estimated value of county

- For Hurricane Projection onto counties I used the following data sets to convert rmax and latitude and longitude into modeled damage.
    - [Coastal Dataset Florida](https://fgdl.org/zips/metadata/htm/cntbnd_sep15.htm)
    - [Long-lat Dataset Florida](https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?flg=en-us&disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name&refine.state_name=Florida&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InVzLWNvdW50eS1ib3VuZGFyaWVzIiwib3B0aW9ucyI6eyJmbGciOiJlbi11cyIsImRpc2p1bmN0aXZlLnN0YXRlZnAiOnRydWUsImRpc2p1bmN0aXZlLmNvdW50eWZwIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lIjp0cnVlLCJkaXNqdW5jdGl2ZS5uYW1lbHNhZCI6dHJ1ZSwiZGlzanVuY3RpdmUuc3R1c2FiIjp0cnVlLCJkaXNqdW5jdGl2ZS5zdGF0ZV9uYW1lIjp0cnVlLCJyZWZpbmUuc3RhdGVfbmFtZSI6IkZsb3JpZGEifX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImFsYW5kIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJzdGF0ZWZwIiwibWF4cG9pbnRzIjo1MCwic29ydCI6IiJ9XSwidGltZXNjYWxlIjoiIiwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&location=6,27.74868,-83.8046&basemap=jawg.light)
