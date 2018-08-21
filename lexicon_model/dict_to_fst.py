import sys

if len(sys.argv) < 3:
    print('Usage:')
    print('     python dict_to_fst.py <dir> <dict_file>')

input_file = open(sys.argv[1] + '/' + sys.argv[2])
lines = input_file.readlines()

for line in lines:
    if len(line) == 0:
        pass

    components = line.strip().split()
    output_file = open(sys.argv[1] + '/' + '_'.join(components[1:]) + '.config', 'w')

    output_line = '0 1 ' + components[1] + ' ' + components[0] + '\n'
    output_file.write(output_line)

    for i in range(2, len(components)):
        output_line = str(i - 1) + ' ' + str(i) + ' ' + components[i] + ' ' + '<epsilon>' + '\n'
        output_file.write(output_line)

    output_file.write(str(len(components) - 1))

    output_file.close()


input_file.close()
