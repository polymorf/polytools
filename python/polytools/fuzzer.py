from polytools.crypto import xor

def to_bytes(val, byte_len):
	hex_val = hex(val).replace("0x","").replace("L","")
	out_bytes_hex = ("0" * (byte_len - len(hex_val)) + hex_val)
	return b"".fromhex(out_bytes_hex)

def xor(key,data):
	out=b""
	for i,c in enumerate(data):
		key_byte = key[i%len(key)]
		out += bytes([c ^ key_byte])
	return out


def bit_flipper_X(data_in, pre_mask):
	for bit_pos in reversed(range((len(data_in) * 8)-1)):
		msg_hex_len = len(data_in)*2
		for mask in pre_mask:
			mask2 = to_bytes(mask<<bit_pos, msg_hex_len)
			data = xor(mask2, data_in)
			yield data

def bit_flipper_1(data_in):
	return bit_flipper_X(data_in, [1])

def bit_flipper_2(data_in):
	return bit_flipper_X(data_in, [0b1, 0b11])

def bit_flipper_3(data_in):
	return bit_flipper_X(data_in, [0b1, 0b101, 0b011, 0b111])

