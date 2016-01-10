from random import randint

generatedInput = ""
for i in range(20000):
    if randint(0, 1) == 0:
        generatedInput += '<'
    else:
        generatedInput += '3'

print generatedInput
