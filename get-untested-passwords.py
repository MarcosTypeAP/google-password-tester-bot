# Python
import sys


def get_passwd_number(line):
    # 01/24 19:11:50 |  'password' isn't valid - tested: 32\n
    return int(line[:-1].rsplit(' ', 1)[1])


def main():
    logs_file = sys.argv[1]
    passwords_file = sys.argv[2]
    tested_passwd_numbers = set()
    untested_passwd_numbers = []
    new_passwd_lines = []
    file_lines = open(logs_file, 'r').readlines()

    for line in file_lines:
        if "isn't valid" in line:
            tested_passwd_numbers.add(get_passwd_number(line))
    tested_passwd_numbers = list(tested_passwd_numbers)
    tested_passwd_numbers.sort()

    for index, num in enumerate(tested_passwd_numbers):
        if len(tested_passwd_numbers) != index + 1:
            if tested_passwd_numbers[index + 1] != num + 1:
                passwd_numbers = list(range(
                    num + 1,
                    tested_passwd_numbers[index + 1]
                ))
                untested_passwd_numbers += passwd_numbers

    with open(passwords_file, 'r') as fp:
        file_lines = fp.readlines()

    passwd_num = 0
    for line in file_lines:
        passwd_num += 1
        if passwd_num in untested_passwd_numbers:
            passwd_line = line.replace('1\n', '0\n')  # 'password 1\n'
            new_passwd_lines.append(passwd_line)

    with open('untested-passwords.txt', 'w') as fp:
        fp.writelines(new_passwd_lines)


if __name__ == '__main__':
    main()
