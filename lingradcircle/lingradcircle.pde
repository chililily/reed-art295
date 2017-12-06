// Constants
color b1, b2, c1, c2;

void setup() {
  size(640, 360);

  // Define colors
  c1 = color(204, 102, 0);
  c2 = color(0, 102, 153);

  noLoop();
}

void draw() {
  linGradCirc(50.0, 190.0, 20.0, c2, c1);
}

void linGradCirc(float x, float y, float r, color c1, color c2) {
  /* Creates a circle, with origin at (x, y) and radius r, filled with a linear 
  (left to right) gradient that goes from c1 to c2. */
  float cY;
  noFill();
  pushMatrix();
  translate(x, y);            // sets circle's origin to (x, y)
  for (float i = -r; i <= r; i += 0.01) {
    float inter = map(i, -r, r, 0, 1);
    color c = lerpColor(c1, c2, inter);
    stroke(c);
    cY = sin((acos(i/r)))*r;  // calculates the y-coordinate of the line to be created
    line(i, cY, i, -cY);
  }
  popMatrix();
}