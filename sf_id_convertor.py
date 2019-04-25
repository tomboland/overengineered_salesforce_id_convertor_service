from __future__ import annotations
from sanic import Sanic
from sanic.response import json
from typing import NewType, Optional
from funcy import partition


app = Sanic()

SfId15 = NewType("SfId15", str)
SfId18 = NewType("SfId18", str)


def sf18_from_15(sf_id: SfId15) -> Optional[SfId18]:
    """Convert a 15 character Salesforce ID to the 18 character one.
    This encodes the character case of the ID in to 3 additional characters
    1) Split the input in to chunks of 5, and reverse the chunks
    2) Turn each chunk in to a binary representation, uppercase == 1
    3) Look up the result converted to int in an alphunumeric table
    4) Append the three characters and return the result
    """
    if not all([
        len(sf_id) == 15,
        sf_id.isalnum()
    ]):
        return None
    parts = [part[::-1] for part in partition(5, sf_id)]
    ups_downs = ((c.isupper() for c in part) for part in parts)
    bins = ("".join("1" if c else "0" for c in part) for part in ups_downs)
    int_chrs = (int(bs, 2) for bs in bins)
    lookup_chars = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"[x] for x in int_chrs]
    return SfId18(sf_id + "".join(lookup_chars))


@app.route("/sf_id/<sf_id>")
async def sf_id(request, sf_id):
    result = sf18_from_15(SfId15(sf_id))
    return json({"sf_id": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
