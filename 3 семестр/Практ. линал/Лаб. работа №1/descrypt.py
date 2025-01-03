from random import randint

import numpy as np

alphabet = {
    'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6, 'Ж': 7, 'З': 8, 'И': 9,
    'Й': 10, 'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18,
    'Т': 19, 'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Э': 27,
    'Ю': 28, 'Я': 29, ' ': 30
}
reverse_alphabet = {v: k for k, v in alphabet.items()}


def message_to_numbers(message, alphabet):
    return [alphabet[char] for char in message]


def generate_random_key_matrix(modulus=31):
    return np.array([[randint(0, modulus - 1), randint(0, modulus - 1)],
                     [randint(0, modulus - 1), randint(0, modulus - 1)]])


message_1 = "ПРИВЕТ Я РОН"
message_2 = "АВТОМАТ ШИФР"

msg_1_numbers = np.array(message_to_numbers(message_1, alphabet)).reshape((2, 6,))
msg_2_numbers = np.array(message_to_numbers(message_2, alphabet)).reshape((2, 6,))

key_matrix = np.array([18, 6, 15, 13]).reshape((2, 2))
# key_matrix = generate_random_key_matrix()

encrypted_msg_1 = np.matmul(key_matrix, msg_1_numbers) % 31
encrypted_msg_2 = np.matmul(key_matrix, msg_2_numbers) % 31
print(encrypted_msg_2)

print(' \\\\ \n'.join([' & '.join(map(str, i)) for i in encrypted_msg_1]))
print(' \\\\ \n'.join([' & '.join(map(str, i)) for i in encrypted_msg_2]))

for x in range(31):
    for y in range(31):
        if (16 * x + 30 * y) % 31 == encrypted_msg_1[0][0] and (17 * x + 29 * y) % 31 == encrypted_msg_1[0][1] and (
                9 * x + 30 * y) % 31 == encrypted_msg_1[0][2] and (
                2 * x + 17 * y) % 31 == encrypted_msg_1[0][3] and (5 * x + 15 * y) % 31 == encrypted_msg_1[0][4] and (
                19 * x + 14 * y) % 31 == encrypted_msg_1[0][5]:
            print(x, y)

for x in range(31):
    for y in range(31):
        if (16 * x + 30 * y) % 31 == encrypted_msg_1[1][0] and (17 * x + 29 * y) % 31 == encrypted_msg_1[1][1] and (
                9 * x + 30 * y) % 31 == encrypted_msg_1[1][2] and (
                2 * x + 17 * y) % 31 == encrypted_msg_1[1][3] and (5 * x + 15 * y) % 31 == encrypted_msg_1[1][4] and (
                19 * x + 14 * y) % 31 == encrypted_msg_1[1][5]:
            print(x, y)


matrix = np.array([27, 9, 7, 4]).reshape((2, 2))
ans = np.matmul(matrix, encrypted_msg_2) % 31
print(' \\\\ \n'.join([' & '.join(map(str, i)) for i in ans]))
# print(key_matrix)
