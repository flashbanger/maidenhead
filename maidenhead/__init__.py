from typing import Tuple
"""## mlocs - Maidenhead
toMaiden([lat, lon], level) returns a char (len = lvl*2)
toLoc(mloc) takes any string and returns topleft [lat,lon] within mloc

Beyond 8 characters is not defined for Maidenhead.
"""


def toLoc(maiden: str) -> Tuple[float, float]:
    """
    input: maidenhead locator of length 2 to 8
    output: [lat,lon]
    """
    if not isinstance(maiden, str):
        raise TypeError('Maidenhead locator must be a string')

    maiden = maiden.strip().upper()

    N = len(maiden)
    if not 8 >= N >= 2 and N % 2 == 0:
        raise ValueError('Maidenhead locator requires 2-8 characters, even number of characters')

    Oa = ord('A')
    lon = -180.
    lat = -90.
# %% first pair
    lon += (ord(maiden[0])-Oa)*20
    lat += (ord(maiden[1])-Oa)*10
# %% second pair
    if N >= 4:
        lon += int(maiden[2])*2
        lat += int(maiden[3])*1
# %%
    if N >= 6:
        lon += (ord(maiden[4])-Oa) * 5./60
        lat += (ord(maiden[5])-Oa) * 2.5/60
# %%
    if N >= 8:
        lon += int(maiden[6]) * 5./600
        lat += int(maiden[7]) * 2.5/600

    return lat, lon


def toMaiden(lat: float, lon: float,
             precision: int = 3) -> str:
    """Returns a maidenhead string for specified lat-lon tuple at specified level.
    """

    A = ord('A')
    a = divmod(lon+180, 20)
    b = divmod(lat+90, 10)
    astring = chr(A+int(a[0])) + chr(A+int(b[0]))
    lon = a[1] / 2.
    lat = b[1]
    i = 1
    while i < precision:
        i += 1
        a = divmod(lon, 1)
        b = divmod(lat, 1)
        if not (i % 2):
            astring += str(int(a[0])) + str(int(b[0]))
            lon = 24 * a[1]
            lat = 24 * b[1]
        else:
            astring += chr(A+int(a[0])) + chr(A+int(b[0]))
            lon = 10 * a[1]
            lat = 10 * b[1]

    if len(astring) >= 6:
        astring = astring[:4] + astring[4:6].lower() + astring[6:]

    return astring


def genGoogleMap(mloc: str) -> str:

    gpos = toLoc(mloc)

    return "http://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=10&size=320x240&sensor=false".format(gpos[0], gpos[1])


def genNonSense(lat: float, lon: float, level: int = 3) -> str:
    mloc = toMaiden(lat, lon, level)

    return "http://no.nonsense.ee/qthmap/?qth={}".format(mloc)
