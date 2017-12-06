int countChars(String word) {
  int n = 0;
  word = word.toLowerCase();
  for (int i=0; i < word.length(); i++) {
    char c = word.charAt(i);
    charFreqs.add(str(c), 1);
    n++;
    
    if (i < word.length()-1 && isAlphabet(word.charAt(i+1))) {
      cxns.add(str(c)+"-"+str(word.charAt(i+1)), 1);
    }
  }
  return n;
}

boolean isAlphabet(char c) {
  String abc = "abcdefghijklmnopqrstuvwxyz";
  if (abc.indexOf(str(c)) != -1) {
    return true;
  } else {
    return false;
  }
}