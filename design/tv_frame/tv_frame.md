
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
               # 3 pairs of 3/16 tapped holes
               # will mount back 'lock bar' tubes
               .faces('<X').workplane()
               .pushPoints([(0.0,  0.5),
                            (0.0, -0.5),
                            (0.0, 8.8386),
                            (0.0, 7.8386),
                            (0.0, -8.8386),
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
