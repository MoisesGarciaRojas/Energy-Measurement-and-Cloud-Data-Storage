# Energy Measurement and Cloud Storage With a FiPy Board
#### *Moises Daniel Garcia Rojas*
#### *October 29, 2019*

## Project Overview

The FiPy board is interfaced with a PZEM-004T-100A(V3.0) sensor. The interaction of the two monitors energy variables, which then are uploaded to the Pybytes platform to store and visualize the data.


### Data Overview
Variable description:

* price : price of home in USD
* bedrooms: number of bedrooms in home
* bathrooms: number of bathrooms in home
* sqft living: living aerea (in sq.ft)
* sqft lot: lot size of the house (in sq.ft)
* floors: number of floors
* waterfront: Waterfront dummy variable (= 1 if home is at Waterfront; 0 other-wise)
* view: Scenic view dummy variable (= 1 if home has a scenic view; 0 otherwise)
* condition: condition of home
* grade: Classification by construction quality which refers to the types of materials used and the quality of workmanship, higher grade = higher quality
* sqft basement: size of the basement
* sqft above: sqft above = sqft living - sqft basement
* yr built: year in which house was built
* yr renovated: year in which house was renovated for the last time, `0' indicating that no major renovation took place
* zipcode: ZIP code
* lat: geographic latitude of location
* long: geographic longitude of location
* sqft living15: the average house square footage of the 15 closest houses
* sqft lot15: the average lot square footage of the 15 closest houses

### Summary statistics for house prices

Bellow, the statistics tell us that the dataset has a house with a minimum price of 75,000 USD, and a house with a maximum value of 7,700,000 USD, with a median value in prices equal to 450,000 USD, and mean value of 540,088 USD with a standard deviation of ± 367,127.2 USD.
<pre class="r">
<code class="hljs">summary(houseData$price)</code>
</pre>
<pre><code class="hljs">##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##   75000  321950  450000  540088  645000 7700000</code></pre>
<pre class="r"><code class="hljs">sd(houseData$price)</code></pre>
<pre><code class="hljs">## [1] 367127.2</code></pre>
