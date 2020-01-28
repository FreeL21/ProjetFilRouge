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

