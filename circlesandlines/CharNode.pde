class CharNode {
  
  float x, y, baseX, baseY;
  float n;
  float size;  // diameter
  color f, s;  // fill and stroke colours
  String label;
  int chr;
  
  // I miss multiple assignment.
  boolean isNum = false;
  boolean isVowel = false;
  boolean isCons = false;
  //boolean oacc;
  boolean isSyn = false;
  boolean isSpec = false;
  
  CharNode(String character, float posx, float posy, float number, color c) {
    baseX = posx;
    baseY = posy;
    x = baseX;
    y = baseY;
    n = number;
    size = n/charCount*1000;
    f = c;
    label = character;
    chr = character.charAt(0);
    
    String ns = "0123456789";
    String cons = "bcdfghjklmnpqrstvwxyz";
    //String oabc = "šœžµßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ";
    String vs = "aeiou";
    String syn = "!&()-[]{};:'\",.?/<>#@+=_$%^*~`|\\";
    
    if (ns.indexOf(label) != -1) {
      isNum = true;
    } else if (cons.indexOf(label) != -1) {
      isCons = true;
    } else if (vs.indexOf(label) != -1) {
      isVowel = true;
    } else if (syn.indexOf(label) != -1) {
      isSyn = true;
    } else {
      isSpec = true;
    }
  }
  
  void move(float newx, float newy) {
    x = newx-width/2;
    y = newy-height/2;
  }
  
  //void zoom() {
  //  x = scale*baseX;
  //  y = scale*baseY;
  //  size = scale*baseSize;
  //}
  
  void reset() {
    x = baseX;
    y = baseY;
  }
  
  void display() {
    fill(f);
    stroke(s);
    strokeWeight(size/50);
    ellipse(x, y, size, size);
  }
    
  void label() {
    fill(s);
    textAlign(CENTER, BOTTOM);
    text(label, x, y);
    textAlign(CENTER, TOP);
    text(int(n), x, y);
  }
   
  void add() {
    size++;
  }
  
  void add(int amount) {
    size += amount;
  }
  
  boolean hover(float mX, float mY) {
    float lowx = x-size/2+width/2;
    float highx = x+size/2+width/2;
    float lowy = y-size/2+height/2;
    float highy = y+size/2+height/2;
    if (lowx <= mX && mX <= highx && lowy <= mY && mY <= highy) {
      return true;
    } else {
      return false;
    }
  }
}

void makeNodes(IntDict charFreqs) {
  String[] keys;
  
  // Create the character nodes. Also calculate total number of characters.
  for (int i=0; i < charFreqs.size(); i++) {
    keys = charFreqs.keyArray();
    float n = charFreqs.get(keys[i]);
    nodes.put(keys[i], new CharNode(keys[i], 0, 0, n, 0));
    println(keys[i], n, n/charCount, n/charCount*1000);
  }
  
  // Sort the nodes into different arrays based on character type.
  for (String Key: nodes.keySet()) {
    CharNode node = nodes.get(Key);
    if (node.isNum) {
      nums = (CharNode[])append(nums, node);
    } else if (node.isVowel) {
      vowels = (CharNode[])append(vowels, node);
    } else if (node.isCons) {
      cons = (CharNode[])append(cons, node);
    } else if (node.isSyn) {
      syns = (CharNode[])append(syns, node);
    } else {
      specs = (CharNode[])append(specs, node);
    }
  }
  
  // Set colour and position for nodes based on cluster.
  pushStyle();
  colorMode(HSB);
  float cvar, pvar;
  for (int i=0; i < nums.length; i++) {
    // Vary hue
    cvar = map(i, nums.length, 0, 0, 255); 
    nums[i].f = color(cvar, 30, 100);
    nums[i].s = color(cvar, 30, 70);
    pvar = map(i, nums.length, 0, 0, 2*PI);
    nums[i].baseX = 20*cos(pvar);
    nums[i].baseY = 20*sin(pvar);
    nums[i].x = nums[i].baseX;
    nums[i].y = nums[i].baseY;
  }
  for (int i=0; i < cons.length; i++) {
    // Vary hue
    cvar = map(i, 0, cons.length, 0, 255);
    cons[i].f = color(cvar, 90, 200);
    cons[i].s = color(cvar, 100, 130);
    pvar = map(i, 0, cons.length, 0, 2*PI);
    cons[i].baseX = 220*cos(pvar);
    cons[i].baseY = 220*sin(pvar);
    cons[i].x = cons[i].baseX;
    cons[i].y = cons[i].baseY;
  }
  for (int i=0; i < vowels.length; i++) {
    // Vary brightness
    cvar = map(i+1, 0, vowels.length+1, 0, 255);
    vowels[i].f = color(cvar);
    vowels[i].s = color(cvar/2);
    pvar = map(i, 0, vowels.length, 0, 2*PI);
    vowels[i].baseX = 100*cos(pvar);
    vowels[i].baseY = 100*sin(pvar);
    vowels[i].x = vowels[i].baseX;
    vowels[i].y = vowels[i].baseY;    
  }
  for (int i=0; i < syns.length; i++) {
    // Dark grey
    syns[i].f = color(70);
    syns[i].s = color(120);
    pvar = map(i, 0, syns.length, 0, 2*PI);
    syns[i].baseX = 320*cos(pvar);
    syns[i].baseY = 320*sin(pvar);
    syns[i].x = syns[i].baseX;
    syns[i].y = syns[i].baseY;
  }
  for (int i=0; i < specs.length; i++) {
    // Medium grey
    specs[i].f = color(120);
    specs[i].s = color(90);
    pvar = map(i, 0, specs.length, 0, 2*PI);
    specs[i].baseX = 340*cos(pvar);
    specs[i].baseY = 340*sin(pvar);
    specs[i].x = specs[i].baseX;
    specs[i].y = specs[i].baseY;
  }
  popStyle();
}

//void rotateCluster(CharNode[] cluster, int r) {
//  float angle;
//  for (int i=0; i < cluster.length; i++) {
//    angle = acos(cluster[i].x/r);
//    println(angle);
//    if (cos(angle+.005) <= -.99) {
//      angle -= .005;
//    } else {
//      angle += .005;
//    }
//    cluster[i].x = r*cos(angle);
//    cluster[i].y = r*sin(angle);
//    println(angle, cluster[i].x, cluster[i].y);
//  }
//}