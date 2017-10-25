# coding: utf8
import string

def hexdump(buf,title="",color=6,start=0):
	color_start = "\033[3%d;1m" % color
	color_stop = "\033[0m"
	out=("           %s┌"+"─"*49+"┬"+"─"*18+"┐%s\n") % (color_start,color_stop)
	if title != "":
		dashlen = (46-len(title))/2
		out=("           %s┌"+"─"*dashlen+"  "+title+"  "+"─"*(dashlen-(1-(len(title)%2)))+"┬"+"─"*18+"┐%s\n") % (color_start,color_stop)
	for i in xrange(0,len(buf),16):
		out+="%s0x%08x │ %s" % (color_start,i+start,color_stop)
		for j in xrange(16):
			if i+j < len(buf):
				out+="%02x " % (ord(buf[i+j]))
			else:
				out+="   "
		out+="%s│ %s" % (color_start,color_stop)
		for j in xrange(16):
			if i+j < len(buf):
				if buf[i+j] in string.printable and buf[i+j] not in "\t\n\r\x0b\x0c":
					out+="%s" % (buf[i+j])
				else:
					out+="."
			else:
				out+=" "
		out+=" %s│%s\n" % (color_start,color_stop)
	out+=("           %s└"+"─"*49+"┴"+"─"*18+"┘%s") % (color_start,color_stop)
	print out
