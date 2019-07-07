# Generated with CadQuery2 v0.1
# Colored with KiCAD step-up tools
# No offsets

import cadquery as cq
import os

dims = {
    "body" : {
        "x"     : 5,
        "y"     : 5,
        "z"     : 1.57,
    },
    "indicator" : {
        "x"     : 0.9,
        "y"     : 0.9,
        "z"     : 0.3
     },
    "hole" : {
        "r"     : (4/2, 3.35/2),
        "depth"    : 0.8
    },
    "pin_frame" : {
        "x"             : 5.4,
        "y"             : 4.2,
        "z"             : 1.54-0.8,
        "thickness" : 0,
    },
    "pins" : {
        "x"     : 0.9,
        "y"     : 0.9
    }
}

if dims["pin_frame"]["thickness"] == 0:
    dims["pin_frame"]["thickness"] = (dims["pin_frame"]["x"] - dims["body"]["x"])/2

# Make main body
body = cq.Workplane("XY")\
    .box(dims["body"]["x"], dims["body"]["y"], dims["body"]["z"],\
         centered = (True, True, False))

# Cut recess for pins
body = body\
    .faces(">Y").workplane()\
    .center(-dims["body"]["x"]/2, -dims["body"]["z"]/2)\
    .rect(\
          dims["pins"]["x"],\
          dims["pin_frame"]["thickness"], centered = False)\
    .center(dims["body"]["x"],0)\
    .rect(\
          -dims["pins"]["x"],\
          dims["pin_frame"]["thickness"], centered = False)\
    .cutThruAll()

# Cut out LED cavity
body = body\
    .faces(">Z").workplane().circle(dims["hole"]["r"][0])\
    .cutBlind(-dims["hole"]["depth"])\
    .faces(">Z[-2]")\
    .edges()\
    .chamfer(dims["hole"]["depth"]-0.01, (dims["hole"]["r"][0] - dims["hole"]["r"][1])/2)

# Cut out pin3 indicator
body = body\
    .faces(">Z").center(dims["body"]["x"]/2, -dims["body"]["y"]/2)\
    .lineTo(-dims["indicator"]["x"], 0).lineTo(0, dims["indicator"]["y"]).close()\
    .cutBlind(-dims["indicator"]["z"])
    

# Create block of all 4 pins
pin_frame = cq.Workplane("XY")\
    .box(dims["pin_frame"]["x"],dims["pin_frame"]["y"],dims["pin_frame"]["z"],\
         centered = (True, True, False))

# Hollow out block to create a "bent pin" frame
pin_frame = pin_frame\
    .faces(">Y").workplane().rect(\
          dims["pin_frame"]["x"] - dims["pin_frame"]["thickness"]*2,\
          dims["pin_frame"]["z"]- dims["pin_frame"]["thickness"]*2)\
    .center(0, -(dims ["pin_frame"]["z"]/2 - dims["pin_frame"]["thickness"]/2))\
    .rect(dims["pin_frame"]["x"] - dims["pins"]["x"]*2, dims["pin_frame"]["thickness"])\
    .cutThruAll()\
    
# Remove circle so they don't Z-fight with the LED cavity
pin_frame = pin_frame\
    .faces(">Z").workplane().circle(dims["hole"]["r"][0] * 1.01)\
    .cutThruAll()

# Cut excess matierial to make them "single" pins
pin_frame = pin_frame\
    .faces("<Z").workplane().rect(\
        dims["pin_frame"]["x"],
        dims["pin_frame"]["y"] - dims["pins"]["y"]*2)\
    .cutBlind(-(dims["pin_frame"]["z"] - dims["pin_frame"]["thickness"]))\
    .faces(">Z").workplane().center(\
        -dims["pin_frame"]["x"]/2,\
        -(dims["pin_frame"]["y"]/2) + dims["pins"]["y"])\
    .rect(\
          dims["pin_frame"]["thickness"]*1.05,\
          dims["pin_frame"]["y"] - dims["pins"]["y"]*2,\
          centered = False)\
    .center(\
        dims["pin_frame"]["x"],\
        0)\
    .rect(\
          -dims["pin_frame"]["thickness"]*1.05,\
          dims["pin_frame"]["y"] - dims["pins"]["y"]*2,\
          centered = False)\
    .cutThruAll()\
    .edges("|Y and >X or |Y and <X").fillet(0.1)

ws2812b = body.union(pin_frame)



# If this is being run from the commandline, export a step
if '__file__' in globals():
    with open("LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm.step", "w+") as f:
        cq.exporters.exportShape(ws2812b, cq.exporters.ExportTypes.STEP, f)
else:
    show_object(body, name = "body", options = {"color" : "F9F9F9"})
    show_object(pin_frame, name = "pin_frame", options = {"color" : "#a0a0a0"})