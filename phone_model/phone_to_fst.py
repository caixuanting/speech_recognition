import sys

input_file = open(sys.argv[1] + '/' + sys.argv[2])

lines = input_file.readlines()

for line in lines:
    line = line.strip()

    output_file = open(sys.argv[1] + '/' + line + '.config', 'w')

    output_file.write('0 0 <blank> <blank>\n')
    output_file.write('0 1 ' + line + ' ' + line + '\n')
    output_file.write('1 1 ' + line + ' ' + '<epsilon>\n')
    output_file.write('1 2 <epsilon> <epsilon>\n')
    output_file.write('2 2 <blank> <blank>\n')
    output_file.write('2')

    output_file.close()

input_file.close()