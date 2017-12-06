
color genColor(String word, String mode) {
  int a=0, b=0, c=0;
  int len = word.length();
  color crgb, chsb;
  
  if (isNumber(word)) {
    crgb = int(word);
    chsb = int(word);
  } else {
    for (int i=0; i < len; i += 3) {
        TableRow r = ascii.findRow(str(word.charAt(i)), "symbol");
      if (r == null) {
        println("Error finding '" + str(word.charAt(i)) + "'");
        break;
      }
      a += r.getInt("dec");
      if (i+1 < len) {
        r = ascii.findRow(str(word.charAt(i+1)), "symbol");
        if (r == null) {
          println("Error finding '" + str(word.charAt(i)) + "'");
          break;
        }
        b += r.getInt("dec");
      }
      if (i+2 < len) {
        r = ascii.findRow(str(word.charAt(i+2)), "symbol");
        if (r == null) {
          println("Error finding '" + str(word.charAt(i)) + "'");
          break;
        }
        c += r.getInt("dec");
      }
    }
    
    if (len > 3) {
      int div = len/3;
      c /= div;
      switch (len%3) {
        case 0:
          a /= div;
          b /= div;
          break;
        case 1:
          a /= div+1;
          b /= div;
          break;
        case 2:
          a /= div+1;
          b /= div+1;
          break;
      }
    }
    
    println("premapping: ",a,b,c);
    a = int(map(a, 45, 122, 0, 255));
    b = int(map(b, 45, 122, 0, 255));
    c = int(map(c, 45, 122, 0, 255));
    println("postmapping: ",a, b, c);
  
    pushStyle();
    colorMode(RGB);
    crgb = color(a,b,c);
    colorMode(HSB);
    chsb = color(a,b,c);
    popStyle();
  }
  
  TableRow newEntry = chromadict.addRow();
  newEntry.setString("words", word);
  newEntry.setInt("rgb", crgb);
  newEntry.setInt("hsb", chsb);
  
  if (mode == "rgb") {
    return crgb;
  } else {
    return chsb;
  }
}

boolean isNumber(String seq) {
  for (int i=0; i < seq.length(); i++) {
    if (!(seq.charAt(0) >= 48 && seq.charAt(0) <= 57)) {
      return false;
    }
  }
  return true;
}