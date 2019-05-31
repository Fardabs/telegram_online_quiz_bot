conf_file = open("./online_exam_bot.config","r")

lines = conf_file.readlines()

data = []

conf = {}

i = 0
for line in lines:
    if i <= 10:
        extracted = line.split("'")
        data.append(extracted)
        if i != 5:
            conf[data[i][1]] = data[i][3]
        else:
            pass
        i += 1
