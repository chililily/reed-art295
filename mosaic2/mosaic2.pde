// KEY FUNCTIONS
// 'h' - HSB mode
// 'r' - RGB mode (default)
// SPACE - switch color mode
// 'f' - continuously switch color modes

// For some reason, there's occasionally an error finding 't' in ascii.csv. 
// My guess is that for whatever reason, it's not the "standard" 't' and so 
// isn't getting read as 't' but, on a low level, as some other character that 
// isn't included in ascii.csv. Or it could just be a random error.

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

String filename = "aeneid.txt";    // file MUST be in data folder
String[] words;

Table chromadict;
Table ascii;

float isize;
int dimension;
float x, y;
color c, crgb, chsb;

String cmode = "rgb";
int save = 0;
//boolean move = false;

void setup() {
  // Checks if there is a file chromadict.csv.
  // If so, load the data into a Table. If not, create a new Table.
  File f = new File(dataPath("chromadict.csv"));
  if (f.exists()) {
    chromadict = loadTable(dataPath("chromadict.csv"), "header");
  } else {
    chromadict = new Table();
    chromadict.addColumn("words");
    chromadict.addColumn("rgb", Table.INT);
    chromadict.addColumn("hsb", Table.INT);
  }
  ascii = loadTable(dataPath("ascii.csv"), "header");

  f = new File(dataPath(filename));
  if (f.exists()) {
    words = getWords(dataPath(filename));
    //if (!(filename == "ascii.csv" || filename == "chromadict.csv")) {
    //  move = true;
    //}
  } else {
    words = getWords(dataPath(split(filename, ".")[0]+"/"+filename));
  }
  
  // Determines size of the color blocks from the word count and window size.
  size(750,750);
  isize = width/sqrt(words.length);
  dimension = int(sqrt(words.length)*isize);
  println("Word count: " + words.length);
  println("Words per line: " + int(sqrt(words.length)));
  println("Word block size: (" + isize + " px)^2");
  
  // Style things.
  noStroke();
  rectMode(CENTER);
  frameRate(10);
}


void draw() {
  // Initial position.
  x = isize/2;
  y = isize/2;
  background(0);
  
  // Keyboard functions.
  // SPACE - changes color mode
  // r - RGB mode
  // h - HSB mode
  // f - flips between the modes; press any other button to stop looping
  if (keyPressed) {
    if ((key == ' ' && (cmode.equals("rgb")) || (key == 'h'))) {
     //colorMode(RGB);
     cmode = "hsb";
    } else if ((key == ' ' && (cmode.equals("hsb")) || (key == 'r'))) {
     //colorMode(HSB);
     cmode = "rgb";
    }
  }
  if (key == 'f') {
    if (cmode == "rgb") {
      //colorMode(RGB);
      cmode = "hsb";
    } else {
      //colorMode(HSB);
      cmode = "rgb";
    }
  }
  
  // Iterates over the array of words and draws a square for each one. The fill colour 
  // is determined by an averaging of the pixel colours in the first 20 images returned 
  // in a Google image search of the word.
  for (int i = 0; i < words.length && i <= pow(width, 2); i++) {
    String word = words[i];
    TableRow r = chromadict.findRow(word, "words");
    if (r != null) {
      c = r.getInt(cmode);
    } else {
      c = genColor(word, cmode);
    }
    
    fill(c);
    if (isize >= 1.0) {
      rect(x, y, isize, isize);
    } else {
      rect(x, y, 1, 1);
    }
    
    if (x+isize > width) {
      x = isize/2;
      y += isize;
    } else {
      x += isize;
    }
  }
  
  String path;
  switch (save) {
    case 0:
      saveTable(chromadict, "data/chromadict.csv");
      PImage rgb = get(0, 0, dimension, dimension);
      path = dataPath("imgs/"+split(filename, ".")[0]+"."+str(width)+"x"+str(height)+cmode+".jpg");
      rgb.save(path);
      //if (move) {
      //  File source = new File(dataPath(filename));
      //  File dest = new File(dataPath(split(filename, ".")[0]+"/"+filename));
      //  source.renameTo(dest);
      //}
      save++;
      break;
    case 1:
      if (cmode == "hsb") {
        PImage hsb = get(0, 0, dimension, dimension);
        path = dataPath("imgs/"+split(filename, ".")[0]+"."+str(width)+"x"+str(height)+cmode+".jpg");
        hsb.save(path);
        save++;
        break;
      }
  }
}