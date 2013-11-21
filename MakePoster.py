#!/usr/bin/env python

from PIL import Image
import os
import sys
import json
import pprint
   
tile_size = 512

name = sys.argv[1]
time = sys.argv[2]

crop_factor = float(sys.argv[3])

jsondir = 'data/panojson'
tiledir = 'data/panotile'
panojsons = os.listdir(jsondir)
html_tile_row = ''
html_yaw_row = ''
html_map_row = ''

max_row = 0
max_col = 0

i = 0
real_total = 0
jsons_count = len(panojsons)
for jsonfilename in panojsons:
   pano_metadata = jsonfilename[0:-5].split('_')

   if pano_metadata[0] == name and pano_metadata[1] == time:
      real_total = real_total + 1

      pano_row = int(pano_metadata[4])
      pano_col = int(pano_metadata[5])

      #print str(pano_row) + ', ' + str(pano_col)

      if pano_row > max_row:
         max_row = pano_row
      if pano_col > max_col:
         max_col = pano_col

   # parse progress
   sys.stdout.write('Parsing |')
   progress = float(i) / float(jsons_count)
   for p in range(0, int(progress * 50)):
      sys.stdout.write('=')
   for p in range(int(progress * 50), 50):
      sys.stdout.write(' ')
   sys.stdout.write('| ' + str(progress*100) + ' %\r')
   sys.stdout.flush()
   i = i + 1
print ''

rows = max_row + 1
cols = max_col + 1
print str(rows) + ' x ' + str(cols)

cropped_tile_size = int(tile_size * crop_factor)

pixel_width  = cols * cropped_tile_size
pixel_height = rows * cropped_tile_size

print str(pixel_width) + "px x " + str(pixel_height) + "px"

out = Image.new('RGBA', (pixel_width, pixel_height))

i = 0
for jsonfilename in panojsons:
   pano_metadata = jsonfilename[0:-5].split('_')

   if pano_metadata[0] == name and pano_metadata[1] == time:
      #print pano_metadata
      #continue

      pano_row = int(pano_metadata[4])
      pano_col = int(pano_metadata[5])

      jsonfile = open(jsondir + '/' + jsonfilename, 'r')
      pano = json.loads(jsonfile.read())
      jsonfile.close()

      panoid    = pano[u'Location'][u'panoId']
      yaw       = pano[u'Projection'][u'pano_yaw_deg']
      latitude  = pano[u'Location'][u'lat']
      longitude = pano[u'Location'][u'lng']
      ll = str(latitude) + ',' + str(longitude)

      first_tile_filename = 'data/panotile/' + panoid + '_z2_0_0.jpeg'

      left   = int((tile_size - cropped_tile_size) / 2);
      top    = left;
      right  = left + cropped_tile_size;
      bottom = top + cropped_tile_size;

      #print (left, top, right, bottom)

      tile = Image.open(first_tile_filename)
      tile = tile.crop((left, top, right, bottom))

      out.paste(tile, (cropped_tile_size * pano_col, cropped_tile_size * rows - (cropped_tile_size * (pano_row+1))))

      #yaw_html = yaw + '<div style="display:block; width:80px; height:80px;"><div style="display:block;width:80px; height:3px; background-color:black; border:2px solid white; -webkit-transform: rotate('+str(float(yaw)+90)+'deg);"></div></div>'
      #map_html = '<a href="http://maps.google.com/maps?q='+ll+'">Full Map</a><br/><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.com/maps?f=q&amp;source=s_q&amp;hl=en&amp;geocode=&amp;q=40.759351,-73.885095&amp;aq=&amp;sll=33.775566,-84.375391&amp;sspn=0.012646,0.019183&amp;vpsrc=0&amp;ie=UTF8&amp;t=m&amp;z=16&amp;ll=' + ll + '&amp;output=embed"></iframe>'

      #html_tile_row = html_tile_row + '<td><img src="../panotile/'+first_tile_filename+'" width="512" height="512" /></td>'
      #html_yaw_row  = html_yaw_row + '<td>' + yaw_html + '</td>'
      #html_map_row  = html_map_row + '<td>' + map_html + '</td>'

      # Composite progress
      sys.stdout.write('Compositing |')
      progress = float(i) / float(real_total)
      for p in range(0, int(progress * 50)):
         sys.stdout.write('=')
      for p in range(int(progress * 50), 50):
         sys.stdout.write(' ')
      sys.stdout.write('| ' + str(progress*100) + ' %\r')
      sys.stdout.flush()
      i = i + 1
print ''
   
out.save('data/look/' + name + '_' + str(time) + '_' + str(cropped_tile_size) + '.jpg', 'JPEG')
