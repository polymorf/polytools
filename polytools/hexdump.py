# coding: utf8
import string


"""
0x00000000 │ 6a 4d a7 28 de d1 46 11 96 51 fc 35 cb d4 a9 29 │ jM.(..F..Q.5...) │
"""
def load_hexdump(data):
	out=""
	for line in data.split("\n"):
		if "│" not in line:
			continue
		hex_data = line.split("│")[1]
		hex_data = hex_data.replace(" ","")
		hex_data = hex_data.replace("\x1b[0m","")
		hex_data = hex_data.replace("\x1b[36;1m","")
		out+=hex_data.decode("hex")
	return out

def hexdump(buf,title="",color=6,start=0):
	color_start = "\033[3%d;1m" % color
	color_stop = "\033[0m"
	out=("           %s┌"+"─"*49+"┬"+"─"*18+"┐%s\n") % (color_start,color_stop)
	if title != "":
		dashlen = int((46-len(title))/2)
		out=("           %s┌"+"─"*dashlen+"  "+title+"  "+"─"*(dashlen-(1-(len(title)%2)))+"┬"+"─"*18+"┐%s\n") % (color_start,color_stop)
	for i in range(0,len(buf),16):
		out+="%s0x%08x │ %s" % (color_start,i+start,color_stop)
		for j in range(16):
			if i+j < len(buf):
				out+="%02x " % (ord(buf[i+j]))
			else:
				out+="   "
		out+="%s│ %s" % (color_start,color_stop)
		for j in range(16):
			if i+j < len(buf):
				if buf[i+j] in string.printable and buf[i+j] not in "\t\n\r\x0b\x0c":
					out+="%s" % (buf[i+j])
				else:
					out+="."
			else:
				out+=" "
		out+=" %s│%s\n" % (color_start,color_stop)
	out+=("           %s└"+"─"*49+"┴"+"─"*18+"┘%s") % (color_start,color_stop)
	print(out)
