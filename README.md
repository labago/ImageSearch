ImageSearch (Working Title)
===========

Semester Project

Authors:
Jonathan Lane
Mike Allen
Julio Maniratunga
Taylor Johndrew

Example Usage

<code>python ImageSearch.py -p TestImages/morning.png -s TestImages/morning.png </code>

Should return MATCHES in the console output

TO MAKE SPIMS FILE

Make sure the parser location declaration (located at the top of the ImageSearch.py file) is correct. The one already there should work on CCIS linux boxes. Then, make sure the file has execution permissions and rename the file to "spims". Run the program like the following example

<code>./spims -p TestImages/morning.png -s TestImages/morning.png </code>