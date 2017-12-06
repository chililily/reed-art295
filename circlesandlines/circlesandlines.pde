import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;

//String filepath;
//String filename;
String filename = "blackjack.go";
String[] words;

IntDict charFreqs = new IntDict();
IntDict cxns = new IntDict();

//So...so gross. Find a way to clean this up when you have time.
HashMap <String, CharNode> nodes = new HashMap <String, CharNode> ();
CharNode[] nums = new CharNode[0];
CharNode[] vowels = new CharNode[0];
CharNode[] cons = new CharNode[0];
CharNode[] syns = new CharNode[0];
CharNode[] specs = new CharNode[0];
Cxn[] lines = new Cxn[0];

float charCount;
float numCxns;

//Table c3;    // character-colour codes. yay alliteration!
Table ascii;

// Transformation variables
float angle;
float scale = 1.0;
float xdisplace = 0.0;
float ydisplace = 0.0;

// State variables
//boolean move;
boolean reset = false;
boolean showLabels;
//boolean dialogOpen = true;

void setup() {
  //c3 = loadTable(dataPath("c3.csv"), "header");
  ascii = loadTable(dataPath("ascii.csv"), "header");
  
  // Reads the data from the input file.
  //selectInput("Select a file to process:", "processFile");
  
  File f = new File(dataPath(filename));
  if (f.exists()) {
   words = getWords(dataPath(filename));
   //if (!(filename == "ascii.csv" || filename == "chromadict.csv")) {
   //  move = true;
   //}
  } else {
   words = getWords(dataPath(split(filename, ".")[0]+"/"+filename));
  }
  
   // Get the count for each character represented in the text data.
   for (int i=0; i < words.length; i++) {
     charCount += countChars(words[i]);
   }
    
   // Make ALL the objects.
   makeNodes(charFreqs);
   makeCxns(cxns);

  size(750,750);
}

void draw() {
  background(25);
  
  //if (!dialogOpen) {
    pushMatrix();
  
    // Transformations
    translate(width/2+xdisplace, height/2+ydisplace);
    scale(scale);
    if (key == 'r') {
      rotate(angle);
      angle += .005;
    }
    
    // Draw connecting lines.
    for (int i=0; i < lines.length; i++) {
      lines[i].connect();
    }
    
    // Draw nodes.
    for (String Key: nodes.keySet()) {
      CharNode n = nodes.get(Key);
      n.display();
      // Display label.
      if (showLabels || n.hover(mouseX, mouseY)) {
        n.label();
      }
      // Move node.
      if (mousePressed && n.hover(pmouseX, pmouseY)) {
        n.move(mouseX, mouseY);
      }
      // Reset node.
      if (keyPressed && key == ' ') {
        n.reset();
        reset = true;
      }
    }
    popMatrix();
    
    // Display character and word counts in bottom right corner.
    pushStyle();
    fill(160);
    textAlign(RIGHT,BOTTOM);
    textSize(10);
    text(words.length,width-5,height-20);
    text(int(charCount),width-5,height-5);
    popStyle();
    
    if (keyPressed) {
      
      // Save image.
      if (key == 's') {
        save(dataPath("imgs/"+split(filename, ".")[0]+".jpg"));
        
      // Show all labels.
      } else if (key == 'l') {
        if (showLabels) {
          showLabels = false;
        } else {
          showLabels = true;
        }
        
      // Zoom.
      } else if (key == '.') {
        scale += 0.1;
      } else if (key == ',' && scale > 0) {
        scale -= 0.1;
        
      // Pan.
      } else if (keyCode == UP) {
        ydisplace += 10;
      } else if (keyCode == DOWN) {
        ydisplace -= 10;
      } else if (keyCode == LEFT) {
        xdisplace += 10;
      } else if (keyCode == RIGHT) {
        xdisplace -= 10;
      }
    }
  
  
    if (reset) {
      scale = 1.0;
      xdisplace = 0.0;
      ydisplace = 0.0;
      reset = false;
    }
    
    // Doesn't work for some reason, even though it was c+p'd from another program where 
    // it worked fine.
    //if (move) {
    //  File source = new File(dataPath(filename));
    //  File dest = new File(dataPath(split(filename, ".")[0]+"/"+filename));
    //  source.renameTo(dest);
    //  move = false;
    //}
  //} else {
  //  text("Selecting file...", width/2, height/2);
  //}
}

//void processFile(File selection) {
//  if (selection == null) {
//    println("Window was closed or user hit cancel.");
//  } else {
//    filepath = selection.getAbsolutePath();
//    String[] elems = split(filepath, "/");
//    filename = elems[elems.length-1];
    
//    getWords(filepath);
    
//    dialogOpen = false;
//  }
//}

// <<NOTES/TO-DO>>
// * build+save c3. currently the colours are set through FIVE DIFFERENT for loops.
//   the horror. (at least they're not five *nested* loops I guess. that would be 
//   exponentially worse...hah)
// * select input
// * move files