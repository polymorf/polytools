from polytools.crypto import xor

def to_bytes(val, byte_len):
	hex_val = hex(val).replace("0x","").replace("L","")
	out_bytes = ("0" * (byte_len - len(hex_val)) + hex_val).decode("hex")
	return out_bytes

def bit_flipper_1(data_in):
	for bit_pos in reversed(range((len(data_in) * 8)-1)):
		msg_hex_len = len(data_in)*2
		mask2 = to_bytes(1<<bit_pos, msg_hex_len)
		data = xor(mask2, data_in)
		yield data

def bit_flipper_2(data_in):
	for bit_pos in reversed(range((len(data_in) * 8)-1)):
		msg_hex_len = len(data_in)*2
		for pre_mask in [0b1, 0b11]:
			mask2 = to_bytes(pre_mask<<bit_pos, msg_hex_len)
			data = xor(mask2, data_in)
			yield data

def bit_flipper_3(data_in):
	for bit_pos in reversed(range((len(data_in) * 8)-2)):
		msg_hex_len = len(data_in)*2
		for pre_mask in [0b1, 0b101, 0b011, 0b111]:
			mask2 = to_bytes(pre_mask<<bit_pos, msg_hex_len)
			data = xor(mask2, data_in)
			yield data
