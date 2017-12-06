// Try clicking or pressing SPACE.

import gifAnimation.*;

// Number of unique control points (per curve). Processing's bezier function only
// accepts 4 pairs of x,y coordinates (boo), so don't change this or nothing will work.
// tl;dr DO NOT TOUCH.
int nPoints = 4;

// Array of Point arrays. Each Point array corresponds to one bezier curve.
Point[][] curves = {};

int r = 10;             // radius
color c;
int sWeight = 4;        // stroke weight
int buffer = 60;         // width of the buffer zone
float step, t;
boolean write;
//GifMaker gifExport;

void setup() {
  size(540, 540);
 frameRate(45);
  curves = (Point[][]) append(curves, genPoints());  // one is the loneliest number
  for (int p = 0; p < 30; p++) {
    curves = (Point[][]) append(curves, genPoints());
  }
  //gifExport = new GifMaker(this, "cluster420n30.gif");
  //gifExport.setRepeat(0);
  //gifExport.setDelay(35);
}

// Main loop
void draw() {
  background(230);
//  println(frameRate);
  int i;            // counter
  
  // Generates a new bezier curve.
  //if (curves.length < 51 && (mousePressed || (keyPressed && key == ' ')))
  //  { curves = (Point[][]) append(curves, genPoints()); }
   
  // Draws each curve whose control points are stored in 'curves' (type Point[][]), 
  // plus associated control lines and traveling circles ('ball'). 
  // Style changes are a pain.
  for (i = 0; i < curves.length; i++) {
    arrBez(curves[i]);
    c = color(0, 20);
    drawCtrlLn(curves[i], sWeight+2, c);
    c = color(0, 30);
    t = map(step, 0, 80, 0, 1);
    Point[] nCurve = intBez(t, curves[i], c);
    drawCtrlLn(nCurve, sWeight, c);
    c = color(0, 40);
    Point[] n2Curve = intBez(t, nCurve, c);
    drawCtrlLn(n2Curve, sWeight, c);
    fill(60);
    noStroke();
    Point ball = new Point(arrBezPoint(curves[i], "x", t), arrBezPoint(curves[i], "y", t));
    ellipse(ball.x, ball.y, r, r);
  }
  
  // Animate! (see line 33)
  if (step == 80) { 
    step = 0; 
    //noLoop();
    //gifExport.finish();
  } else { 
    step++; 
    //gifExport.addFrame();
  }
}

// Functions

// arrBez and arrBezPoint mimic built-in Bezier functions (bezier and bezierPoint 
// respectively) but have been tailored to take a reduced number of arguments for 
// convenience. You can see how annoying it can get below.
void arrBez(Point[] points) {
  noFill();
  stroke(10, 99);
  strokeWeight(2);
  bezier(points[0].x, points[0].y, points[1].x, points[1].y, points[2].x, points[2].y, points[3].x, points[3].y);
}

float arrBezPoint(Point[] curve, String mode, float t) {
  if (mode == "x") { return bezierPoint(curve[0].x, curve[1].x, curve[2].x, curve[3].x, t); }
  else { return bezierPoint(curve[0].y, curve[1].y, curve[2].y, curve[3].y, t); }
}
  
// Draws control lines for a Point array (Bezier curve).
void drawCtrlLn(Point[] curve, int sW, color c) {
  int i;
  fill(c);
  for (i = 0; i < curve.length-1; i++) {
    strokeWeight(sW);
    stroke(c);
    line(curve[i].x, curve[i].y, curve[i+1].x, curve[i+1].y);
  }
}

// Draws control lines for all the lower-order curves of a given curve.
Point[] intBez(float t, Point[] curve, color c) {
  int i;
  Point[] points = {};
  stroke(c);
  Point initPt, newPt;
  for (i = 0; i < curve.length-2; i++) {
    strokeWeight(3);
    initPt = new Point(map(t, 0, 1, curve[i].x, curve[i+1].x), map(t, 0, 1, curve[i].y, curve[i+1].y));
    newPt = new Point(map(t, 0, 1, curve[i+1].x, curve[i+2].x), map(t, 0, 1, curve[i+1].y, curve[i+2].y));
    points = (Point[]) append(points, initPt);
    if (i == 0) { line(curve[0].x, curve[0].y, initPt.x, initPt.y); }
    if (i == curve.length-3) {
      line(newPt.x, newPt.y, curve[curve.length-1].x, curve[curve.length-1].y);
      points = (Point[]) append(points, newPt);
    }
  }
  return points;
}

// Generates coordinates for the control points of a new curve. 
// Coordinates are determined randomly from the width and height of the window, 
// excluding a pre-defined buffer zone (stored in 'buffer').
Point[] genPoints() {
  int i;
  Point[] points = new Point[nPoints];
  points[0] = new Point(width/2, height/2);
  points[nPoints-1] = points[0];
  for (i = 1; i < nPoints-1; i++) {
    points[i] = new Point(random(buffer, width-buffer), random(buffer, height-buffer));
  }
  return points;
}