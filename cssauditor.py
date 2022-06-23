import sys 
import argparse 
import os
import re
try:
 import lxml.html
except ImportError:
 print("Error: You need to install the lxml package first.")
 exit()


css_parse = argparse.ArgumentParser(prog='CSSAuditor', description="This application audits CSS code.")
css_parse.add_argument('--unused', nargs=2, help='Show unused CSS classes.')
css_parse.add_argument('--colors', help='Show repeated colors in CSS file(s).')
css_parse.add_argument('--styletags', help='Show files where style tags are used.')
css_parse.add_argument('--styleatts', help='Show where style attributes are used in HTML/PHP files.')
allargs = css_parse.parse_args()

argslist = [allargs.unused,allargs.colors,allargs.styletags,allargs.styleatts]
for arg in argslist:
 if arg and arg==allargs.unused:
  if os.path.exists(arg[0])==False:
   raise FileNotFoundError("CSS file/folder not found. If you're sure the file/folder exists, check the name and path you typed.")
  elif os.path.exists(arg[1])==False:
   raise FileNotFoundError("HTML/PHP file/folder not found. If you're sure the file/folder exists, check the name and path you typed.")
 elif arg and arg != allargs.unused:
  if os.path.exists(arg)==False:
   raise FileNotFoundError("File/folder not found. If you're sure the file/folder exists, check the name and path you typed.")


def css_list(csspath) -> list:
 csslist = []
 if os.path.isfile(csspath): 
  if os.path.splitext(csspath)[1] != '.css': 
   raise TypeError('Only css files are supported.')
  else:
   csslist.append(csspath)
 elif os.path.isdir(csspath):  
  cssdirlist = os.listdir(csspath)
  for i in cssdirlist:
   itempath = os.path.join(csspath, i) 
   if (os.path.isfile(itempath)) and (os.path.splitext(itempath)[1] == '.css'): 
    csslist.append(itempath)
  if any(csslist) == False:
   raise ValueError('No CSS files were found.')
   exit()
 return csslist

def html_list(htmlpath) -> list:
 htmllist = []
 if os.path.isfile(htmlpath):
  if os.path.splitext(htmlpath)[1] not in ['.html','.php']:
   raise TypeError('Only HTML and PHP files are supported.')
  else:
   htmllist.append(htmlpath)
 elif os.path.isdir(htmlpath):
  for dirpath,subdirs,files in os.walk(htmlpath):
   for file in files:
    if os.path.splitext(file)[1] in ['.html','.php']: 
     htmllist.append(os.path.join(dirpath,file))
  if any(htmllist) == False:
   raise ValueError('No HTML/PHP files were found.')
   exit()
 return htmllist

def css_classes(csslist) -> dict:
 classlist=[]
 classdict = dict()
 for csspath in csslist:
  with open(csspath,'r') as filer:
   filestr = filer.read()
  filestr = re.sub(r'/\*[\s\S]*?\*/','',filestr) 
  lineslist = filestr.splitlines() 
  for line in lineslist:
    if '{' in line:
     classlist += [x.lstrip('.') for x in re.findall(r"[\.][-_A-Za-z0-9]+",line)]
  classdict[csspath] = set(classlist)
  classlist.clear() 
 return classdict

def inner_loops(htmllist,classname):
 for htmlpath in htmllist:
  try:
   elemtree = lxml.html.parse(htmlpath)
   bstr = lxml.html.tostring(elemtree)
   htmlobj = lxml.html.fromstring(bstr)
  except TypeError:
   continue
  for element in htmlobj.iter():
   if 'class' in element.attrib and classname in element.classes:
    return True

def used_classes(csslist, htmllist) -> dict:
 classdict = css_classes(csslist)
 usedclasses = dict.fromkeys(classdict,set())
 for i in classdict:
  for j in classdict[i]:
   if inner_loops(htmllist,j):
    usedclasses[i].add(j)
 return usedclasses     

def unused_classes(csslist,htmllist) -> dict:
 classdict = css_classes(csslist)
 usedclasses = used_classes(csslist, htmllist)
 unusedclasses = dict.fromkeys(classdict)
 for classpath in classdict:
  unusedclasses[classpath] = classdict[classpath].difference(usedclasses[classpath])   
 return unusedclasses

def style_attributes(htmllist) -> dict:
 styledict = dict.fromkeys(htmllist,list())
 for htmlpath in htmllist:
  try:
   elemtree = lxml.html.parse(htmlpath)
   bstr = lxml.html.tostring(elemtree)
   htmlobj = lxml.html.fromstring(bstr)
  except TypeError:
   continue
  for element in htmlobj.iter():
   if 'style' in element.attrib:
    styledict[htmlpath].append(element.tag)
 return styledict

def style_tags(htmllist) -> list:
 stylelist = []
 for htmlpath in htmllist:
  try:
   elemtree = lxml.html.parse(htmlpath)
   bstr = lxml.html.tostring(elemtree)
   htmlobj = lxml.html.fromstring(bstr)
  except TypeError:
   continue
  for element in htmlobj.iter():
   if element.tag == 'style':
    stylelist.append(htmlpath)
    break
 return stylelist

def duplicate_colors(csslist) -> dict:
 colordict = dict.fromkeys(csslist,dict())
 filelist = []
 colorlist = []
 colorstrlist = ['black','silver','gray','grey','darkgray','darkgrey','darkslategray','darkslategrey','dimgray','dimgrey','lightgray','lightgrey','slategray','slategrey','white','maroon','red','purple','fuchsia','magenta','green','lime','olive','yellow','navy','blue','teal','aqua','orange','aliceblue','antiquewhite','aquamarine','azure','beige','bisque','blanchedalmond','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgreen','darkkhaki','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue','darkturquoise','darkviolet','deeppink','deepskyblue','dodgerblue','firebrick','floralwhite','forestgreen','gainsboro','ghostwhite','gold','goldenrod','greenyellow','honeydew','hotpink','indianred','indigo','ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgreen','lightpink','lightsalmon','lightseagreen','lightskyblue','lightslategray','lightslategrey','lightsteelblue','lightyellow','limegreen','linen','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite','oldlace','olivedrab','orangered','orchid','palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum','powderblue','rosybrown','royalblue','saddlebrown','salmon','sandybrown','seagreen','seashell','sienna','skyblue','slateblue','snow','springgreen','steelblue','tan','thistle','tomato','turquoise','violet','wheat','whitesmoke','yellowgreen','rebeccapurple']
 rehex = re.compile(r'#[A-Za-z0-9]{3,8}')
 rergba = re.compile(r'rgba?\([0-9%,\/\.\s]*\)')
 rehsla = re.compile(r'hsla?\([0-9%,\/\.\s]*\)')
 rehwb = re.compile(r'hwb\([0-9%\/\.\s]*\)')
 relab = re.compile(r'lab\([0-9%\/\.\s]*\)')
 relch = re.compile(r'lch\([0-9%\/\.\s]*\)')
 for csspath in csslist:
  with open(csspath,'r') as filer:
   bigfilestr = filer.read()
  bigfilestr = re.sub(r'/\*[\s\S]*?\*/','',bigfilestr) 
  lineslist = bigfilestr.splitlines()
  for line in lineslist:
   if ':' in line:
    filelist.append(line) 
  filestr = ''.join(filelist)
  hexlist = rehex.findall(filestr)
  rgbalist = rergba.findall(filestr)
  hslalist = rehsla.findall(filestr)
  hwblist = rehwb.findall(filestr)
  lablist = relab.findall(filestr)
  lchlist = relch.findall(filestr)
  colorfunlist = hexlist+rgbalist+hslalist+hwblist+lablist+lchlist
  colorfunset = set(colorfunlist)
  for color1 in colorfunset:   
   if (count1:=colorfunlist.count(color1))>1:
    colorlist.append((color1,count1))
  for color2 in colorstrlist:   
   if (count2:=filestr.lower().count(color2))>1:
    colorlist.append((color2,count2)) 
  colordict[csspath] = colorlist    
 return colordict


if allargs.unused:   
 csslist = css_list(allargs.unused[0])
 htmllist = html_list(allargs.unused[1])
 unusedclasses = unused_classes(csslist, htmllist)
 for path in unusedclasses:
  print(path+'\n', unusedclasses[path], '\n')
elif allargs.colors:   
 csslist = css_list(allargs.colors)
 colordict = duplicate_colors(csslist)
 for path in colordict:
  print(path+'\n',colordict[path],'\n')
elif allargs.styletags:  
 htmllist = html_list(allargs.styletags)
 styletags = style_tags(htmllist)
 print(styletags)
elif allargs.styleatts:  
 htmllist = html_list(allargs.styleatts)
 styleattribs = style_attributes(htmllist)
 for path in styleattribs:
  print(path+'\n', styleattribs[path])
