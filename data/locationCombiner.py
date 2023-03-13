data_file = open("data.txt", "r")
address_file = open("address.txt", "r")

res_file = open("res.txt", "w")


while True:
    # count-=1
    data = data_file.readline()
    address = address_file.readline()
    if not data:
        break
    data = data.split("\t")
    address = address.split("\t")
    # print(data[1], data[2],data[3], address[1], address[2])
    res_file.write(data[1] + "\t" + data[2] + "\t" + data[3] + "\t" + address[1] + "\t" + address[2])