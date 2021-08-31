# ZIP Code Converters
### Python functions for using USA ZIP Codes in geospatial processes.
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

*By J. A. Cooper -- https://github.com/cooperjaXC*

## Overview
Crosswalks for easy python conversions of USA ZIP codes.

 * *Inputs* 
     * USA ZIP codes 
 * *Outputs:*
     * 5 digit US Census Zip Code Tabulation Areas (ZCTAs) *(string)*
     * ZCTA's latitude & longitude centroid coordinates *(list)*

Operates with both individual ZIP-code and pandas dataframes. 
Compatible with both US Census year 2010 and 2020 (default) ZCTAs. 

## Key Functions
* `zip_code_crosswalk` - Takes a (1) postal ZIP Code and transforms it into a Zip Code Tract Area (ZCTAs), 
    the US Census-defined polygonal region for a ZIP Code. Compatible with both 2010 and 2020 ZCTAs.
* `df_zip_crosswalk` - Takes a Pandas Dataframe with a ZIP-Code field and 
    returns a ZCTA field using the crosswalk function.
* `lat_lon_centroid` - Takes a (1) postal ZIP Code and returns its ZCTA's spatial coordinates in a [latitude, longitude]
    format based on US Census TIGER shapefiles. Compatible with both 2010 and 2020 ZCTAs.
* `df_latlon_centroids` - Takes a Pandas Dataframe with a ZIP-Code field and 
    returns fields with the ZCTA's central latitude and longitude coordinates using the centroid function.
