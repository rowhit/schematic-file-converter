#!/usr/bin/env python
# json-ulp.py - generate json.ulp, Eagle CAD program to export circuits to JSON
# Alex Ray (2011) <ajray@ncsu.edu>

# TODO(ajray): use pluralization instead of rewriting ('libraries','library')
#             figure out what's up with clearance[number]
# TODO do comma's properly

f = open('json.ulp','w')
header = """
// json.ulp - Export an Eagle Board, Schematic or Library into JSON
// Generated by json-ulp.py
// Alex Ray (2011) <ajray@ncsu.edu>
"""
misc = """
string esc(string s) { // JSON string escapes. tested
    string out = "";
    for (int i = 0; s[i]; ++i) {
        switch(s[i]) {
            case '"': out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '/': out += "\\/"; break;
            case '\b': out += "\\b"; break;
            case '\f': out += "\\f"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default: out += s[i];
        }
    }
    return out;
}
string beg(string a) { // pair with the start of an object
    string s;
    sprintf(s,"\"%s\": ",esc(a));
    return s;
}
string pl(string a) { // pair with the start of a list
    string s;
    sprintf(s,"\"%s\": [\n",esc(a));
    return s;
}
string ps(string a, string b) { // pair with string
    string s;
    sprintf(s,"\"%s\":\"%s\"",esc(a),esc(b));
    return s;
}
string pi(string a, int b) { // pair with int
    string s;
    sprintf(s,"\"%s\":%d",esc(a),b);
    return s;
}
string pr(string a, real b) { // pair with real
    string s;
    sprintf(s,"\"%s\":%g",esc(a),b);
    return s;
}
"""

def makepick(l):
  """ Make a pick function from a list """
  name = l[0]
  s = "string pick%s(int i) { // pick %s_...\n\tswitch(i) {\n" % (name, name)
  for term in l[1:]:
    s += '\t\tcase %s_%s: return "%s_%s";\n' % (name,term,name,term)
  s += '\t\tdefault: return "%s_unknown";\n\t}\n}\n' % name
  return s
# Goes with makepick()
picks = [
  ["CAP","FLAT","ROUND"],
  ["GRID_UNIT","MIL","MM","MIL","INCH"],
  ["ATTRIBUTE_DISPLAY_FLAG","OFF","VALUE","NAME"]]

def makeprint(l):
  """ Make a print function from a list """
  name = l[0]
  s = "string print%s(UL_%s %s) { // print %s_...\n\tswitch(i) {\n" % (name, name)
  for term in l[1:]:
    s += '\t\tcase %s_%s: return "%s_%s";\n' % (name,term,name,term)
  s += '\t\tdefault: return "%s_unknown";\n\t}\n}\n' % name
  # TODO secondary function
  s += "string pprint%s"
  return s
# Goes with makeprint()
prints = [
  ["arc",
    pr("angle1"),
    pr("angle2"),
    pi("cap"),
    pi("layer"),
    pi("radius"),
    pi("width"),
    pi("x1"), pi("y1"),
    pi("x2"), pi("y2"),
    pi("xc"), pi("yc")],
  ["area",
    pi("x1"), pi("y1"),
    pi("x2"), pi("y2")],
  ["attribute",
    pi("constant"),
    ps("defaultvalue"),
    pi("display"),
    ps("name"),
    po("text"),
    ps("value")],
  ["board",
    po("area"),
    po("grid"),
    ps("name"),
    pl("attributes","attribute"),
    pl("circles","circle"),
    pl("classes","class"),
    pl("elements","element"),
    pl("frames","frame"),
    pl("holes","hole"),
    pl("layers","layer"),
    pl("libraries","library"),
    pl("polygons","polygon"),
    pl("rectangles","rectangle"),
    pl("signals","signal"),
    pl("texts","text"),
    pl("wires","wire")],
  ["bus",
    ps("name"),
    pl("segments","segment")],
  ["circle",
    pi("layer"),
    pi("radius"),
    pi("width"),
    pi("x"), pi("y")],
  ["class",
    pi("clearance"), # TODO figure this out
    pi("drill"),
    ps("name"),
    pi("number"),
    pi("width")],
  ["contact",
    ps("string"),
    po("pad"),
    ps("signal"),
    po("smd"),
    pi("x"), pi("y")],
  ["contactref",
    po("contact"),
    po("element")],
  ["device",
    po("area"),
    ps("description"),
    ps("headline"),
    ps("library"),
    ps("name"),
    po("package"),
    ps("prefix"),
    ps("technologies"),
    ps("value"),
    pl("attributes","attribute"),
    pl("gates","gate")],
  ["deviceset",
    po("area"),
    ps("description"),
    ps("headline"),
    ps("library"),
    ps("name"),
    ps("prefix"),
    ps("value"),
    pl("devices","device"),
    pl("gates","gate")],
  ["element",
    pr("angle"),
    ps("attribute"), # TODO figure this out
    ps("column"),
    pi("locked"),
    pi("mirror"),
    ps("name"),
    po("package"),
    ps("row"),
    pi("smashed"),
    pi("spin"),
    ps("value"),
    pi("x"), pi("y"),
    pl("attributes","attribute"),
    pl("texts","text")],
  ["frame",
    pi("columns"),
    pi("rows"),
    pi("border"),
    pi("layer"),
    pi("x1"), pi("y1"),
    pi("x2"), pi("y2"),
    pl("texts","text"),
    pl("wires","wire")],
  ["gate",
    pi("addlevel"),
    ps("name"),
    pi("swaplevel"),
    pi("addlevel"),
    po("symbol"),
    pi("x"), pi("y")],
  ["grid",
    pr("distace"),
    pi("dots"),
    pi("multiple"),
    pi("on"),
    ps("unit"),
    ps("unitdist")],
  ["hole",
    pi("diameter"), # TODO: woogity here
    pi("drill"),
    pi("drillsymbol"),
    pi("x"), pi("y")],
  ["instance",
    pr("angle"),
    ps("column"),
    po("gate"),
    pi("mirror"),
    ps("name"),
    ps("row"),
    ps("sheet"),
    ps("smashed"),
    ps("value"),
    pi("x"), pi("y"),
    pl("attributes","attribute"),
    pl("texts","text"),
    pl("xrefs","gate")], #TODO: yeah these dont match
  ["junction",
      pi("diameter"),
    pi("x"), pi("y")],
  ["label",
      pr("angle"),
      pi("layer"),
      pi("mirror"),
      pi("spin"),
      po("text"),
      pi("x"), pi("y"),
      pi("xref"),
      pl("wires","wire")],
  ["layer",
      pi("color"),
      pi("fill"),
      ps("name"),
      pi("number"),
      pi("used"),
      pi("visible")],
  ["library",
      ps("description"),
      po("grid"),
      ps("headline"),
      ps("name"),
      pl("devices","device"),
      pl("devicesets","deviceset"),
      pl("layers","layers"),
      pl("packages","package"),
      pl("symbols","symbol")],
  ["net",
      po("class"),
      ps("column"),
      ps("name"),
      ps("row"),
      pl("pinrefs","pinref"),
      pl("segments","segment")],
  ["package",
      po("area"),
      ps("description"),
      ps("headline"),
      ps("library"),
      ps("name"),
      pl("cicles","circle"),
      pl("contacts","contact"),
      pl("frames","frame"),
      pl("holes","hole"),
      pl("polygons","polygon"),
      pl("rectangles","rectangle"),
      pl("texts","text"),
      pl("wires","wire")],
  ["pad",
      pr("angle"),
      pi("diameter"), # TODO This weird shit
      pi("drill"),
      pi("drillsymbol"),
      pi("elongation"),
      pi("flags"),
      ps("name"),
      pi("shape"), #TODO the fuck is this
      ps("signal"),
      pi("x"), pi("y")],
  ["part",
      ps("attribute"), # TODO this
      po("device"),
      po("deviceset"),
      ps("name"),
      ps("value"),
      pl("attributes","attribute"),
      pl("instances","instance")],
  ["pin",
      pr("angle"),
      po("contact"),
      pr("direction"),
      pr("function"),
      pr("length"),
      pr("name"),
      pr("net"),
      pr("swaplevel"),
      pr("visible"),
      pi("x"), pi("y"),
      pl("circles","circles"),
      pl("texts","texts"),
      pl("instances","instance")],
  ["pinref",
      po("instance"),
      po("part"),
      po("pin")],
  ["polygon",
      pi("isolate"),
      pi("layer"),
      pi("orphans"),
      pi("pour"),
      pi("rank"),
      pi("spacing"),
      pi("thermals"),
      pi("width"),
      pl("contours","wire"), #TODO these dont match
      pl("fillings","wire"), #TODO these dont match
      pl("wires","wire")], #TODO these dont match
  ["rectangle",
      pr("angle"),
      pi("layer"),
      pi("x1"), pi("y1"),
      pi("x2"), pi("y2")],
  ["schematic",
      po("grid"),
      ps("name"),
      ps("xreflabel"),
      pl("attributes","attribute"),
      pl("classes","class"),
      pl("layers","layer"),
      pl("libraries","library"),
      pl("nets","net"),
      pl("parts","part"),
      pl("sheets","sheet")],
  ["segment",
      pl("junctions","junction"),
      pl("labels","label"),
      pl("pinrefs","pinref"),
      pl("texts","text"),
      pl("wires","wire")],
  ["sheet",
      po("area"),
      pi("number"),
      pl("busses","bus"),
      pl("circles","circle"),
      pl("frames","frame"),
      pl("nets","net"),
      pl("parts","part"),
      pl("polygons","polygon"),
      pl("rectangles","rectangle"),
      pl("texts","text"),
      pl("wires","wire")],
  ["signal",
      pi("airwireshidden"),
      po("class"),
      ps("name"),
      pl("contactrefs","contactref"),
      pl("polygons","polygon"),
      pl("vias","via"),
      pl("wires","wire")],
  ["smd",
      pr("angle"),
      pi("dx"), pi("dy"), #TODO these are weird
      pi("flags"),
      pi("layer"),
      ps("name"),
      pi("roundness"),
      ps("signal"),
      pi("x"), pi("y")],
  ["symbol",
      po("area"),
      ps("library"),
      ps("name"),
      pl("circles","circle"),
      pl("frames","frame"),
      pl("rectangles","rectangle"),
      pl("pins","pin"),
      pl("polygons","polygon"),
      pl("texts","text"),
      pl("wires","wire")],
  ["text",
    pr("angle"),
    pi("font"),
    pi("layer"),
    pi("mirror"),
    pi("ratio"),
    pi("size"),
    pi("spin"),
    ps("value"),
    pi("x"), pi("y")],
  ["via",
      pi("diameter"), #TODO WTF is this
      pi("drill"),
      pi("drillsymbol"),
      pi("end"),
      pi("flags"),
      pi("shape"), # TODO wtf is this
      pi("start"),
      pi("x"), pi("y")],
  ["wire",
      po("arc"),
      pi("cap"),
      pr("curve"),
      pi("layer"),
      pi("style"),
      pi("width"),
      pi("x1"), pi("y1"),
      pi("x2"), pi("y2"),
      pl("pieces","wire")] #TODO one of these is not like the other
  ]

for pick in picks: print makepick(pick)
