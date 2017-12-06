PFont aMono;
int h, m, s, hX, mX, sX;
String time, hxd;

void setup() {
  size(400, 200);
  textSize(18);
  fill(240);
  aMono = createFont("Andale Mono", 18);
  textFont(aMono);
}

void draw() {
  h = hour();
  m = minute();
  s = second();
  hX = int(map(h, 0, 60, 0, 255));
  mX = int(map(m, 0, 60, 0, 255));
  sX = int(map(s, 0, 60, 0, 255));
  background(hX, mX, sX);
  time = nf(h, 2) + ":" + nf(m, 2) + ":" + nf(s, 2);
  hxd = "#" + hex(hX, 2) + hex(mX, 2) + hex(sX, 2);
  textAlign(CENTER);
  text(time, width/2, height/2);
  text(hxd, width/2, height*2/3);
}