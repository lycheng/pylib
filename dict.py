import sys
import urllib2
from xml.dom import minidom

OKGREEN = '\033[92m'
ENDC = '\033[0m'

# use iciba
addr    = "http://dict-co.iciba.com/api/dictionary.php?w=%s"
example = "apple"
format  = "  %s %s"

def getResult( words ):
	if ( len( words ) < 1 ):
		words.append( example )

	print ' '

	for word in words:
		print OKGREEN + word + ENDC
		result = urllib2.urlopen( addr % word )
		root = minidom.parse( result ).documentElement

		poses = root.getElementsByTagName( "pos" )
		acceptations = root.getElementsByTagName( "acceptation" )

		size = min( len( poses ), len( acceptations ) )
		for i in range( size ):
			print format % ( poses[i].firstChild.nodeValue, acceptations[i].firstChild.nodeValue )

if __name__ == '__main__':
	getResult( sys.argv[1: ] )
