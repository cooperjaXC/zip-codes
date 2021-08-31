"""
ZIP-Code Crosswalks.
Takes USA ZIP-Codes and returns 5 digit US Census Zip Code Tabulation Areas (ZCTAs)
and/or their latitude & longitude centroid coordinates.

By J. A. Cooper https://github.com/cooperjaXC
"""

import os, json, inspect, numpy as np, pandas as pd, openpyxl


def zip_code_formatter(postal_code):
    """Formats a USA ZIP-Code into the correct 5-digit format."""
    # Put in some safeguards here in case you get entries with zip 9s or zips w/o the leading 0s.
    postal_code = str(postal_code)
    if len(postal_code) > 5:
        postal_code = postal_code[:5]
    if "-" in postal_code:
        postal_code = postal_code.replace("-", "").replace(" ", "")
    # Use zfill()? https://stackoverflow.com/questions/733454/best-way-to-format-integer-as-string-with-leading-zeros
    if len(postal_code) == 3:
        # No longer only uses postal codes "501" and "544". Expanded to include US overseas territories.
        postal_code = "00" + postal_code
    if len(postal_code) == 4:
        postal_code = "0" + postal_code
    # Catch nulls and return None
    null_list = ["0", "nan", "null", "none", "0none", "00nan"]
    if (not postal_code) or (postal_code.lower() in null_list):
        postal_code = None
    return postal_code


class ZipCodes:
    """Contains variables relating to ZIP-Codes and ZCTAs.
    2010 Crosswalk data here comes from https://udsmapper.org/zip-code-to-zcta-crosswalk/ .
    This dictionary is based on the 2010 Census' ZCTA data and will need to be updated with the new 2020 geographies."""

    def __init__(self, year=2020):
        # Establish the Census year in question
        try:
            year = int(year)
        except:
            print(
                "Year value of",
                year,
                "is an invalid input for the Zip Code Class. Default of '2020' will be set.",
            )
            year = 2020
        if year not in [2010, 2020]:  # Census years
            if year < 2020:
                # years in the 2010s (before 2020) all operate on 2010 census definitions.
                year = 2010
            else:
                year = 2020
        self.year = str(year)

        # Find the path to the directory of JSONs containing ZIP-Code data.
        filepath = os.path.join(
            os.path.realpath(
                os.path.abspath(
                    os.path.split(inspect.getfile(inspect.currentframe()))[0]
                )
            ),
            "json",
        )
        # If the `json` directory is in a sibling directory to the script
        if os.path.exists(filepath) is False:
            filepath = os.path.join(
                os.path.dirname(os.path.dirname(filepath)), os.path.basename(filepath)
            )

        # Establish year-specific variables
        # # ZIP-Code -> ZCTA Crosswalks
        crosswalk_path = os.path.join(
            filepath, "zipzcta_crosswalk_" + self.year + ".json"
        )
        with open(crosswalk_path) as open_cross:
            # A dictionary containing the ZIP-Code (key; string)
            # and corresponding ZCTA (value; string) for the given [year].
            self.crosswalk = json.load(open_cross)
        latlon_path = os.path.join(
            filepath, "zcta_latloncentroid_" + self.year + ".json"
        )
        # # ZCTA -> Latitude & Longitude Centroids
        with open(latlon_path) as open_ll:
            # A dictionary containing the ZCTA (key; string)
            # and corresponding [Latitude, Longitude] coordinates (value; list) for the given [year].
            self.latlon_centroids = json.load(open_ll)


def zip_code_crosswalk(
    postal_code, year=2020, use_postalcode_if_error=False, suppress_prints=False
):
    """This function takes a (1) postal ZIP Code and transforms it into a Zip Code Tabulation Area,
    the US Census-defined polygonal region for a ZIP Code.
    Postal ZIP Codes are not indicative of a continuous region; rather, they are functional attributes used by the
    US Postal Service to deliver mail & goods. They can refer to a single post office (point), a discontinuous
    region, or an area that transcends state borders. The ZCTA is the Census' way of polygonizing and ordering this
    messy but commonly-used geographic identifying attribute.
    Crosswalk data here comes from https://udsmapper.org/zip-code-to-zcta-crosswalk/ .
    This function has been updated with the 2020 census' new ZCTA definitions."""
    zipcrosswalk = ZipCodes(year).crosswalk

    # Put in some safeguards here in case you get entries with zip 9s or zips w/o the leading 0s.
    postal_code = zip_code_formatter(postal_code)

    # Get ZCTA
    if postal_code in zipcrosswalk:
        zcta = zipcrosswalk[postal_code]
    else:
        nozctawarning = str(postal_code) + " is not in CCAoA's records."
        if use_postalcode_if_error is True:
            if suppress_prints is False:
                print(nozctawarning, "The input postal code will be returned instead.")
            zcta = postal_code
        else:
            if suppress_prints is False and str(postal_code).lower() != "none":
                print(
                    nozctawarning,
                    "No ZCTA will be returned. Please double check your entry and try again.",
                )
            zcta = None

    return zcta


def df_zip_crosswalk(
    dataframe,
    zip_field_name,
    year=2020,
    zcta_field_name="zcta",
    use_postalcode_if_error=False,
    suppress_prints=False,
):
    """Takes a Pandas Dataframe with a ZIP-Code field and returns a ZCTA field using the crosswalk function.
    Returns a Pandas dataframe."""
    if zip_field_name not in dataframe.columns.to_list():
        print(
            zip_field_name,
            "not in the submitted dataframe. No ZCTA field will be added.",
        )
        return dataframe
    else:
        outdf = dataframe.copy()
        outdf[zcta_field_name] = (
            outdf[zip_field_name]
            .fillna("0")
            .astype(int)
            .astype(str)
            .apply(
                lambda x: zip_code_crosswalk(
                    x,
                    year=year,
                    use_postalcode_if_error=use_postalcode_if_error,
                    suppress_prints=suppress_prints,
                )
            )
        )
        return outdf


def lat_lon_centroid(
    postal_code, year=2020, use_postalcode_if_error=False, suppress_prints=False
):
    """Returns the latitude and longitude coordinates in the centroid of the postal ZIP code's ZCTA
    as defined by the US Census Bureau's TIGER shapefiles. The function will return a list: [lat, lon].
    These centroids are not guaranteed to be on land.
    If there is a body of water near the geometric center of the ZCTA, the centroid may be placed offshore."""
    zcta = zip_code_formatter(
        zip_code_crosswalk(postal_code, year, use_postalcode_if_error, suppress_prints)
    )
    latlon_crosswalk = ZipCodes(year).latlon_centroids

    if zcta in latlon_crosswalk:
        centroid = latlon_crosswalk[zcta]
    else:
        if suppress_prints is False:
            zip_is_zcta = zcta == postal_code
            if zip_is_zcta:
                no_centroid_warning = (
                    str(postal_code) + " does not have a centroid in CCAoA's records"
                )
            else:
                no_centroid_warning = (
                    str(postal_code)
                    + "'s tabulation area "
                    + str(zcta)
                    + " does not have a centroid in CCAoA's records"
                )
            no_centroid_warning = (
                no_centroid_warning
                + " for the census year "
                + str(year)
                + ".\n No centroid will be returned. Please double check your entry and try again."
            )
            print(no_centroid_warning)
        # There is hot debate in coding communities on whether to reutrn None or an empty list for situations like this.
        # https://softwareengineering.stackexchange.com/questions/120355/is-it-better-to-return-null-or-empty-values-from-functions-methods-where-the-ret
        # https://www.reddit.com/r/Python/comments/30yb5t/return_none_or_not_to_return_none/
        # I have chosen to return the None as coordinates within a list
        # # so as to not destroy downstream list parsing efforts.
        centroid = [None, None]
    return centroid


def df_latlon_centroids(
    dataframe,
    zip_in_field_name,
    year=2020,
    keep_coordinates_field=False,
    use_postalcode_if_error=False,
    suppress_prints=False,
):
    """
    Takes a Pandas Dataframe with a ZIP-Code field and returns a [latitude, longitude] coordinates field
    using the `lat_lon_centroid` function. Returns a Pandas dataframe.
    """
    if zip_in_field_name not in dataframe.columns.to_list():
        print(
            zip_in_field_name,
            "not in the submitted dataframe. No ZCTA centroid fields will be added.",
        )
        return dataframe
    else:
        outdf = dataframe.copy()
        coordfieldname = "coordinates"
        # Generate the coordinates field with a [lat, lon] list
        outdf[coordfieldname] = outdf[zip_in_field_name].apply(
            lambda x: lat_lon_centroid(
                x,
                year=year,
                use_postalcode_if_error=use_postalcode_if_error,
                suppress_prints=suppress_prints,
            )
        )
        # Split the coordinates field into a lat and lon field separately.
        outdf["lat"] = outdf[coordfieldname].apply(lambda x: x[0])
        outdf["lon"] = outdf[coordfieldname].apply(lambda x: x[1])
        # Remove the coordinates field unless the input argument says otherwise
        if keep_coordinates_field is False:
            outdf = outdf.drop(coordfieldname, axis=1)
        return outdf
