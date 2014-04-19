#!/usr/bin/env python
# -*- coding: utf-8 -*-

# utilities for generating HTML indices
# (c) 2003-2006, 2009-2013 by the GRASS Development Team, Markus Neteler, Glynn Clements, Luca Delucchi

import sys
import os
import string
from datetime import datetime

## TODO: better fix this in include/Make/Html.make, see bug RT #5361

# exclude following list of modules from help index:

exclude_mods = [
    "i.find",
    "r.watershed.ram",
    "r.watershed.seg",
    "v.topo.check",
    "helptext.html"]

# these modules don't use G_parser()

desc_override = {
    "g.parser": "Provides automated parser, GUI, and help support for GRASS scipts.",
    "r.li.daemon": "Support module for r.li landscape index calculations."
    }

############################################################################

header1_tmpl = string.Template(\
r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
 <title>${title}</title>
 <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
 <meta name="Author" content="GRASS Development Team">
""")

macosx_tmpl = string.Template(\
r"""
 <meta name="AppleTitle" content="GRASS GIS ${grass_version} Help">
 <meta name="AppleIcon" content="GRASS-${grass_mmver}/grass_icon.png">
 <meta name="robots" content="anchors">
""")

header2_tmpl = string.Template(\
r""" <link rel="stylesheet" href="grassdocs.css" type="text/css">
</head>
<body style="width: 99%">

<!-- this file is generated by man/build_html.py -->

<img src="grass_logo.png" alt="GRASS logo"><hr align=center size=6 noshade>

<h2>GRASS GIS ${grass_version} Reference Manual</h2>

<p><b>Geographic Resources Analysis Support System</b>, commonly
referred to as <a href="http://grass.osgeo.org">GRASS</a>, is a <a
href="http://en.wikipedia.org/wiki/Geographic_information_system">Geographic
Information System</a> (GIS) used for geospatial data management and
analysis, image processing, graphics/maps production, spatial
modeling, and visualization. GRASS is currently used in academic and
commercial settings around the world, as well as by many governmental
agencies and environmental consulting companies.</p>

<p>This reference manual details the use of modules distributed with
Geographic Resources Analysis Support System (GRASS), an open source
(<a href="http://www.gnu.org/licenses/gpl.html">GNU GPLed</a>), image
processing and geographic information system (GIS).</p>

""")
#"

overview_tmpl = string.Template(\
r"""<!-- the files grass7.html & helptext.html file live in lib/init/ -->

<table align="center" border="0" cellspacing="8">
  <tbody>
    <tr>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Quick Introduction</h3>
      <ul>
       <li><a href="helptext.html">How to start with GRASS</a></li>
       <li><a href="topics.html">Index of topics</a></li>
      </ul>
     <p>
      <ul>
       <li><a href="projectionintro.html">Intro: projections and spatial transformations</a></li>
       <li><a href="rasterintro.html">Intro: 2D raster map processing</a></li>
       <li><a href="raster3dintro.html">Intro: 3D raster map (voxel) processing</a></li>
       <li><a href="imageryintro.html">Intro: image processing</a></li>
       <li><a href="vectorintro.html">Intro: vector map processing and network analysis</a></li>
       <li><a href="databaseintro.html">Intro: database management</a></li>
       <li><a href="temporalintro.html">Intro: temporal data processing</a></li>
      </ul></td>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Display/Graphical User Interfaces</h3>
       <ul>
        <li><a href="wxGUI.html">wxGUI</a> wxPython-based GUI frontend</li>
        <li><a href="wxGUI.components.html">wxGUI components</a></li>
       </ul>

       <ul>
        <li><a href="topic_gui.html">GUI commands</li>
       </ul>

       <ul>
        <li><a href="display.html">Display commands manual</a></li>
        <li><a href="displaydrivers.html">Display drivers</a></li>
       </ul>
      </td>
    </tr>
    <tr>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Raster and 3D raster processing</h3>
       <ul>
        <li><a href="raster.html">Raster commands manual</a></li>
        <li><a href="raster3D.html">3D raster (voxel) commands manual</a></li>
      </ul></td>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Image processing</h3>
       <ul>
        <li><a href="imagery.html">Imagery commands manual</a></li>
      </ul></td>
    </tr>
    <tr>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Vector processing</h3>
       <ul>
        <li><a href="vector.html">Vector commands manual</a></li>
        <li><a href="vectorascii.html">GRASS ASCII vector format specification</a></li>
      </ul></td>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Database</h3>
       <ul>
       <li><a href="sql.html">SQL support in GRASS GIS</a></li>
       <li><a href="database.html">Database commands manual</a></li>
       </ul></td>
    </tr>
    <tr>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;General</h3>
      <ul>
      <li><a href="grass7.html">GRASS GIS startup manual page</a></li>
      <li><a href="general.html">General commands manual</a></li>
      </ul></td>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Miscellaneous&nbsp;&amp;&nbsp;Variables</h3>
       <ul>
        <li><a href="misc.html">Miscellaneous commands manual</a></li>
        <li><a href="variables.html">GRASS variables and environment variables</a></li>
       </ul></td>
    </tr>
    <tr>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Temporal processing</h3>
       <ul>
        <li><a href="temporal.html">Temporal commands manual</a></li>
       </ul></td>
      <td valign="top" bgcolor="${box_color}" class="box"><h3>&nbsp;Printing</h3>
       <ul>
        <li><a href="postscript.html">Postscript commands manual</a></li>
       </ul></td>
    </tr>
  </tbody>
</table>
""")
#"

footer_tmpl = string.Template(\
r"""<hr>
<p><a href="${index_url}">Help Index</a> | <a href="topics.html">Topics Index</a> | <a href="keywords.html">Keywords Index</a> | <a href="full_index.html">Full Index</a></p>
<p>&copy; 2003-${year} <a href="http://grass.osgeo.org">GRASS Development Team</a>, GRASS GIS ${grass_version} Reference Manual</p>
</body>
</html>
""")
#"

cmd1_tmpl = string.Template(\
r"""<b><a href="#${cmd}">${cmd}.*</a></b>""")
#"

cmd2_tmpl = string.Template(\
r"""<a name="${cmd}"></a>
<h3>${cmd}.* commands:</h3>
<table>
""")
#"

desc1_tmpl = string.Template(\
r"""<tr><td valign="top"><a href="${cmd}">${basename}</a></td> <td>${desc}</td></tr>
""")
#"

sections = \
r""" ]
<table border=0>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#d">d.*</a> </td><td>display commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#db">db.*</a> </td><td>database commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#g">g.*</a> </td><td>general commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#i">i.*</a> </td><td>imagery commands</td></tr>

<tr><td>&nbsp;&nbsp;<a href="full_index.html#m">m.*</a> </td><td>miscellaneous commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#ps">ps.*</a> </td><td>postscript commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#r">r.*</a> </td><td>raster commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#r3">r3.*</a> </td><td>raster3D commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#t">t.*</a> </td><td>temporal commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="full_index.html#v">v.*</a> </td><td>vector commands</td></tr>
<tr><td>&nbsp;&nbsp;<a href="wxGUI.Nviz.html">nviz</a> </td><td>visualization suite</td></tr>
<tr><td>&nbsp;&nbsp;<a href="wxGUI.html">wxGUI</a> </td><td>wxPython-based GUI frontend</td></tr>
</table>
"""
#"

modclass_intro_tmpl = string.Template(\
r"""Go to <a href="${modclass_lower}intro.html">${modclass} introduction</a> | <a href="topics.html">topics</a> <p>
""")
#"

modclass_tmpl = string.Template(\
r"""Go <a href="index.html">back to help overview</a>
<h3>${modclass} commands:</h3>
<table>
""")
#"

desc2_tmpl = string.Template(\
r"""<tr><td valign="top"><a href="${cmd}">${basename}</a></td> <td>${desc}</td></tr>
""")
#"


full_index_header = \
r"""Go <a href="index.html">back to help overview</a>
<h3>Full command index:</h3>
[ 
"""
#"


message_tmpl = string.Template(\
r"""Generated HTML docs in ${html_dir}/index.html
----------------------------------------------------------------------
Following modules are missing the 'modulename.html' file in src code:
""")
#"

moduletopics_tmpl = string.Template(\
r"""
<li> <a href="topic_${key}.html">${name}</a></li>
"""
)
#"

headertopics_tmpl = \
r"""
<link rel="stylesheet" href="grassdocs.css" type="text/css">
</head>
<body style="width: 99%">

<img src="grass_logo.png" alt="GRASS logo"><hr align=center size=6 noshade> 
<h2>Topics</h2>
<ul>
"""
#"

headerkeywords_tmpl = \
r"""
<link rel="stylesheet" href="grassdocs.css" type="text/css">
</head>
<body style="width: 99%">

<img src="grass_logo.png" alt="GRASS logo"><hr align=center size=6 noshade> 
<h2>Keywords - Index of GRASS GIS modules</h2>
"""
#"

headerkey_tmpl = string.Template(\
r"""
<link rel="stylesheet" href="grassdocs.css" type="text/css">
</head>
<body bgcolor="white">

<img src="grass_logo.png" alt="GRASS logo"><hr align=center size=6 noshade> 

<h2>Topic: ${keyword}</h2>
<table>
""")
#"

############################################################################

def check_for_desc_override(basename):
    return desc_override.get(basename)

def read_file(name):
    f = open(name, 'rb')
    s = f.read()
    f.close()
    return s

def write_file(name, contents):
    f = open(name, 'wb')
    f.write(contents)
    f.close()

def try_mkdir(path):
    try:
        os.mkdir(path)
    except OSError, e:
        pass

def replace_file(name):
    temp = name + ".tmp"
    if os.path.exists(name) and os.path.exists(temp) and read_file(name) == read_file(temp):
        os.remove(temp)
    else:
        try:
            os.remove(name)
        except OSError, e:
            pass
        os.rename(temp, name)

def copy_file(src, dst):
    write_file(dst, read_file(src))

def html_files(cls = None):
    for cmd in sorted(os.listdir(html_dir)):
        if cmd.endswith(".html") and \
           (cls in [None, '*'] or cmd.startswith(cls + ".")) and \
           (cls != '*' or len(cmd.split('.')) >= 3) and \
           cmd not in ["full_index.html", "index.html"] and \
           cmd not in exclude_mods and \
           not cmd.startswith("wxGUI."):
            yield cmd

def write_html_header(f, title, ismain = False):
    f.write(header1_tmpl.substitute(title = title))
    if ismain and macosx:
        f.write(macosx_tmpl.substitute(grass_version = grass_version,
                                       grass_mmver = grass_mmver))
    f.write(header2_tmpl.substitute(grass_version = grass_version))

def write_html_cmd_overview(f):
    box_color = "#e1ecd0"
    f.write(overview_tmpl.substitute(box_color = box_color))

def write_html_footer(f, index_url, year = None):
    if year is None:
        cur_year = default_year
    else:
        cur_year = year
    f.write(footer_tmpl.substitute(grass_version = grass_version,
                                   index_url = index_url, year = cur_year))

def get_desc(cmd):
    f = open(cmd, 'r')
    while True:
        line = f.readline()
        if not line:
            return ""
        if "NAME" in line:
            break

    while True:
        line = f.readline()
        if not line:
            return ""
        if "SYNOPSIS" in line:
            break
        if "<em>" in line:
            sp = line.split('-',1)
            if len(sp) > 1:
                return sp[1].strip()
            else:
                return None

    return ""

############################################################################

arch_dist_dir = os.environ['ARCH_DISTDIR']
html_dir = os.path.join(arch_dist_dir, "docs", "html")
gisbase = os.environ['GISBASE']
grass_version = os.getenv("VERSION_NUMBER", "unknown")
grass_mmver = '.'.join(grass_version.split('.')[0:2])
macosx = "darwin" in os.environ['ARCH'].lower()
default_year = os.getenv("VERSION_DATE")
if not default_year:
    default_year = str(datetime.now().year)

############################################################################
