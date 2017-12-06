// Adapted from example at https://processing.org/reference/createReader_.html

String[] getWords(String filepath) {
  
  String[] words = new String[0];
  
  BufferedReader reader = createReader(filepath);
  String line;
  
  for (;true;) {    // this looks so weird but how else do I write an endless for loop
    try {
      line = reader.readLine();
    } catch (IOException e) {
      e.printStackTrace();
      line = null;
    }
    if (line == null) {
      break;
    } else {
      String[] wordsinline = splitTokens(line, " /\t");
      for (int i = 0; i < wordsinline.length; i++) {
        String[] word = checkWord(wordsinline[i]);
        words = concat(words, word);
      }
    }
  }
  return words;
}

String[] checkWord(String word) {
  String[] w1 = new String[0];
  if (word.indexOf("'") != -1) {
    String[] parts = splitTokens(word, "'");
    w1 = append(w1, join(parts, ""));
    return w1;
  } else if (word.indexOf("-") != -1) {
    String[] parts = splitTokens(word, "-");
    if (parts.length < 3) {
      w1 = append(w1, join(parts, ""));
    } else {
      w1 = concat(w1, parts);
    }
  } else {
    w1 = append(w1, word);
  }
  return w1;

}