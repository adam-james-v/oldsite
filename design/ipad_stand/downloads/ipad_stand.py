# coding: utf-8

def rect_tube(b, h, t, L):
    # Define tube's edge radius according to thickness
    r = t*1.5
    
    # Set up the workplane for the tube's profile
    end_plane = cq.Workplane('XY').workplane(offset=-L/2.0)

    tube = (end_plane
                .rect(b, h, centered=True).extrude(L)
                .edges('|Z').fillet(r)
               )
    inner = (end_plane
                .rect(b-(t*2.0), h-(t*2.0), centered=True).extrude(L)
                .edges('|Z').fillet(r-t)
            )
    tube.cut(inner)
    return tube

# measurements in inches
base = (rect_tube(3.0, 1.5, 0.125, 15.0)
            .faces('<Y').workplane() # select bottom of tube
            .moveTo(0.0, 3.0).hole(0.85, 0.2) # create access holes to fit a socket wrench
            .moveTo(0.0, -3.0).hole(0.85, 0.2)
            .faces('>Y').workplane() # select top of tube
            .moveTo(0.0, 3.0).hole(0.316, 0.2) # top holes to allow 5/16in bolt through
            .moveTo(0.0, 3.375).rect(0.9, 0.075)
            .moveTo(0.0, 2.625).rect(0.9, 0.075)
            .moveTo(0.0, -3.375).rect(0.9, 0.075)
            .moveTo(0.0, -2.625).rect(0.9, 0.075).cutBlind(-0.2)
            .faces('>Y').workplane()
            .moveTo(0.0, -3.0).hole(0.316, 0.2)
       )

show_object(base)



vert = (rect_tube(1.0, 0.75, 0.065, 16.0)
            .faces('<X').workplane(centerOption='CenterOfBoundBox') # select side of tube
            .moveTo(0.0, 1.0).hole(0.3125)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(-0.5, 1.4)
            .lineTo(-0.4, 1.4)
            .lineTo(-0.25, 1.0)
            .lineTo(-0.4, 0.6)
            .lineTo(-0.5, 0.6).close().cutBlind(-0.1)
            .faces('<Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(0.5, 1.4)
            .lineTo(0.4, 1.4)
            .lineTo(0.25, 1.0)
            .lineTo(0.4, 0.6)
            .lineTo(0.5, 0.6).close().cutBlind(-0.1)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(-0.4, -7.0)
            .lineTo(-0.4, -8.1)
            .lineTo(0.0, -8.25)
            .lineTo(0.4, -8.1)
            .lineTo(0.4, -7.0).close().extrude(-0.065)
            .faces('<Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(-0.4, -7.0)
            .lineTo(-0.4, -8.1)
            .lineTo(0.0, -8.25)
            .lineTo(0.4, -8.1)
            .lineTo(0.4, -7.0).close().extrude(-0.065)
       )

show_object(vert)


support = (rect_tube(1.0, 0.75, 0.065, 2.0)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(0.0, -0.75)
            .rect(0.635, 0.152).cutBlind(-0.8)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(0.0, -0.634)
            .rect(0.375, 0.08).cutBlind(-0.2)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(0.0, 1.0)
            .lineTo(0.0, 0.85)
            .lineTo(-0.15, 0.8375)
            .lineTo(-0.05, 0.0)
            .threePointArc((0.141, -0.353), (0.5, -0.5))
            .lineTo(0.5, 1.0).close().cutBlind(-0.8)
            .faces('>Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(-0.4, -0.9)
            .lineTo(-0.4, -1.1)
            .lineTo(0.0, -1.25)
            .lineTo(0.4, -1.1)
            .lineTo(0.4, -0.9).close().extrude(-0.065)
            .faces('<Y').workplane(centerOption='CenterOfBoundBox')
            .moveTo(-0.4, -0.9)
            .lineTo(-0.4, -1.1)
            .lineTo(0.0, -1.25)
            .lineTo(0.4, -1.1)
            .lineTo(0.4, -0.9).close().extrude(-0.065)
       )

show_object(support)

import cqjupyter_extras as cqe
import cqtools

asm = [
    ['base', '0 0 0', '0 0 0' ],
    ['vert', '0 222.25 76.2', '270 0 0' ],
    ['vert', '0 222.25 -76.2', '270 0 0' ],
    ['support', '38.1 247.65 76.2', '0 90 270' ],
    ['support', '38.1 247.65 -76.2', '0 90 270' ],
]

cqe.cqassemble(asm, name='support')

base_part = cqtools._loadSTEP('base.STEP')
vert_part = cqtools._loadSTEP('vert.STEP')
support_part = cqtools._loadSTEP('support.STEP')

asm2 = [
    base_part.findSolid(),
    (vert_part
         .rotate((0,0,0), (1,0,0), 270)
         .translate((0, 76.2, 222.25))
         .findSolid()
    ),
    (vert_part
         .rotate((0,0,0), (1,0,0), 270)
         .translate((0, -76.2, 222.25))
         .findSolid()
    ),
    (support_part
         .rotate((0,0,0), (0,1,0), 90)
         .rotate((0,0,0), (1,0,0), 270)
         .translate((38.1, 247.65, 76.2))
         .findSolid()
    ),
    (support_part
         .rotate((0,0,0), (0,1,0), 90)
         .rotate((0,0,0), (1,0,0), 270)
         .translate((38.1, 247.65, -76.2))
         .findSolid()
    ),
]

# Some weird syntax to properly create the compound geometry
# There is likely a cleaner way to do this, but I'm unaware currently
final = cq.cq.Compound.makeCompound(asm2)
final = cq.CQ(final)
show_object(final)