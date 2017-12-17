# make a simple sample piece 
# to try out the dxf import function
sample_tube = (cq.Workplane('XY')
               .workplane(offset=-1)
               .dxf('downloads/profile.dxf')
               .extrude(2)
              )

show_object(sample_tube)

L = 31.6772 # comes from width of scrn + offset due to tube dims
tap_01875 = 0.1495

outer_h_top = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # holes on top face near edge
               # will be tapped with 3/16 bolt thread
               # used to mount inner frame tube
               .faces('>Y').workplane()
               .pushPoints([(-0.5,  13.3386),
                            (-0.5, -13.3386),
                            (-0.5,  6.6693),
                            (-0.5, -6.6693),
                            (-0.5, 0.0),])
               .hole(tap_01875, depth=0.08)
               # holes centered on back face
               # 2 pairs of 3/16 tapped holes
               # will mount back 'lock bar' tubes
               .faces('<X').workplane()
               .pushPoints([(0.0, 6.8386),
                            (0.0, 7.8386),
                            (0.0, -6.8386),
                            (0.0, -7.8386)])
               .hole(tap_01875, depth=0.08)
               # Cut the tube ends to create a 'dovetail'
               # joint to hold the vertical tubes in place
               # back left
               .faces('>Y').workplane()
               .moveTo(0.425, 15.3386)
               .polyline([(0.425, 15.4086),
                         (0.5, 15.839),
                         (0.75, 15.839),
                         (0.75, 15.3386)]).close()
               .cutThruAll()
               # front left
               .faces('>Y').workplane(centerOption='CenterOfBoundBox')
               .moveTo(-0.425, 15.3386)
               .polyline([(-0.425, 15.4086),
                         (-0.5, 15.839),
                         (-0.75, 15.839),
                         (-0.75, 15.3386)]).close()
               .cutThruAll()
               # back right
               .faces('>Y').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.425, -15.3386)
               .polyline([(0.425, -15.4086),
                         (0.5, -15.839),
                         (0.75, -15.839),
                         (0.75, -15.3386)]).close()
               .cutThruAll()
               # front right
               .faces('>Y').workplane(centerOption='CenterOfBoundBox')
               .moveTo(-0.425, -15.3386)
               .polyline([(-0.425, -15.4086),
                         (-0.5, -15.839),
                         (-0.75, -15.839),
                         (-0.75, -15.3386)]).close()
               .cutThruAll()
              )

show_object(outer_h_top)


# Outer Horizontal Bottom

tap_025 = 0.201

outer_h_bottom = (outer_h_top
                  .faces('<Y').workplane(centerOption='CenterOfBoundBox')
                  .pushPoints([(0.0,  7.3386),
                               (0.0, -7.3386)])
                  .hole(tap_01875, depth=0.08)
                 )

show_object(outer_h_bottom)


# Outer Verticals

L = 19.6693 # comes from height of scrn + offset due to tube dims
tap_01875 = 0.1495

outer_v = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # holes on top face near edge
               # will be tapped with 3/16 bolt thread
               # used to mount inner frame tube
               .faces('<Y').workplane()
               .pushPoints([(-0.5,  8.8507),
                            (-0.5, -8.8507),
                            (-0.5,  4.4173),
                            (-0.5, -4.4173),
                            (-0.5, 0.0),])
               .hole(tap_01875, depth=0.08)
               # Cut the tube ends to create the
               # 'dovetail' slot
               # left
               .faces('>Z').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.0, -0.135).rect(0.85, 0.25, centered=True)
               .cutBlind(-0.5, clean=True)
               .faces('>Z').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.0, 0.135).rect(1.0, 0.25, centered=True)
               .cutBlind(-0.5, clean=True)
               # right
               .faces('<Z').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.0, 0.135).rect(0.85, 0.25, centered=True)
               .cutBlind(-0.5, clean=True)
               .faces('<Z').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.0, -0.135).rect(1.0, 0.25, centered=True)
               .cutBlind(-0.5, clean=True)
              )

show_object(outer_v)


# Inner Frame Horizontals and Verticals

L = 27.6772 # horizontals
# L = 18.6693 # verticals
tap_01875 = 0.1495

pnts = [(0.0, 0.0),
        (0.0,  (L/2.0 - 0.5) ),
        (0.0, -(L/2.0 - 0.5) ),
        (0.0,  (L/2.0 - 0.5)/2.0 ),
        (0.0, -(L/2.0 - 0.5)/2.0 )]

inner = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # holes on the side which are
               # used to mount the inner frame
               # to the outer frame
               .faces('>X').workplane()
               .pushPoints(pnts)
               .hole(tap_01875, depth=0.08)
               # Access holes cut on wide face
               # which will be facing inwards
               # when the whole frame is assembled
               .faces('>Y').workplane()
               .pushPoints(pnts)
               .rect(1.05, 0.5)
               .cutBlind(-0.08)
              )

show_object(inner)


# Inner Horizontals
show_object(inner_h)


# Inner Verticals
show_object(inner_v)


# Stands

L = 10.0

stand = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # hole on top for .25in bolt to pass through
               .faces('>Y').workplane()
               .hole(0.257, depth=0.08)
               # Access hole on bottom
               .faces('<Y').workplane()
               .hole(0.9375, depth=0.08)
              )

show_object(stand)


# Lock Bars

L = 19.6693 # comes from height of scrn + offset due to tube dims
tap_025 = 0.201

pnts = [(0.0, 0.0 ),
        (0.0,  (L/2.0 - 3.0) ),
        (0.0, -(L/2.0 - 3.0) )]

end_holes = [( 0.5,  (L/2.0 - 0.25) ),
             (-0.5,  (L/2.0 - 0.25) ),
             ( 0.5, -(L/2.0 - 0.25) ),
             (-0.5, -(L/2.0 - 0.25) )]

lock_bar = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # hole on bottom for .25in bolt
               # to be threaded through for locking
               .faces('<Y').workplane()
               .pushPoints(pnts)
               .hole(tap_025, depth=0.08)
               # Access hole on top
               .faces('>Y').workplane()
               .pushPoints(pnts)
               .hole(0.9375, depth=0.08)
               # holes on ends for 3/16in 
               # screws to pass through
               .faces('<Y').workplane()
               .pushPoints(end_holes)
               .hole(0.1875, depth=0.08)
               # cut 45deg. triangles from
               # tube ends for screw access
               .faces('>X').workplane(centerOption='CenterOfBoundBox')
               .moveTo(-0.25, (L/2.0) )
               .polyline([( 0.25, (L/2.0) ),
                          ( 0.25, (L/2.0) - 0.5 )]).close()
               .cutThruAll()
               .faces('>X').workplane(centerOption='CenterOfBoundBox')
               .moveTo(-0.25, -(L/2.0) )
               .polyline([( 0.25, -(L/2.0) ),
                          ( 0.25, -(L/2.0) + 0.5 )]).close()
               .cutThruAll()
              )

show_object(lock_bar)


# Design Assembly

import cqjupyter_extras as cqe
import cqtools

# PARTS LIST
# inner_h
# inner_v
# outer_h_bottom
# outer_h_top
# outer_v
# stand
# lock_bar

# all positions are in mm.
# There is definite need to improve the
# assembly workflow here.
asm = [ 
    ['stand', '0 0  186.4', '0 90 0' ],
    ['stand', '0 0 -186.4', '0 90 0' ],
    ['outer_h_bottom', '0 12.7 0', '0 0 0' ],
    ['inner_h', '12.7 38.1 0', '0 0 90' ],
    ['outer_v', '0 256.3 -395.95', '90 90 90' ],
    ['inner_v', '12.7 256.3 -370.55', '270 90 0' ],
    ['outer_v', '0 256.3 395.95', '270 90 270' ],
    ['inner_v', '12.7 256.3 370.55', '90 270 0' ],
    ['outer_h_top', '0 500.0 0', '180 0 0' ],
    ['inner_h', '12.7 474.4 0', '0 0 90' ],
    ['lock_bar', '-25.4 256.3 186.4', '90 270 0' ],
    ['lock_bar', '-25.4 256.3 -186.4', '90 270 0' ],
]

# cqe.cqassemble(asm, name='assembly')
# load the STEP files to build the .STEP assembly file
inner_h = cqtools._loadSTEP('downloads/inner_h.STEP')
inner_v = cqtools._loadSTEP('downloads/inner_v.STEP')
outer_h_bottom = cqtools._loadSTEP('downloads/outer_h_bottom.STEP')
outer_h_top = cqtools._loadSTEP('downloads/outer_h_top.STEP')
outer_v = cqtools._loadSTEP('downloads/outer_v.STEP')
stand = cqtools._loadSTEP('downloads/stand.STEP')
lock_bar = cqtools._loadSTEP('downloads/lock_bar.STEP')

asm2 = [
    (stand
         .rotate((0,0,0), (0,1,0), 90)
         .translate((0, 0, 186.4))
         .findSolid()
    ),
    (stand
         .rotate((0,0,0), (0,1,0), 90)
         .translate((0, 0, -186.4))
         .findSolid()
    ),
    (outer_h_bottom
         .rotate((0,0,0), (1,0,0), 0)
         .translate((0, 12.7, 0))
         .findSolid()
    ),
    (inner_h
         .rotate((0,0,0), (0,0,1), 90)
         .rotate((0,0,0), (1,0,0), 180)
         .translate((12.7, 38.1, 0))
         .findSolid()
    ),
    (outer_v
         .rotate((0,0,0), (1,0,0), 270)
         .rotate((0,0,0), (0,0,1), 180)
         .translate((0, 256.3, -395.95))
         .findSolid()
    ),
    (inner_v
         .rotate((0,0,0), (0,0,1), 90)
         .rotate((0,0,0), (1,0,0), 270)
         .translate((12.7, 256.3, -370.55))
         .findSolid()
    ),
    (outer_v
         .rotate((0,0,0), (1,0,0), 90)
         .rotate((0,0,0), (0,0,1), 180)
         .translate((0, 256.3, 395.95))
         .findSolid()
    ),
    (inner_v
         .rotate((0,0,0), (0,0,1), 90)
         .rotate((0,0,0), (1,0,0), 90)
         .translate((12.7, 256.3, 370.55))
         .findSolid()
    ),
    (outer_h_top
         .rotate((0,0,0), (1,0,0), 180)
         .translate((0, 500.0, 0))
         .findSolid()
    ),
    (inner_h
         .rotate((0,0,0), (0,0,1), 90)
         .translate((12.7, 474.4, 0))
         .findSolid()
    ),
    (lock_bar
         .rotate((0,0,0), (0,0,1), 90)
         .rotate((0,0,0), (1,0,0), 270)
         .translate((-25.4, 256.3, 186.4))
         .findSolid()
    ),
    (lock_bar
         .rotate((0,0,0), (0,0,1), 90)
         .rotate((0,0,0), (1,0,0), 270)
         .translate((-25.4, 256.3, -186.4))
         .findSolid()
    ),
]

# Some weird syntax to properly create the compound geometry
# There is likely a cleaner way to do this, but I'm unaware currently
final = cq.cq.Compound.makeCompound(asm2)
assembly = cq.CQ(final)
show_object(assembly)
