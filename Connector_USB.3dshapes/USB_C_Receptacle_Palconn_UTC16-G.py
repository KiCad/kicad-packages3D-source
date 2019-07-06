# Generated with CadQuery2
# Boolean and align with kicad stepup tools with offsets:
#   Y: -1.17
#   X: 1.65

import cadquery as cq

dims_body = {
    "width" : 8.94,
    "depth" : 7.32,
    "height" : 3.25,
    "radius" : 1.25,
    "wall_thickness" : 0.345,
    "cavity_depth" : 4.8
}

dims_tounge = {
    "width" : 6.69,
    "height" : 0.7,
    "depth" : 4.45,
    "tip_chamfer" : 0.5
 }

dims_pegs = {
    "diameter" : 0.5,
    "length" : 0.76,
    "tip_chamfer" : 0.1,
    "centers" : [
        (5.78/2, -2.63),
        (-5.78/2, -2.63)
    ]
}

dims_pins = {
    "width" : 0.2,
    "length" : 7.63 - 7.32,
    "height" : 0.15,
    "centers" : [
        (-6.7/2, 0),
        (-6.1/2, 0),
        (-5.1/2, 0),
        (-4.5/2, 0)
    ]
}

dims_shield = {
    "thickness" : 0.3,
    "length" : 1,
    "width" : (0.8, 1.1), # (front, back)
    "centers_front" : [
        (-8.64/2, 1.06),
        (8.64/2, 1.06)
    ],
    "centers_back" : [
        (8.64/2, -3.11),
        (-8.64/2, -3.11)
    ]
}

x = -3.5/2
while x < 0:
    dims_pins["centers"].append((x, 0))
    x = dims_pins["centers"][-1][0] + 0.5

for i in range(8):
    dims_pins["centers"].append((dims_pins["centers"][i][0] * -1, 0))


body = cq.Workplane("XZ").box(dims_body["width"], dims_body["height"], dims_body["depth"])\
    .edges("|Y").fillet(dims_body["radius"]).faces("<Y").shell(-dims_body["wall_thickness"])

body_back = body.faces("<Y[-2]").workplane()\
    .box(\
         dims_body["width"]\
         , dims_body["height"]\
         , dims_body["depth"] - dims_body["cavity_depth"] - dims_body["wall_thickness"]\
         , centered = (True, True, False)\
         , combine = False)\
    .edges("|Y").fillet(dims_body["radius"])

shield_pins_front = cq.Workplane("XY").workplane(invert=True).pushPoints(dims_shield["centers_front"])\
    .box(dims_shield["thickness"],dims_shield["width"][0],dims_shield["length"] + dims_body["height"]/2\
         , centered = (True, True, False)\
         , combine = True)\
    .edges("|X and <Z").fillet(dims_shield["width"][0]/2 - 0.01)
    

shield_pins_back = cq.Workplane("XY").workplane(invert=True).pushPoints(dims_shield["centers_back"])\
    .box(dims_shield["thickness"],dims_shield["width"][1],dims_shield["length"] + dims_body["height"]/2\
         , centered = (True, True, False)\
         , combine = True)\
    .edges("|X and <Z").fillet(dims_shield["width"][1]/2 - 0.01)

body = body.union(body_back).union(shield_pins_back).union(shield_pins_front)
#del shield_pins_front
#del shield_pins_back
del body_back

tounge = body.faces(">Y[-3]")\
    .box(dims_tounge["width"],dims_tounge["height"],dims_tounge["depth"]\
         , centered = (True, True, False)\
         , combine = False)\
    .edges("|Z and <Y").chamfer(dims_tounge["tip_chamfer"])

pegs =body.faces("<Z[-3]").workplane().pushPoints(dims_pegs["centers"])\
    .circle(dims_pegs["diameter"]/2).extrude(dims_pegs["length"],combine = False)\
    .edges("<Z").chamfer(dims_pegs["tip_chamfer"])

pins = body.faces(">Y").workplane().center(0, -dims_body["height"]/2)\
    .pushPoints(dims_pins["centers"])\
    .box(dims_pins["width"],dims_pins["height"],dims_pins["length"]\
         , centered = (True, False, False)\
         , combine = False)\


show_object(body, name="body", options = {"color" : "#c8c8c8"})
show_object(tounge, name="tounge", options = {"color" : "#676767"})
show_object(pegs, name="pegs", options = {"color" : "#676767"})
show_object(pins, name="pins", options = {"color" : "#d9bd2d"})