file_length = 0
split_length = 0
current_split = 1
count = 0
output_file = open("output.txt", "w")

with open("input.txt") as f:
	for line in f:
		file_length += 1

print "file length: ", file_length
split_length = file_length / 3
print "split length: ", split_length

with open("input.txt") as f:
	for line in f:
		print(line)
		output_file.write(line)
		count += 1
		print "count: ", count
		if(count == split_length):
			print "change algorithm"
			current_split += 1
			count = 0
			if(current_split == 3 and file_length % 3 != 0):
				split_length += file_length % 3
