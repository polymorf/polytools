from log import *
from print_obj import print_obj

def xor(key,data):
	out=""
	for i,c in enumerate(data):
		key_byte = ord(key[i%len(key)])
		out += chr(ord(c) ^ key_byte)
	return out

def pkcs1_unpad(text):
	if len(text) > 0 and text[0] == '\x02':
		pos = text.find('\x00')
		if pos > 0:
			return text[pos + 1:]
		return None

def pkcs7_pad(cleartext_data):
	pad_len = 0x10 - (len(cleartext_data) % 0x10)
	return cleartext_data + chr(pad_len) * pad_len

def pkcs7_unpad(cleartext_data):
	pad_len=ord(cleartext_data[-1])
	if pad_len == 0 or pad_len > 0x10:
		#error("bad pkcs7 padding")
		return None
	for i in range(pad_len):
		if ord(cleartext_data[-1]) != pad_len:
			#error("bad pkcs7 padding")
			return None
		cleartext_data=cleartext_data[:-1]
	return cleartext_data

def jwt_b64dec(data):
	data = data.replace("-", "+")
	data = data.replace("_", "/")
	data += (4 - len(data) % 4) * "="
	return data.decode("base64")

def jwt_b64enc(data):
	data = data.encode("base64").replace("\n","")
	data = data.replace("+", "-")
	data = data.replace("/", "_")
	data = data.replace("=", "")
	return data

def jwt_parse(data):
	splited = data.split(".")
	for i in range(len(splited)):
		splited[i] = repr(jwt_b64dec(splited[i]))[1:-1]
	print_obj(splited)

