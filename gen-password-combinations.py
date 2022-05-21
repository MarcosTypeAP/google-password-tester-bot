# Python
import itertools
import sys


def get_passwd_part_groups(file_name):
    passwd_part_groups = []

    with open(file_name, 'r') as fp:
        current_part = 1
        line_num = 0

        for file_line in fp.readlines():
            line_num += 1
            file_name = file_name.strip()

            if file_line == '\n':
                double_new_line = len(passwd_part_groups) != current_part
                if not passwd_part_groups or double_new_line:
                    print(f'Syntax error in line {line_num}.')
                    return
                current_part += 1
            else:
                if len(passwd_part_groups) == current_part:
                    passwd_part_groups[current_part - 1].append(file_line[:-1])
                else:
                    passwd_part_groups.append([file_line[:-1]])

    return passwd_part_groups


def main():
    input_file = sys.argv[1]
    output_file = 'passwords.txt'
    tested_passwords_files = sys.argv[2:]
    tested_passwds = set()

    passwd_part_groups = get_passwd_part_groups(input_file)
    if not passwd_part_groups:
        return

    passwd_in_parts_list = itertools.product(*passwd_part_groups)

    for tested_passwords_file in tested_passwords_files:
        with open(tested_passwords_file, 'r') as fp:
            tested_passwds.update([
                line.rsplit(' ', 1)[0]  # 'password 0\n'
                for line in fp.readlines()
            ])

    passwords = (
        ''.join(passwd_in_parts) + ' 0\n'
        for passwd_in_parts in passwd_in_parts_list
        if not tested_passwds or ''.join(passwd_in_parts) not in tested_passwds
    )

    with open(output_file, 'w') as fp:
        fp.writelines(passwords)


if __name__ == '__main__':
    main()
