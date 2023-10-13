# ZIP-Code Converters
### Python functions for using USA ZIP Codes in geospatial processes.
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

*By J. A. Cooper -- https://github.com/cooperjaXC*

## Overview
Crosswalks for easy python conversions of USA ZIP Codes.

1) ZIP Codes &rarr; ZCTAs
 * *Input* 
     * USA ZIP Codes *(string)* 
 * *Outputs:*
     * 5 digit [US Census Zip Code Tabulation Areas (ZCTAs)](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html#:~:text=ZIP%20Code%20Tabulation%20Areas%20or,Plan%20(ZIP)%20Codes%20dataset.) *(string)*
     * ZCTA's latitude & longitude centroid coordinates *(list)*
2) ZIP Codes &rarr; ZCTAs
 * *Input* 
     * ZCTAs *(string)*
 * *Outputs:*
     * Each corresponding 5 digit postal Zip Codes *(list)*

Operates with both individual ZIP Codes and pandas dataframes. 
Compatible with both US Census year 2010 and 2020 (default) ZCTAs. 

## Key Functions
* `zip_code_crosswalk` - Takes a (1) postal ZIP Code and transforms it into a Zip Code Tract Area (ZCTAs), 
    the US Census-defined polygonal region for a ZIP Code. Compatible with both 2010 and 2020 ZCTAs.
* `df_zip_crosswalk` - Takes a Pandas Dataframe with a ZIP-Code field and 
    returns a ZCTA field using the crosswalk function.
* `reverse_zcta_crosswalk` - Takes a (1) Zip Code Tract Area (ZCTAs) and returns all its associated postal ZIP Codes.
    Compatible with both 2010 and 2020 ZCTAs.
* `df_reverse_zcta_crosswalk` - Takes a Pandas Dataframe with a ZCTA field and 
    returns a field with a list of associated ZIP-Codes. Uses the reverse crosswalk function.
* `lat_lon_centroid` - Takes a (1) postal ZIP Code and returns its ZCTA's spatial coordinates in a [latitude, longitude]
    format based on US Census TIGER shapefiles. Compatible with both 2010 and 2020 ZCTAs.
* `df_latlon_centroids` - Takes a Pandas Dataframe with a ZIP-Code field and 
    returns fields with the ZCTA's central latitude and longitude coordinates using the centroid function.
