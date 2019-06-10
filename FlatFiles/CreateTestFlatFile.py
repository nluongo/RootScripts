import os
import random

flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Test_FlatA.txt')
flat_file = open(flat_file_path, 'w')

for i in range(1000):
    l0_et = random.randint(-10, 10)
    l1_et = random.randint(-10, 10)
    l2_et = random.randint(-10, 10)
    l3_et = random.randint(-10, 10)
    had_et = random.randint(-10, 10)

    l0_et_string = str(l0_et)
    l1_et_string = str(l1_et)
    l2_et_string = str(l2_et)
    l3_et_string = str(l3_et)
    had_et_string = str(had_et)

    if l2_et > 0:
        true_et_string = str(1)
    else:
        true_et_string = str(0)

    line = l0_et_string + ',' + l1_et_string + ',' + l2_et_string + ',' + l3_et_string + ',' + had_et_string + ',' + true_et_string + '\n'

    flat_file.write(line)

flat_file.close()
