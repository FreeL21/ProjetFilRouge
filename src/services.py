from flask import request
from flask_api import FlaskAPI, status
import pyongc

app = FlaskAPI(__name__)

port = 5432

CATALOG_LIST = None

SEARCH_WHITE_LIST = [
    "id",
    "name",
    "type",
    "ra",
    "dec",
    "const",
    "majax",
    "minax",
    "pa",
    "bmag",
    "vmag",
    "jmag",
    "hmag",
    "kmag",
    "sbrightn",
    "hubble",
    "cstarumag",
    "cstarvmag",
    "messier",
    "ngc",
    "ic",
    "cstarnames",
    "identifiers",
    "commonnames",
    "nednotes",
    "ongcnotes"
]


def response_template(obj):
    return {
        "Id": obj._id,
        "Name": obj._name,
        "Type": obj._type,
        "R.A.": obj._ra,
        "Dec.": obj._dec,
        "Constellation": obj._const,
        "Major axis": obj._majax,
        "Minor axis": obj._minax,
        "Position d'angle": obj._pa,
        "B-magnitude": obj._bmag,
        "V-magnitude": obj._vmag,
        "J-magnitude": obj._jmag,
        "H-magnitude": obj._hmag,
        "K-magnitude": obj._kmag,
        "Sun brightness": obj._sbrightn,
        "Hubble": obj._hubble,
        "C-Star U-magnitude": obj._cstarumag,
        "C-Star V-magnitude": obj._cstarvmag,
        "Messier": obj._messier,
        "New General Catalog": obj._ngc,
        "IC": obj._ic,
        "C-Star names": obj._cstarnames,
        "Identifiers": obj._identifiers,
        "Common Names": obj._commonnames,
        "Ned notes": obj._nednotes,
        "ONGC notes": obj._ongcnotes
    }

@app.before_first_request
def init_data():
    global CATALOG_LIST
    print("WAIT: Starting download data...")
    CATALOG_LIST = pyongc.listObjects()
    print("DONE: data downloaded." + str(len(CATALOG_LIST)) + "objects loaded")

@app.route("/", methods=['GET'])
def ongc_list():

    global CATALOG_LIST
    global SEARCH_WHITE_LIST
    result = []

    # get user request param
    filters = request.args if request.args else []

    # Filter fields verification
    for filter in filters:
        if filter not in SEARCH_WHITE_LIST:
            msg = "The parameter [" \
                  + filter \
                  + "] does not exist in filter parameters. The available filters are : " \
                  + ", ".join(map(str, SEARCH_WHITE_LIST))
            return msg, status.HTTP_400_BAD_REQUEST

    # Search by filters
    if len(filters):
        # In all objects
        for obj in CATALOG_LIST:
            found = False
            # For each filters
            for filter in filters.items():
                # filters are peers
                filter_name = filter[0]
                # Cast the value in the good type
                if filter[1].find('\"') != -1:  # string
                    filter_value = filter[1].strip('\"')
                elif filter[1].find('.') != -1:  # float
                    filter_value = float(filter[1])
                else:  # int
                    filter_value = int(filter[1])
                if getattr(obj, "_" + filter_name) == filter_value:
                    found = True
                    break
            # Add the object just once
            if found:
                result.append(obj)
    else:
        result = CATALOG_LIST

    # Object to Json
    serialized_result = [response_template(obj) for obj in result]
    return serialized_result


if __name__ == "__main__":
    app.run(debug=True)
