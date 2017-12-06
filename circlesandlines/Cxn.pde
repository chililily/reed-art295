class Cxn {
  
  CharNode from, to;
  String chara, charb;
  float n;
  float weight;
  color c;
  
  Cxn(CharNode anode, CharNode bnode, float freq) {
    from = anode;
    to = bnode;
    chara = from.label;
    charb = to.label;
    n = freq;
    weight = (freq/from.n)*255;
    c = lerpColor(from.s, to.s, 0.5);
    println(from.label, to.label, freq, from.n, weight);
  }
  
  void connect() {
    stroke(c, weight);
    strokeWeight(2);
    line(from.x, from.y, to.x, to.y);
  }
}

void makeCxns(IntDict cxns) {
  String[] keys = cxns.keyArray();
  for (int i=0; i < cxns.size(); i++) {
    String[] s = split(keys[i], "-");
    if (nodes.get(s[0]) != null && nodes.get(s[1]) != null) {
      lines = (Cxn[])append(lines, new Cxn(nodes.get(s[0]), nodes.get(s[1]), cxns.get(keys[i])));
      numCxns += cxns.get(keys[i]);
    }
  }
}