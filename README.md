## Supplemental Information for Data Section

### Data Tables: Original Values from 1990 Census and 2019-2023 ACS Sets and Added Columns

SOURCE: 

Ruggles, Steven et al. IPUMS National Historical Geographic Information System: Version 20.0 [dataset]. Minneapolis, MN: IPUMS. 2025.  http://doi.org/10.18128/D050.V20.0

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

### Explanation of Modifications to Data

See "DATASCI406_Project_Data_Code.ipynb" for the exact code; below are detailed explanations. 

#### Phase 1: 1990 Census Data Modifications

Step 1: Geographic Filtering

- **Columns Modified**: Filtered dataset to California records only

Step 2: Poverty Statistics Aggregation

- **Original Columns**: E07001-E07024 (24 columns)
  - E07001-E07012: Income above poverty level by 12 age groups
  - E07013-E07024: Income below poverty level by 12 age groups
- **New Columns Created**:
  - `total_above_poverty`: Sum of persons above poverty level
  - `total_below_poverty`: Sum of persons below poverty level
  - `total_poverty_determined`: Total persons assessed for poverty status
  - `poverty_rate`: Calculated as `total_below_poverty / total_poverty_determined`
- **Columns Removed**: Dropped all 24 original E07 columns

Step 3: Race/Ethnicity Column Renaming

- **Original Columns**: E4S001-E4S005
- **Modified Columns**:
  - `E4S001` → `race_white`
  - `E4S002` → `race_black`
  - `E4S003` → `race_american_indian_eskimo_aleut`
  - `E4S004` → `race_asian_pacific_islander`
  - `E4S005` → `race_other`

Step 4: Housing Occupancy Transformation

- **Original Columns**: EYP001, EYP002
- **Modified Columns**:
  - `EYP001` → `housing_occupied`
  - `EYP002` → `housing_vacant`
- **New Columns Created**:
  - `total_housing_units`: Sum of occupied and vacant units
  - `occupancy_rate`: Calculated as `housing_occupied / total_housing_units`

Step 5: Year Structure Built Column Renaming

- **Original Columns**: EX7001-EX7008
- **Renamed Columns**:
  - `EX7001` → `year_built_1989_to_1990`
  - `EX7002` → `year_built_1985_to_1988`
  - `EX7003` → `year_built_1980_to_1984`
  - `EX7004` → `year_built_1970_to_1979`
  - `EX7005` → `year_built_1960_to_1969`
  - `EX7006` → `year_built_1950_to_1959`
  - `EX7007` → `year_built_1940_to_1949`
  - `EX7008` → `year_built_1939_or_earlier`

Step 6: Housing Value Columns Processing

- **Original Columns**: EZH001-EZH020 (20 value range columns)
- **Created Columns**: Calculated `median_home_value_1990` using the 50th percentile position across all housing units
- **Cleanup**: Dropped all 20 individual value range columns

Step 7: Data Quality Checks

- **Null Check**: Verified no null values in processed columns
- **Negative Value Check**: Confirmed no negative values in numeric columns
- **Result**: Clean dataset ready for merging

---

#### Phase 2: 2019-2023 ACS Data Modifications

Step 1: Geographic Filtering

- **Action**: Filtered dataset to California records only

Step 2: GISJOIN Standardization

- **Action**: Truncated GISJOIN field to 12 characters with`str.slice(0, 12)` to pair with the 1990 dataset

Step 3: Column Renaming

- **Action**: ASVNE001 (Median home value) renamed to`2019-23_value`

Step 4: Data Quality Validation

- **Null Check**: Verified no null values present
- **Negative Value Check**: Identified and removed records with negative home values and removed all using `census_201923_selected['2019-23_value'] >= 0`

#### Phase 3: Merging and Final Dataset Creation

Step 1: Dataset Merge

- **Method**: Inner join on `GISJOIN`, resulting in only census tracts present in both 1990 and 2019-2023 datasets being retained

Step 2: Deriving 1990 to 2019-2023 Home Value Ratio

- **Columns Created**: `home_value_ratio_2019_23_to_1990` as`2019-23_value / median_home_value_1990`
