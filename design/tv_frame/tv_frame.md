
# Building a TV Frame

Several years ago I built a weird looking desk that had a PC and TV built right in. It never progressed beyond 'usable prototype', and was eventually disassembled. The TV had been partially stripped down to fit nicely in the desk's surface, and the old parts were discarded.

![](img/old_desk.jpg)

Since the TV is still good, I want to design a frame and stand that will allow me to actually use it again.

## Requirements

The frame must meet the following criteria:

* look decent
* be of sound construction, meaning: all connections must be *tight* and secure.
* cover the loose circuit board on the front
* not obstruct any ports on the back of the TV
* provide mounting points on the base for a simple stand
* allow for standard TV mounting hardware to still fit on the back of the TV

## Details and Images

Before the design can properly begin, some measurements will be needed. I walked around the shop and discovered a half-used bundle of some interesting material. 

![](img/raw_material.jpg)

After checking that it was actually OK to use a length or two of this (it was), I pulled one length out and measured. The dimensions are shown below.

<center>![](img/profile.svg)</center>

Conveniently, there is a *work in progress* dxf importer for CadQuery that should make it much simpler to work with 2D objects.

So, I made a **.dxf** file very similar to the above SVG, and imported it to create the tube that I'll use to define all of the tv frame's parts.


```python
# make a simple sample piece 
# to try out the dxf import function
sample_tube = (cq.Workplane('XY')
               .workplane(offset=-1)
               .dxf('downloads/profile.dxf')
               .extrude(2)
              )

show_object(sample_tube)
```

Alright, it works! Now I can work on the actual design.

## Parts Plan

This design is going to be a bit more advanced than my [ipad_stand](https://rustyvermeer.github.io/design/ipad_stand/index.html), so I've got a mental picture in mind that will take a few different parts:

* outer frame composed of:
    * horizontal bar bottom (1x)
    * horizontal bar top (1x)
    * vertical bar (2x)
* inner frame composed of:
    * horizontal bar (2x)
    * vertical bar (2x)
* back lock bar (2x)
* stand bar (2x)

Naming things is, generally speaking, a difficult thing to do. As such, it's much more sensible to *see* the parts than it is to rely solely on names. The next steps will be defining the CadQuery code to generate all of the parts in the list.    

# Outer Frame Horizontals

The horizontal frame pieces are identical, with a small exception for the bottom bar: two holes are cut in order to provide a mounting location for the legs.

## Outer Horizontal Top


```python
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
               .faces('>Y').workplane()
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
```

    newCenter = (0.0, -1.6653345369377348e-16)
    newCenter = (0.0, -1.6653345369377348e-16)










    exported model as: outer_h_bottom.STEP
    exported model as: outer_h_bottom.JSON


## Outer Horizontal Bottom


```python
tap_025 = 0.201

outer_h_bottom = (outer_h_top
                  .faces('<Y').workplane(centerOption='CenterOfBoundBox')
                  .pushPoints([(0.0,  7.3386),
                               (0.0, -7.3386)])
                  .hole(tap_01875, depth=0.08)
                 )

show_object(outer_h_bottom)
```

## Outer Verticals


```python
L = 19.6693 # comes from height of scrn + offset due to tube dims
tap_01875 = 0.1495

outer_v = (cq.Workplane('XY')
               .workplane(offset=-L/2.0)
               .dxf('downloads/profile.dxf')
               .extrude(L)
               # holes on top face near edge
               # will be tapped with 3/16 bolt thread
               # used to mount inner frame tube
               .faces('>Y').workplane()
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
               .moveTo(0.0, 0.135).rect(0.85, 0.25, centered=True)
               .cutBlind(-0.5, clean=True)
               .faces('>Z').workplane(centerOption='CenterOfBoundBox')
               .moveTo(0.0, -0.135).rect(1.0, 0.25, centered=True)
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
```

## Inner Frame Horizontals and Verticals

The inner frame components are identically designed. The horizontal bars are equivalent, as are the vertical bars. The only difference between the verticals and horizontals is the length. As such, the following code is parametric according to L, the tube's total length.


```python
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
```

### Inner Horizontals


```python
show_object(inner_h)
```

### Inner Verticals


```python
show_object(inner_v)
```

## Stands


```python
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
```

## Lock Bars


```python
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
               .faces('>X').workplane()
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
```

# Design Assembly

This frame is a bit more complex of an assembly, so the following code might get a bit messy. It'll show off the intended design, though.


```python
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
    ['outer_v', '0 254.9 -395.95', '90 90 90' ],
    ['inner_v', '12.7 254.9 -370.55', '270 90 0' ],
    ['outer_v', '0 254.9 395.95', '270 90 270' ],
    ['inner_v', '12.7 254.9 370.55', '90 270 0' ],
    ['outer_h_top', '0 498.6 0', '180 0 0' ],
    ['inner_h', '12.7 474.2 0', '0 0 90' ],
    ['lock_bar', '-25.4 255.9 186.4', '90 270 0' ],
    ['lock_bar', '-25.4 255.9 -186.4', '90 270 0' ],
]

# cqe.cqassemble(asm, name='assembly')

# base_part = cqtools._loadSTEP('base.STEP')
# vert_part = cqtools._loadSTEP('vert.STEP')
# support_part = cqtools._loadSTEP('support.STEP')

# asm2 = [
#     base_part.findSolid(),
#     (vert_part
#          .rotate((0,0,0), (1,0,0), 270)
#          .translate((0, 76.2, 222.25))
#          .findSolid()
#     ),
#     (vert_part
#          .rotate((0,0,0), (1,0,0), 270)
#          .translate((0, -76.2, 222.25))
#          .findSolid()
#     ),
#     (support_part
#          .rotate((0,0,0), (0,1,0), 90)
#          .rotate((0,0,0), (1,0,0), 270)
#          .translate((38.1, 247.65, 76.2))
#          .findSolid()
#     ),
#     (support_part
#          .rotate((0,0,0), (0,1,0), 90)
#          .rotate((0,0,0), (1,0,0), 270)
#          .translate((38.1, 247.65, -76.2))
#          .findSolid()
#     ),
# ]

# Some weird syntax to properly create the compound geometry
# There is likely a cleaner way to do this, but I'm unaware currently
# final = cq.cq.Compound.makeCompound(asm2)
# final = cq.CQ(final)
# show_object(final)
```

<iframe width="650" height="500" src="assembly.html?overflow=none" frameborder="0" allowfullscreen=""></iframe>

# Building it for Real

Once again I find myself kicking the laser tube cutter into action. I'm extremely lucky to remember how this thing works. As it turns out, I need to be good at last second maintenance for this thing. I had to search the shop for some hydraulic oil to top up the reservoir! Fortunately, everything still works.

<center><video style="margin-left: 0;" width="300" height="300" autoplay="" muted="" loop="" controls="">
  <source src="img/cutting.mp4" type="video/mp4">
</video></center>

With all the parts cut, it simply comes down to assembly. The pictures below show the process, more or less. Of course, the struggle of tapping the holes and tightening up all of the screws is not pictured.

<iframe width="650" height="700" src="img/asm_imgs.html?overflow=none" frameborder="0" allowfullscreen></iframe>

## Final Thoughts

I can finally use my TV again. Mission accomplished! I like the industrial look to the whole thing, too; I suspect there's no TV quite like this one.

Yet as always, there is room for improvement.

### Process Improvements

* tapping holes makes for some nice construction, but is tedious to do. Reduce how many bolted connections are needed to reduce this.
* it might be good to include more hand-drawn sketch images in these notebooks, to convey the initial thinking phases of my design work. I could alternatively create some basic 2D layout drawings in .dxf format. With that, I could potentially have some fancy import functions that semi-automatically place 3D objects according to some layout drawing. Lot's of potential there, for sure.

### Design Improvements

* I cut 5 holes for screws in every side. I tried using only 3 holes, and it held things together perfectly, so there was no need for so much cutting.
* The 0.5in 'lip' added to the TV does *slightly* interfere with the image when viewing at extreme angles. That fact paired with the reflectivity of the surface can cause some distraction. I only view casually anyway, so this doesn't bother me. It's definitely not good enough for the average consumer, though.
* Finishing. I like the industrial look, but it could be out of place in most homes. A nice powder coated finish could look really sharp.
* Weight. This thing is **heavy**. I like it that way, but it's certainly excessive. I could strategically cut holes on all inner faces to drastically cut down weight. Or I could make a triangular cut out pattern part of the aesthetic of the frame. As well, I could re-think the front frame portion as a flat sheet or even as a piece of plastic or wood to cut down a lot of weight.
* don't forget the remote! I forgot that the only way to turn the TV on is via the remote control (power button was attached to the old bezel). You can't shoot IR signals through solid metal, so I had to drill a hole that aligns with the sensor. Silly thing to forget.
    
There it is, my design and build of an industrial-strength TV frame. Thanks for reading through my article. If you have any questions or suggestions, I'm glad to listen! Please ask away on my Twitter, [@RustyVermeer](https://www.twitter.com/RustyVermeer).


```python
!jupyter nbconvert --to markdown tv_frame.ipynb

import page_tools as pg
pg.generate_page('tv_frame', color='#858a7e')
```

    [NbConvertApp] Converting notebook tv_frame.ipynb to markdown
    /usr/local/lib/python2.7/dist-packages/nbconvert/filters/datatypefilter.py:41: UserWarning: Your element with mimetype(s) [u'application/vnd.jupyter.widget-view+json'] is not able to be represented.
      mimetypes=output.keys())
    [NbConvertApp] Writing 14325 bytes to tv_frame.md
    Created index.html

