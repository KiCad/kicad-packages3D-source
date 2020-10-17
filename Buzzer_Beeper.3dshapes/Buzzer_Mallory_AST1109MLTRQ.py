# This is a CadQuery script template
# Add your script code below
import cadquery as cq

# The show function will still work, but is outdated now
# Use the following to render your model with grey RGB and no transparency
# show(my_model, (204, 204, 204, 0.0))

# New method to render script results using the CadQuery Gateway Interface
# Use the following to render your model with grey RGB and no transparency
# show_object(result, options={"rgba":(204, 204, 204, 0.0)})

dims = {
    "body": {
        "width": 11,
        "depth": 9,
        "height": 2,
        "hole": {
            "radius": 0.5,
            "offset": (0, 0)
        }
    },
    "pad": {
        "width": 2,
        "depth": 2,
        "height": 0.3,
        "hole": {
            "radius": 0.5,
            "offset": (0, 0)
        }
    }
}

dims["body"]["hole"]["offset"] = (
    dims["body"]["width"]/4,
    dims["body"]["depth"]/4
)

dims["pad"]["hole"]["offset"] = \
    ((dims["body"]["width"] + dims["pad"]["width"])/2, 0)

hole_points = []

for i in [-1, 1]:
    for l in [-1, 1]:
        hole_points.append(
            (i*dims["body"]["hole"]["offset"][0],
             l*dims["body"]["hole"]["offset"][1])
        )

body = cq.Workplane("XY")\
    .box(
         dims["body"]["width"],
         dims["body"]["depth"],
         dims["body"]["height"],
         centered=(True, True, False))\
    .faces(">Z").workplane().pushPoints(hole_points)\
    .circle(dims["body"]["hole"]["radius"]).cutBlind(-0.25)

pads = cq.Workplane("XY")\
    .box(
        dims["pad"]["width"]*2 + dims["body"]["width"],
        dims["pad"]["depth"],
        dims["pad"]["height"],
        centered=(True, True, False))\
    .faces(">Z").workplane()\
    .pushPoints([
        (dims["pad"]["hole"]["offset"][0], 0),
        (-dims["pad"]["hole"]["offset"][0], 0)
    ]).hole(dims["pad"]["hole"]["radius"]*2)\
    .faces(">Z").workplane()\
    .rect(
        dims["body"]["width"],
        dims["pad"]["depth"]
    ).cutThruAll()

result = body.union(pads, combine=True, clean=False)

show_object(result)
#show_object(body, options={"rgba": (50, 50, 50, 0)})
#show_object(pads, options={"rgba": (150, 150, 150, 0)})
