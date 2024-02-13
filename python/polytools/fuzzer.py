from polytools.crypto import xor

def xor(key,data):
	out=b""
	for i,c in enumerate(data):
		key_byte = key[i%len(key)]
		out += bytes([c ^ key_byte])
	return out


def bit_flipper_X(data_in, pre_mask):
	for bit_pos in reversed(range((len(data_in) * 8))):
		for mask in pre_mask:
			mask2 = (mask << bit_pos).to_bytes(len(data_in)+1, 'big')
			mask2 = mask2[-len(data_in):]
			data = xor(mask2, data_in)
			yield data

def bit_flipper_1(data_in):
	return bit_flipper_X(data_in, [1])

def bit_flipper_2(data_in):
	return bit_flipper_X(data_in, [0b1, 0b11])

def bit_flipper_3(data_in):
	return bit_flipper_X(data_in, [0b1, 0b101, 0b011, 0b111])

