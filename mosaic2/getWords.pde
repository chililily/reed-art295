// Adapted from example at https://processing.org/reference/createReader_.html

String[] getWords(String filename) {
  
  String[] words = new String[0];
  
  BufferedReader reader = createReader(filename);
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
      String[] wordsinline = splitTokens(line, " \"\t<>[]{}()~!@#$%^&*,./?;:_+=|\\");
      for (int i = 0; i < wordsinline.length; i++) {
        String word = check(wordsinline[i]);
        words = append(words, word);
      }
    }
  }
  
  return words;
}

String check(String word) {
  if (word.indexOf("'") != -1) {
    String[] parts = splitTokens(word, "'");
    word = join(parts, "");
  } else if (word.indexOf("-") != -1) {
    String[] parts = splitTokens(word, "-");
    word = join(parts, "");
  }
  return word;
}