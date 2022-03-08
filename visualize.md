# PIC16B Project: Dry Wells

#### *Predicting water shortages in California's Central Valley using periodic water level data*


California's Central Valley produces 1/4 of the nation's food and its supplies 1/5 of national groundwater demand.[^1] However, the region is prone to drought and water shortages. Furthermore, predicting these water shortages is difficult. Climate change has thrown off the statistical models resulting in huge errors in official water supply predictions, including a 68% error in the predictions for the Sacramento Valley region this year.[^2] Perhaps in response to the poor performance of these complex hydrological models, the California Department of Water Resources recently released its [Drought and Water Shortage Risk Explorer](https://tableau.cnra.ca.gov/t/DWR_IntegratedDataAnalysisBranch/views/SmallWaterSystemRisk-March2021/Dashboard?%3Aembed=y&%3AisGuestRedirectFromVizportal=y), containing an interactive map of the shortage risks of wells in the state. However, this risk assessment does not incorporate past data into a statistical model.

This project uses the [Household Water Supply Shortage Reporting System](https://data.ca.gov/dataset/household-water-supply-shortage-reporting-system-data), which logs 3765 reports of water shortages in California from 2014 onwards. We combine this with a dataset of all wells in the state. The predictors used are the [periodic groundwater level measurements](https://data.ca.gov/dataset/periodic-groundwater-level-measurements) from the Department of Water Resources.

[^1]: https://ca.water.usgs.gov/projects/central-valley/about-central-valley.html
[^2]: https://calmatters.org/newsletters/whatmatters/2022/02/california-water-inaccurate-forecasts/


```python
from plotly import express as px
import pandas as pd
import numpy as np
```

Let's have a look at the (cleaned) data. Here are the wells in our database - 289419 wells in total.


```python
wells = pd.read_csv('../cleaned/wells.csv')
```


```python
print(wells.shape)
print(wells.columns)
```

    (289419, 3)
    Index(['latitude', 'longitude', 'gis_gama_study_area'], dtype='object')



```python
fig = px.scatter_mapbox(wells.dropna(subset=['gis_gama_study_area']).sample(frac=0.2),
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='gis_gama_study_area',
                        opacity = 0.5,
                        zoom=5)
# fig.show()
```
{% include gamaareas.html %}

```python
stations = pd.read_csv('../cleaned/st.csv')
```


```python
print(stations.shape)
print(stations.columns)
```

    (45269, 3)
    Index(['site_code', 'latitude', 'longitude'], dtype='object')


Here are the stations which can be linked to periodic groundwater level measurements.


```python
fig = px.scatter_mapbox(stations,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        opacity = 0.5,
                        zoom=4)
# fig.show()
```
{% include stations.html %}

```python
shortages = pd.read_csv('../cleaned/sh.csv')
```


```python
print(shortages.shape)
print(shortages.columns)
```

    (3765, 4)
    Index(['latitude', 'longitude', 'date', 'y'], dtype='object')



```python
wells['type'] = 'well'
stations['type'] = 'station'
shortages['type'] = 'shortage'
stacked = pd.concat([wells,stations,shortages], join='inner')

```

Here is the geographical distribution of the wells, shortages, and stations. The map shows a 20% random sample.


```python
fig = px.scatter_mapbox(stacked.sample(frac=0.2),
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        opacity = 0.3,
                        color='type',
                        color_discrete_sequence=["green", "blue", "red"],
                        zoom=5)
fig.write_html("../output/stacked.html")
```
{% include stacked.html %}

The boundaries of our study are defined according to GAMA study areas that fall within the Central Valley. They were picked for its economic significance and density of measurement stations.

For the first step of the analysis, we look to explore the spatial correlation between measurements and shortages. The following steps are taken to process the data.
- Merge the stations dataset (which only has geographical coordinates) with the measurements via an identifier code.
- Take the difference of the groundwater elevation between measurements.
- Spatially aggregate the measurements by rounding off geographical coordinates to form a grid.
- Take the mean across time.


```python
d = pd.read_csv('../cleaned/m_agg.csv')
```


```python
d.columns
```




    Index(['latitude', 'longitude', 'd_gwe', 'wse_ch_av', 'wells', 'shortages',
           'sh_frac'],
          dtype='object')




```python
d.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>latitude</th>
      <th>longitude</th>
      <th>d_gwe</th>
      <th>wse_ch_av</th>
      <th>wells</th>
      <th>shortages</th>
      <th>sh_frac</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35.00</td>
      <td>-118.95</td>
      <td>0.484028</td>
      <td>-1.094127</td>
      <td>23</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>35.00</td>
      <td>-118.90</td>
      <td>-0.736640</td>
      <td>-5.352953</td>
      <td>27</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>35.00</td>
      <td>-118.85</td>
      <td>-0.607778</td>
      <td>-5.317659</td>
      <td>17</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>35.05</td>
      <td>-119.25</td>
      <td>0.019417</td>
      <td>0.514444</td>
      <td>15</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>35.05</td>
      <td>-119.15</td>
      <td>0.236467</td>
      <td>0.026113</td>
      <td>27</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



Here's a look at the frequency of shortages relative to the number of wells. This is the outcome that we aim to predict.


```python
fig = px.scatter_mapbox(d,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='sh_frac',
                        opacity=0.8,
                        zoom=5,
                        labels={"sh_frac": "Frequency of shortages"}
                       )

# fig.show()
```

{% include sh_frac.html %}

For the model, we use PySAL, a package for spatial analysis.

Having done the data processing and aggregation, each unit of observation in our dataset is roughly a 3 mile by 3 mile square, with the predictors being the average change in groundwater level in that square since 2013, and the dependent variable being the relative frequency of shortages.

As a benchmark, here are the predictions given by a linear regression model without accounting for spatial correlations.


```python
m_preds = pd.read_csv('../cleaned/m_preds.csv')
```


```python
fig = px.scatter_mapbox(m_preds,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='m1preds',
                        zoom=5,
                        title='Baseline linear regression model')
# fig.show()
```
{% include m1.html %}

Qualitatively, this model doesn't seem to produce very good predictions. To improve the model accuracy, we include *spatial lags*. In other words, we include as predictors a weighted average of the neighbors of each square. As our data is (roughly) carved into a grid, it makes the most sense to include the lags from the 4 nearest neighbors and 8 nearest neighbors.


```python
fig = px.scatter_mapbox(m_preds,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='m2preds',
                        zoom=5,
                        labels={"m2preds": "predicted values"},
                        title='Model including lags from 4 nearest neighbors')
# fig.show()
```
{% include m2.html %}


```python
fig = px.scatter_mapbox(m_preds,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='m3preds',
                        zoom=5,
                        labels={"m3preds": "predicted values"},
                        title='Model including lags from 8 nearest neighbors'
                       )
# fig.show()
```
{% include m3.html %}

The models with 4 and 8 nearest neighbors produce predictions that look close to the shortage map, and have lower mean squared errors. The coefficients for the spatial lags are also negative and statistically significant.

For the model to be useful for making predictions ahead of time, we need to exploit the time dimension of our data. Now, instead of averaging out the measurements across time, we aggregate the measurements (which are sporadically taken at roughly one-month intervals) into monthly data, interpolate missing months with the earlier value, and take the first difference. We also include the first and second lag (measurements from two prior months) to augment our predictors. After running the model, we obtain predicted values for every month-coordinate combination in the dataset. The average across time of the predicted values are mapped below, but the set of predictions contain a lot more information. Looking at the regression summary, both the water level measurement and its first lag are statistically significant. In fact, the first lag of the water level measurement is statistically significant regardless of whether the measurement for the month itself is included, suggesting that the water level changes may predict shortages before they occur.


```python
mt_preds = pd.read_csv('../cleaned/mt_preds.csv')
```


```python
fig = px.scatter_mapbox(mt_preds,
                        mapbox_style="carto-positron",
                        lat='latitude',
                        lon='longitude',
                        color='preds',
                        zoom=5)
# fig.show()
```
{% include 'output/m4.html' %}

In conclusion, this exercise has demonstrated that periodic groundwater level measurements contain useful signals for well shortages. In particular, this prediction task calls for incorporating both spatial and temporal lags. To extend the work of this project, future efforts could improve the method of geographical aggregation, take into account climate (especially seasonality), and include more detailed information on local hydrology such as the proximity to water features. As a concrete recommendation, the relevant authorities would do well to improve data availability and linkage, and to judiciously incorporate hydrological data into their existing risk-prediction systems.
