import json
import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def orientation(a, b, c):
    """
    Given three points, find the orientation.
    See examples below. They are colinear(0), clockwise(1), and
    counterclockwise(2) respectively.
    c
    |
    b   b_c   c_b
    |   |       |
    a   a       a
    """ 
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y) 
  
    # If equal to 0 -> colinear, >0 -> clockwise, <0 -> counterclockwise
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def inBetween(p1, mid, p2):
    """
    Determine whether if point mid in on the line p1p2
    """
    return (mid.x <= max(p1.x, p2.x) and mid.x >= min(p1.x, p1.x) and
            mid.y <= max(p1.y, p2.y) and mid.y >= min(p1.y, p2.y))
        
def intersect(a, b, c, d):
    """
    determine if line ab intersects with line cd
    Cases when the segments intersect:
    1. (a,b,c) != (a,b,d) && (c,d,a) != (c,d,b)
    2. All orientations are colinear, but one line lies on the other
    """
    
    # First we find the orientation of each set of 3 points
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)
    
    # Case 1: Different orientations
    if o1 != o2 and o3 != o4:
        return True
  
    # Case 2: If colinear and lines lie on each other
    # Otherwise return false
    return (o1 == 0 and inBetween(a, c, b)) or (o2 == 0 and inBetween(a, d, b)) or \
           (o3 == 0 and inBetween(c, a, d)) or (o4 == 0 and inBetween(c, b, a))
           
def inside(p1, polygon):
    """
    Determine if a point is inside a polygon
    We can do this by extending an infinite line from the point and checking its intersections
    If it has an odd amount of intersections it is inside, otherwise outside
    """
    # The point should go toward infinity, just make it a large number to avoid issues
    p2 = Point(10000, p1.y)
    
    count = 0
    for i in range(-1, len(polygon)-1):
        poly1 = Point(polygon[i][0], polygon[i][1])
        poly2 = Point(polygon[i+1][0], polygon[i+1][1])
        if intersect(p1, p2, poly1, poly2):
        
            #if (orientation(poly1, p1, poly2) == 0): 
            #    return inBetween(poly1, p1, poly2)
            count += 1
    
    return count % 2 == 1

if __name__ == '__main__':
    # Argument parsing
    # Asks for filepath if not provided
    if not sys.argv[1:]:
        filename = input('Enter path to your JSON file: ')
    else:
        filename = sys.argv[1]

    with open(filename) as json_data:
        data = json.load(json_data)

    # Assuming file is valid
    shapes = data['shapes']
    
    # Create structure to hold the results, ids, and states
    results = {}
    ids = []
    # id -> id -> number
    # 0=inside, 1=intersect, 2=separate, 3=surrounds
    states = [" is inside shape ", " intersects shape ", " is separate from shape ", " surrounds shape "]
    
    # Loop through all shapes, and compare their points to every point in every other shape
    for shape1 in shapes:
        # Create dict to hold results and array to keep order of ids
        results[shape1['id']] = {}
        ids.append(shape1['id'])
        for shape2 in shapes:
            if shape1 is shape2: continue
            
            # See how many points are inside
            count = 0
            for (x,y) in shape1['points']:
                point = Point(x,y)
                # If point is inside
                if inside(point, shape2['points']):
                    count += 1
            if count == len(shape1['points']):
                # all points inside
                results[shape1['id']][shape2['id']] = 0
            elif count > 0:
                # Some points inside
                results[shape1['id']][shape2['id']] = 1
            else:
                results[shape1['id']][shape2['id']] = 2
                
    # The only special cases will the ones that classify as separate or intersect.
    # It may classify surrounds or intersect as separate because we only check if points are in other polygons
    # Let's go through and manually change them by using our other results
    # Also because dicts do not guarentee order, I iterate using a list
    for id in ids:
        for k in ids:
            if id == k: continue
            if results[id][k] == 1 or results[id][k] == 2:
                if results[k][id] == 0:
                    results[id][k] = 3
                elif results[k][id] == 1:
                    results[id][k] = 1
                    
            print("Shape " + id.upper() + states[results[id][k]] + k.upper())
