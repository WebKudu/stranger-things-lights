# stranger-things-lights
Python script for creating Stranger Things alphet lights with WS2811 LEDs

## Prerequisites
Follow the directions on https://webkudu.com/stranger-things-lights-with-raspberry-pi/

## Configuring the script
Edit stranger.py

You will need to change the LED_COUNT if using a different number of LEDs

You may choose to change the BRIGHTNESS to a value between 0 and 1

You will almost certainly need to change ALPHABET to reflect the positioning of your lights against the alphabet wall

You may choose to change the COLORS

You may have to change the PIXEL_PIN and ORDER, according to your setup.

When done, simply run
`python3 stranger.py`

## Setting up the web server
First, create a database. The default name and password is stranger/danger. If you choose another combo, make sure to edit /app/Database.php and the initialize() funciton in stranger.py

Import stranger-server/sql/phrases.sql to set up the table
`mysql stranger -u stranger -pdanger < stranger-server/sql/phrases.sql`

Point apache or nginx at stranger-server/www

**If you choose not to use the stranger-server, be sure to remove the related lines from stranger.py**
