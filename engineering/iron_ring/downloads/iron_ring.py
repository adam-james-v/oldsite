import math

# R is outer radius of ring
# T is NOT the ring's thickness radially 
# but vertically, if the ring is resting on a surface
# ie, the hollow cylinder that is the ring has a HEIGHT of T
R = 9.5
T = 3.0

# Make a function that radially patterns points
def list_points(r, a, N):
    '''Radially pattern points
    
    r: the radius of the circle on which points are placed
    a: an offset angle from the x axis, CCW, in degrees
    N: number of points to place radially along. 
       Spaces evenly along full 360 circle
    '''
    arad = math.radians(a)
    theta = math.pi*2 / N
    pnts = []
    
    for i in range(0, N):
        coord = (r*math.cos(theta*i + arad), r*math.sin(theta*i + arad))
        pnts.append(coord)
        
    return pnts

# Create a plain ring, centered in the plane and around the origin
ring = (cq.Workplane("XZ").workplane(offset=(-T/2.0))
    .circle(R).extrude(T)
    .faces("<Y").workplane(invert=True)
    .circle(R-(R*0.145)).cutBlind(T)
)

# Make spheres on top and bottom of ring
# These will be cut away from the ring 
# To make the 'divets' of an iron ring
spheres1 = cq.Workplane("XZ").workplane(offset=(T-0.4))
spheres2 = cq.Workplane("ZX").workplane(offset=(T-0.4))

for point in list_points((R*1.789), 0, 8):
    spheres1 = spheres1.moveTo(point[0], point[1]).sphere(R*0.8526)
    
for point in list_points((R*1.789), 22.5, 8):
    spheres2 = spheres2.moveTo(point[0], point[1]).sphere(R*0.8526)

iron_ring = ring.cut(spheres1).cut(spheres2)

show_object(iron_ring)