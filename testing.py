#
# == TESTING THE CALIBRATION RECOVERY HERE == 
#

calibration = []
with open('calibration.txt', mode = 'r', encoding='utf-8') as file:
    calibration = file.read()

print(calibration)
test_list = list(eval(calibration))

print(test_list[1])