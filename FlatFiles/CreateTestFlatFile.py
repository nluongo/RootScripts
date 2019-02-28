import os
import random

flat_file_path = os.path.join(os.path.expanduser('~'), 'TauTrigger', 'Formatted Data Files', 'Test_Flat.txt')
flat_file = open(flat_file_path, 'w')

for i in range(100):
    l0_et = random.randint(1, 10)
    l1_et = random.randint(1, 10)
    l2_et = random.randint(1, 10)
    l3_et = random.randint(1, 10)
    had_et = random.randint(1, 10)

    l0_et_string = str(l0_et)
    l1_et_string = str(l1_et)
    l2_et_string = str(l2_et)
    l3_et_string = str(l3_et)
    had_et_string = str(had_et)

    true_et_string = str(2*l0_et + 5*l1_et)

    line = l0_et_string + ',' + l1_et_string + ',' + l2_et_string + ',' + l3_et_string + ',' + had_et_string + ',' + true_et_string + '\n'

    flat_file.write(line)

flat_file.close()
