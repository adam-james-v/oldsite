
# Designing an iPad Pro Stand

I love my iPad Pro. It is very light and very powerful. With the Smart Keyboard cover and the Pencil, I can use the iPad for nearly all of my computing needs (with assistance of a virtual private server for more technical tasks). 

However, after extended time working, I notice a pain in my neck. Sadly, there is no comfortable way to adjust the placement of the iPad relative to the keyboard.

My solution: purchase a bluetooth keyboard to allow de-coupled typing. Problem solved, right?

Well, almost. I could certainly adjust the iPad's location relative to my hands for typing, which was a huge step up, but the height adjustment left something to be desired. {Author's note: place picture of iPad on stack of textbooks or something}.

So I decided to stretch my designer / builder muscles and solve my problem!

Below are the designs for each component of the iPad stand I built. 

NOTE:
- explain Jupyter Notebooks
- explain CadQuery
- explain A-Frame VR for showing off the final solution
- share downloads of STEP files? 
- also share a BOM of parts used. Hopefully I can provide source-able alternatives to the custom pieces.

## Define a Tube Function

Since the design is going to use tubes, it makes sense to define a simple function to quickly create them. In this case, I know that I only want to use rectangular tubes, so I'll define a function that takes:

* base dimension of the tube's cross section
* height dimension of the tube's cross section
* thickness of the tube, assuming the thickness is added inwards from the base and height
* total length of the tube

Edge radius of the tube is going to be internally defined in the function for simplicity. In actuality, the radius may not strictly be computable from the given dimensions. In such situations, a lookup table of radius values would have to be employed. Since these parts will only be dealt with in very small quantity, I don't care to build a whole database of materials and will simply make an assumption about the radius.

For a personal project, that will certainly be good enough.


```python
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
```

# Build the Base


```python
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
```









# Set Up the Stand

Now that we've prepared a base, it's time to make the vertical arms that will actually hold the iPad up at a comfortable height. 

I want to keep my neck fairly straight while using this, and prefer to maintain a good posture while I work, so I'll set things fairly high up.

The benefit of a high stand is that I could also move it to a standing desk and still have the screen located at a decent height, requiring only a minor angle to my neck.

At least, that's the theory. I'll find out in practice if the height's good. At least I can always re-build the stand, if it comes to it. Let's plan for success, though.

For variety, I'll use some smaller scrap tubing that looks quite nice.

(Insert scrap tube image here)


```python
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
```









# Create the Support Arms

To actually hold the iPad up, some horizontal support arms will be necessary. It's sensible to use the same tube as is used for the vertical components, because it eliminates the need to change the machine over to a different material size a third time. It also looks quite nice when parts have a smooth interface between them. By that I simply mean that I like it when things line up.

The iPad's angle shouldn't be too great, either, so that's a design consideration. The closer to vertical the better, since the screen is already going to sit at eye level. But, since this stand will be relying solely on gravity, it would be unstable to design the iPad to sit perfectly vertical. It would fall over.

So, I'll make a horizontal arm that extends out about 2 inches and provides a small lip for the iPad to catch on, preventing sliding. The vertical supports will serve as the backrest, preventing it from falling backwards.

Foam will be placed on all metal surfaces that will come in contact with the device; I don't want scratches on my nice toys!


```python
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
```










```python
import cqjupyter_extras as cqe 

asm = [
    ['base', '0 0 0', '0 0 0' ],
    ['vert', '0 222.25 76.2', '270 0 0' ],
    ['vert', '0 222.25 -76.2', '270 0 0' ],
    ['support', '38.1 247.65 76.2', '0 90 270' ],
    ['support', '38.1 247.65 -76.2', '0 90 270' ],
]

cqe.cqassemble(asm, name='assembly')
```


```python
asm2 = [
    base.findSolid(),
    vert.translate((0.0, 0.0, 0.0)).rotate((0,0,0), (1,0,0), 270).findSolid(),
    #vert,
    #support,
    #support,
]


def grab_source(key):
    has_assign = [i for i,inpt in enumerate(In) if key + ' =' in inpt] #find all line indices that have `=`z
    has_assign.sort()
    for idx in has_assign:
        inpt_line_tokens = [token for token in In[idx].split(' ') if token.strip() != '']
        indices = [i for i,token in enumerate(inpt_line_tokens) if '=' in token]
        for i,pntr in enumerate(indices):
            if inpt_line_tokens[pntr - 1].split()[-1] == key:
                return inpt_line_tokens[pntr - 1].split()[-1] + ' ' + ' '.join(inpt_line_tokens[pntr:])

blarg = grab_source('a')
print blarg
print blarg.count('\n\n')

# final = cq.cq.Compound.makeCompound(asm2)
# final = cq.CQ(final)
# show_object(final)
```
