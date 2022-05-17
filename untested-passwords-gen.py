def get_passwd_number(line):
    return int(line[:-1].rsplit(' ', 1)[-1])


def main():
    tested_passwd_numbers = set()
    untested_passwd_numbers = []
    new_passwd_lines = []

    with open('logs.txt', 'r') as fp:
        file_lines = fp.readlines()

    for line in file_lines:
        if "isn't valid" in line:
            tested_passwd_numbers.add(get_passwd_number(line))
    tested_passwd_numbers = list(tested_passwd_numbers)
    tested_passwd_numbers.sort()

    tested_passwd_numbers_length = len(tested_passwd_numbers)
    for index, num in enumerate(tested_passwd_numbers):
        if tested_passwd_numbers_length != index + 1:
            if tested_passwd_numbers[index + 1] != num + 1:
                passwd_numbers = list(range(
                    num + 1,
                    tested_passwd_numbers[index + 1]
                ))
                untested_passwd_numbers += passwd_numbers

    with open('passwords.txt', 'r') as fp:
        file_lines = fp.readlines()

    passwd_num = 0
    for line in file_lines:
        passwd_num += 1
        if passwd_num in untested_passwd_numbers:
            passwd = line.split(' ', 1)[0]
            passwd_line = f'{passwd} 0\n'
            new_passwd_lines.append(passwd_line)

    with open('untested-passwords.txt', 'w') as fp:
        fp.writelines(new_passwd_lines)

    for paswd_line in new_passwd_lines:
        print(passwd_line)


if __name__ == '__main__':
    main()
