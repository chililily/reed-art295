class Dot {
  float x, y, r;
  int maxr;
  boolean state;
  color c;

  Dot(float posx, float posy, int radius, color clr) {
    x = posx;
    y = posy;
    r = radius;
    maxr = radius;
    c = clr;
  }
  
  void display() {
    noStroke();
    fill(c);
    ellipse(x, y, r, r);
  }
  
  void shrink() {
    if (r > 0) { 
      background(220);
      r -= 0.5;
      ellipse(x, y, r, r);
    }
  }
  
  void enlarge() {
    if (r < maxr) {
      background(220);
      r += 0.5;
      fill(c);
      ellipse(x, y, r, r);
    }
  }
}