pipe = []

pipe.append({'key': 1, 'test': "Test"})
pipe.append({'key': 2, 'test': "Test2"})

print pipe

for letter in pipe :
    if letter['key'] == 1 :
        print "Test"
