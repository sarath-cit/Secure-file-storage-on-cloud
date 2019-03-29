import random
import time
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4

file_length = 0
split_length = 0
current_split = 1
count = 0
algorithm = "aes"
input_file_name = "input.txt"
encrypted_file_name = "encrypted_file.txt"
decrypted_file_name = "decrypted_file.txt"
aes_key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
aes_iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
des_key = ''.join(chr(random.randint(0, 0xFF)) for i in range(8))
arc4_key = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
BS = 16 #Byte size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt_in_aes(key, msg, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.encrypt(pad(msg))

def decrypt_in_aes(key, msg, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return unpad(aes.decrypt(msg))

def encrypt_in_des(key, msg):
	des = DES.new(key, DES.MODE_ECB)
	return des.encrypt(pad(msg))

def decrypt_in_des(key, msg):
	des = DES.new(key, DES.MODE_ECB)
	return unpad(des.decrypt(msg))

def encrypt_in_arc4(key, msg):
	arc4 = ARC4.new(key)
	return arc4.encrypt(msg)

def decrypt_in_arc4(key, msg):
	arc4 = ARC4.new(key)
	return arc4.decrypt(msg)

def encrypt_file(input_file_name, encrypted_file):
	global algorithm, count, split_length, current_split, aes_key, aes_iv, des_key, BS
	with open(input_file_name) as f:
		for line in f:
			data = line
			if(algorithm == "aes"):
				encrypted_data = encrypt_in_aes(aes_key, data, aes_iv)
				encrypted_file.write(encrypted_data+"\n")
			elif(algorithm == "des"):
				encrypted_data = encrypt_in_des(des_key, data)
				encrypted_file.write(encrypted_data+"\n")
			elif(algorithm == "arc4"):
				encrypted_data = encrypt_in_arc4(arc4_key, data)
				encrypted_file.write(encrypted_data+"\n")
			count += 1
			if(count == split_length):
				current_split += 1
				if(current_split == 2):
					BS = 8
					algorithm = "des"
				else:
					algorithm = "arc4"
				count = 0
				if(current_split == 3 and file_length % 3 != 0):
					split_length += file_length % 3

def decrypt_file(encrypted_file_name, decrypted_file):
	global algorithm, count, split_length, current_split, aes_key, aes_iv, des_key, BS
	with open(encrypted_file_name) as f:
		for line in f:
			encrypted_data = line
			if(algorithm == "aes"):
				decrypted_data = decrypt_in_aes(aes_key, encrypted_data.rstrip(), aes_iv)
				decrypted_file.write(decrypted_data)
			elif(algorithm == "des"):
				decrypted_data = decrypt_in_des(des_key, encrypted_data.rstrip())
				decrypted_file.write(decrypted_data)
			elif(algorithm == "arc4"):
				decrypted_data = decrypt_in_arc4(arc4_key, encrypted_data.rstrip())
				decrypted_file.write(decrypted_data)
			count += 1
			if(count == split_length):
				current_split += 1
				if(current_split == 2):
					BS = 8
					algorithm = "des"
				else:
					algorithm = "arc4"
				count = 0
				if(current_split == 3 and file_length % 3 != 0):
					split_length += file_length % 3

with open("input.txt") as f:
	for line in f:
		file_length += 1

print "file length: ", file_length
split_length = file_length / 3
print "split length: ", split_length

encrypted_file = open(encrypted_file_name, "w")
encrypt_file(input_file_name, encrypted_file)

encrypted_file = open(encrypted_file_name, "r")
decrypted_file = open(decrypted_file_name, "w")
algorithm = "aes"
BS = 16
count = 0
current_split = 1
decrypt_file(encrypted_file_name, decrypted_file)
