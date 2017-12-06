// Some parts of code adapted from https://processing.org/examples/keyboardfunctions.html

// TO DO:
// * write to do list

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

Table chromadict;
Table ascii;

String[] words = new String[0];

float isize;
int dimension;
float x, y;

boolean newword;

color c, crgb, chsb;
String cmode = "rgb";

boolean save = false;


void setup() {
  size(750, 750);
  
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
  
  isize = width/sqrt(words.length);
  dimension = int(sqrt(words.length)*isize);
  
  noStroke();
  rectMode(CENTER);
}

void draw() {
  background(0);
  if(newword == true) {
    // Draw the "letter"
    int y_pos;
    if (letterHeight == maxHeight) {
      y_pos = y;
      rect( x, y_pos, letterWidth, letterHeight );
    } else {
      y_pos = y + minHeight;
      rect( x, y_pos, letterWidth, letterHeight );
      fill(numChars/2);
      rect( x, y_pos-minHeight, letterWidth, letterHeight );
    }
    newword = false;
  }
}

void keyPressed()
{
  // If the key is between 'A'(65) to 'Z' and 'a' to 'z'(122)
  if((key >= 'A' && key <= 'Z') || (key >= 'a' && key <= 'z')) {
    int keyIndex;
    if(key <= 'Z') {
      keyIndex = key-'A';
      letterHeight = maxHeight;
      fill(colors[key-'A']);
    } else {
      keyIndex = key-'a';
      letterHeight = minHeight;
      fill(colors[key-'a']);
    }
  } else {
    fill(0);
    letterHeight = 10;
  }

  newword = true;

  // Update the "letter" position
  x = ( x + letterWidth ); 

  // Wrap horizontally
  if (x > width - letterWidth) {
    x = 0;
    y+= maxHeight;
  }

  // Wrap vertically
  if( y > height - letterHeight) {
    y = 0;      // reset y to 0
  }
  println("Word count: " + words.length);
  println("Words per line: " + int(sqrt(words.length)));
  println("Word block size: (" + isize + " px)^2");
}