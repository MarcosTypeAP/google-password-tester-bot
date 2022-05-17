import itertools
import sys


def get_passwd_parts_groups(file_name):
    passwd_parts_groups = []

    with open(file_name, 'r') as fp:
        current_part = 0
        line_num = 0

        for fl in fp.readlines():
            line_num += 1

            if fl == '\n':
                double_new_line = len(passwd_parts_groups) != current_part + 1
                if not passwd_parts_groups or double_new_line:
                    print(f'Syntax error in line {line_num}.')
                    return
                current_part += 1
            else:
                if len(passwd_parts_groups) == current_part + 1:
                    passwd_parts_groups[current_part].append(fl[:-1])
                else:
                    passwd_parts_groups.append([fl[:-1]])

    return passwd_parts_groups


def main():
    input_file = 'passwd-params.txt'
    output_file = 'passwords.txt'
    tested_passwords_files = sys.argv[1:]
    tested_passwds = set()

    passwd_parts_groups = get_passwd_parts_groups(input_file)
    passwds_in_parts = itertools.product(*passwd_parts_groups)

    if tested_passwords_files:
        for tested_passwords_file in tested_passwords_files:
            with open(tested_passwords_file, 'r') as fp:
                tested_passwds.update([
                    line.rsplit(' ', 1)[0]
                    for line in fp.readlines()
                ])
    #  print(len(list(passwds_in_parts)), len(tested_passwds))

    passwords = (
        ''.join(passwd_parts) + ' 0\n'
        for passwd_parts in passwds_in_parts
        if not tested_passwds or ''.join(passwd_parts) not in tested_passwds
    )

    with open(output_file, 'w') as fp:
        fp.writelines(passwords)


if __name__ == '__main__':
    main()
