int i;
int nDots = 12;       // Number of dots
int r = 20;           // Radius of small dots
int R = 120;          // Radius of dot ring
float angle, x, y;
Dot[] dots = new Dot[nDots];

void setup() {
  size(400, 400);
  background(220);
  pushMatrix();
  translate(width/2, height/2);
  for (i=0; i < nDots; i++) {        // Creates and displays dot ring
    x = cos(angle)*R;
    y = sin(angle)*R;
    dots[i] = new Dot(x, y, r, color(40));
    dots[i].display();
    angle += (2*PI/nDots);
  }
  popMatrix();
}

void draw() {
  if (keyPressed) { 
//    if (key == 's') { d1.shrink(); }
  //  else if (key == 'e') { d1.enlarge(); }
  }

}

boolean overlap(int x1, int y1, int r, int x2, int y2) {
  /* Checks if an object (specialized to circles) overlaps with another object 
  by comparing whether both the ranges of x-values and y-values overlap with 
  one another. */
  boolean ovx, ovy, itx, ity;
  ovx = inRangeInc(x2, x1-r, x1+r);
  ovy = inRangeInc(y2, y1-r, y1+r);
  itx = inRangeExc(x2, x1-r, x1+r);
  ity = inRangeInc(y2, y1-r, y1+r);
  if (ovx && ovy) { return true; }
  else if ((ovx || ovy) && (itx || ity)) { return true; }
  else { return false; }
}

boolean inRangeInc(int v, int start, int stop) {
  /* Checks if a value is in a specified range, endpoints included. Value of start is 
  assumed to be less than the value of stop. */
  if (v >= start && v <= stop) { return true; }
  else { return false; }
}

boolean inRangeExc(int v, int start, int stop) {
  /* Checks if a value is in a specified range, endpoints excluded. Value of start is 
  assumed to be less than the value of stop. */
  if (v > start && v < stop) { return true; }
  else { return false; }
}