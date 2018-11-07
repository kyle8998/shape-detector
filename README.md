# shape-detector

Describe polygons on a grid.

### How to run

```python3 shape_detect.py <FILEPATH HERE>```

`python3 shape_detect.py ./test.json`

### My Approach

 When I first saw this problem, I thought of a similar problem where you have
 to see if a point is inside a shape. You can do this by creating an infinite
 line coming out of the point and counting the intersections with the shape.
 If there is a even amount of intersections it is outside, and otherwise inside.
 You can determine intersections of two lines by playing around with the
 orientation of the 4 points (as done in the orientation method).

 I modified this approach to work for entire shapes. I go through the points
 of every shape and I compare it to every other shape. We have 4 cases.
 
 1. No points intersect
 2. Some Points Intersect
 3. All points are inside
 4. All points outside

 I base my points around these cases. By checking each point, we can easily see
 if it fits one of the scenarios. The only special case is that an outer shape
 doesn't necessarily intersect an inner shape. I just went around this by
 checking the states after the initial run. If we saw a shape inside another shape,
 we know to change the other shape to have a surrounding state. Once I set the
 proper states, I simply print out the values.