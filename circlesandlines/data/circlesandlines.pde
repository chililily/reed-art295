// notes/to-do
// * build+save c3. currently the colours are set through FIVE DIFFERENT for loops.
//   the horror.
// * fix the zoom

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

String filename = "hahahaha.txt";
String[] words;

IntDict charFreqs = new IntDict();
IntDict cxns = new IntDict();
float totalChars;

//CharNode[] nodes = new CharNode[0];
HashMap <String, CharNode> nodes = new HashMap <String, CharNode> ();
CharNode[] nums = new CharNode[0];
CharNode[] vowels = new CharNode[0];
CharNode[] cons = new CharNode[0];
CharNode[] syns = new CharNode[0];
CharNode[] specs = new CharNode[0];
Cxn[] lines = new Cxn[0];

Table c3;    // character-colour codes. yay alliteration!
Table ascii;

float angle;
float scale;

boolean move;
boolean showLabels;

void setup() {
  c3 = loadTable(dataPath("c3.csv"), "header");
  ascii = loadTable(dataPath("ascii.csv"), "header");
  
  // Creates a subfolder for the input file in the data folder and moves the input file 
  // into that folder.
  File f = new File(dataPath(filename));
  if (f.exists()) {
    words = getWords(dataPath(filename));
    if (!(filename == "ascii.csv" || filename == "chromadict.csv")) {
      move = true;
    }
  } else {
    words = getWords(dataPath(split(filename, ".")[0]+"/"+filename));
  }
  
  // Get the count for each character represented in the text data.
  for (int i=0; i < words.length; i++) {
    totalChars += countChars(words[i]);
  }
  
  makeNodes(charFreqs);
  makeCxns(cxns);
  
  size(750,750);
}

void draw() {
  background(25);
  pushMatrix();
  translate(width/2, height/2);
  if (key == 'r') {
    rotate(angle);
    angle += .005;
  }
  for (int i=0; i < lines.length; i++) {
    lines[i].connect();
  }
  for (String Key: nodes.keySet()) {
    CharNode n = nodes.get(Key);
    n.display();
    if (showLabels || n.hover(mouseX, mouseY)) {
      n.label();
    }
    if (mousePressed && n.hover(pmouseX, pmouseY)) {
      n.move(mouseX, mouseY);
    }
    if (keyPressed) {
      if (key == ' ') {
        n.reset();
      // Zoom. It doesn't work that well right now.
      } else if (keyCode == UP) {
        scale += 0.01;
        n.zoom();
      } else if (keyCode == DOWN) {
        scale -= 0.01;
        n.zoom();
      }
    }
  }
  popMatrix();
  
  // Display word count in bottom right corner.
  pushStyle();
  fill(80);
  textAlign(RIGHT,BOTTOM);
  textSize(10);
  text(words.length,width-5,height-20);
  text(int(totalChars),width-5,height-5);
  popStyle();
  
  // TO DO
  // input---
  // zoom?
  if (keyPressed) {
    if (key == 's') {
      save(dataPath(split(filename, ".")[0]+".jpg"));
    } else if (key == 'l') {
      if (showLabels) {
        showLabels = false;
      } else {
        showLabels = true;
      }
    }
  }
  
  //if (move) {
  //  File source = new File(dataPath(filename));
  //  File dest = new File(dataPath(split(filename, ".")[0]+"/"+filename));
  //  source.renameTo(dest);
  //  move = false;
  //}
}