import random
import time
import sys
import os
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

file_length = 0
split_length = 0
current_split = 1
count = 0
algorithm = "aes"
input_file_name = sys.argv[2]
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

def sendEmail(email_user, email_password, email_send):
	subject = 'Key'

	msg = MIMEMultipart()
	msg['From'] = email_user
	msg['To'] = email_send
	msg['Subject'] = subject

	body = 'Hi there, this is a key for hybrid decryption'
	msg.attach(MIMEText(body,'plain'))

	filename='key.txt'
	attachment = open(filename, "rb")

	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= "+filename)

	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(email_user,email_password)


	server.sendmail(email_user,email_send,text)
	server.quit()
	os.remove("key.txt")

with open("input.txt") as f:
	for line in f:
		file_length += 1

split_length = file_length / 3

if(sys.argv[1] == "encrypt"):
	encrypted_file = open(encrypted_file_name, "w")
	encrypt_file(input_file_name, encrypted_file)
	email_user = raw_input('Enter email id: ')
	email_password = raw_input('Enter password: ')
	email_send = raw_input('Enter recipient email id: ')
	filename = 'key.txt'
	attachment = open(filename, "w")
	attachment.write(str(aes_key)+"256"+str(aes_iv)+"256"+str(des_key)+"256"+str(arc4_key))
	attachment.close()
	sendEmail(email_user, email_password, email_send)
elif(sys.argv[1] == "decrypt"):
	encrypted_file = open(encrypted_file_name, "r")
	decrypted_file = open(decrypted_file_name, "w")
	algorithm = "aes"
	BS = 16
	count = 0
	current_split = 1
	keys = ""
	with open("key.txt") as f:
		for line in f:
			keys += line
	keys = keys.split("256")
	aes_key = keys[0]
	aes_iv = keys[1]
	des_key = keys[2]
	arc4_key = keys[3]
	decrypt_file(encrypted_file_name, decrypted_file)
