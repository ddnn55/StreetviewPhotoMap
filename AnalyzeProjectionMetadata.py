#!/usr/bin/env python

import os
import sys
import json
import pprint


jsondir = 'data/panojson'
tiledir = 'data/panotile'
panojsons = os.listdir(jsondir)
html_tile_row = ''
html_yaw_row = ''
html_map_row = ''
for jsonfilename in panojsons:
   jsonfile = open(jsondir + '/' + jsonfilename, 'r')
   pano = json.loads(jsonfile.read())
   jsonfile.close()

   panoid    = pano[u'Location'][u'panoId']
   yaw       = pano[u'Projection'][u'pano_yaw_deg']
   latitude  = pano[u'Location'][u'lat']
   longitude = pano[u'Location'][u'lng']
   ll = str(latitude) + ',' + str(longitude)

   first_tile_filename = panoid + '_0_0.jpeg'
   yaw_html = yaw + '<div style="display:block; width:80px; height:80px;"><div style="display:block;width:80px; height:3px; background-color:black; border:2px solid white; -webkit-transform: rotate('+str(float(yaw)+90)+'deg);"></div></div>'
   map_html = '<a href="http://maps.google.com/maps?q='+ll+'">Full Map</a><br/><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/maps?f=q&amp;source=s_q&amp;hl=en&amp;geocode=&amp;q=40.759351,-73.885095&amp;aq=&amp;sll=33.775566,-84.375391&amp;sspn=0.012646,0.019183&amp;vpsrc=0&amp;ie=UTF8&amp;t=m&amp;z=16&amp;ll=' + ll + '&amp;output=embed"></iframe>'

   html_tile_row = html_tile_row + '<td><img src="../panotile/'+first_tile_filename+'" width="512" height="512" /></td>'
   html_yaw_row  = html_yaw_row + '<td>' + yaw_html + '</td>'
   html_map_row  = html_map_row + '<td>' + map_html + '</td>'
   

html = '<table><tr>' + html_tile_row + '</tr>' + '<tr>' + html_yaw_row  + '</tr>' + '<tr>' + html_map_row  + '</tr></table>'

htmlfile = open('data/analysis/index.html', 'w')
htmlfile.write(html)
htmlfile.close()
