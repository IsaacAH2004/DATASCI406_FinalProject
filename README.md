#### Geographic Identifiers

- **GISJOIN**: GIS Join Match Code - unique identifier for linking geographic data across datasets and GIS applications
- **YEAR**: Data file year (1990 for historical census data)
- **STATE**: State name (California for this dataset)
- **TRACTA**: Census Tract Code - identifies the specific census tract within the county

- #### Race/Ethnicity Demographics (1990 Census)

Source: Table NP8 (E4S series) from 1990 Census STF 3

- **race_white**: Number of persons identifying as White
- **race_black**: Number of persons identifying as Black
- **race_american_indian_eskimo_aleut**: Number of persons identifying as American Indian, Eskimo, or Aleut
- **race_asian_pacific_islander**: Number of persons identifying as Asian or Pacific Islander
- **race_other**: Number of persons identifying as Other race

- #### Poverty Statistics (1990 Census)

Source: Table NP117 (E07 series) from 1990 Census STF 3 - Aggregated from 24 age-specific columns

- **total_above_poverty**: Total number of persons with income above poverty level in 1989
- **total_below_poverty**: Total number of persons with income below poverty level in 1989
- **total_poverty_determined**: Total persons for whom poverty status was determined
- **poverty_rate**: Calculated as (total_below_poverty / total_poverty_determined) - represents the percentage of people living below the poverty line

*Universe: Persons for whom poverty status is determined*

*Note: Original data included poverty status by 12 age groups for both above and below poverty levels, which have been aggregated into summary statistics*


#### Year Structure Built (1990 Census)

Source: Table NH25 (EX7 series) from 1990 Census STF 3

- **year_built_1989_to_1990**: Number of housing units built between 1989 and March 1990
- **year_built_1985_to_1988**: Number of housing units built between 1985 and 1988
- **year_built_1980_to_1984**: Number of housing units built between 1980 and 1984
- **year_built_1970_to_1979**: Number of housing units built between 1970 and 1979
- **year_built_1960_to_1969**: Number of housing units built between 1960 and 1969
- **year_built_1950_to_1959**: Number of housing units built between 1950 and 1959
- **year_built_1940_to_1949**: Number of housing units built between 1940 and 1949
- **year_built_1939_or_earlier**: Number of housing units built in 1939 or earlier

*Universe: All housing units in the census tract*

*These columns show the age distribution of the housing stock in each census tract as of 1990*


#### Contemporary Housing Value (2019-2023 American Community Survey)

Source: Table B25077 (ASVN series) from 2023 ACS 5-Year Data

- **2019-23_value**: Median value in dollars for owner-occupied housing units, averaged over the 2019-2023 period

*Universe: Owner-occupied housing units*

*This represents the most recent available census data for median home values, providing a comparison point to the 1990 data*
