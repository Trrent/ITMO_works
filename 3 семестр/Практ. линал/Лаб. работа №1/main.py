import numpy as np
from random import randint

# Алфавит и его обратная версия для преобразования
alphabet = {
    'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6, 'Ж': 7, 'З': 8, 'И': 9,
    'Й': 10, 'К': 11, 'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18,
    'Т': 19, 'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Э': 27,
    'Ю': 28, 'Я': 29, ' ': 30
}
reverse_alphabet = {v: k for k, v in alphabet.items()}

# Преобразование сообщения в числа
def message_to_numbers(message, alphabet):
    return [alphabet[char] for char in message]

# Преобразование чисел обратно в символы
def numbers_to_message(numbers, reverse_alphabet):
    return ''.join([reverse_alphabet[num] for num in numbers])

# Шифрование сообщения
def encrypt_message(message_numbers, key_matrix, modulus=31):
    # encrypted_message = []
    # for i in range(0, len(message_numbers), 2):
    #     pair = np.array([message_numbers[i], message_numbers[i + 1]])
    #     encrypted_pair = np.dot(key_matrix, pair) % modulus
    #     encrypted_message.extend(encrypted_pair)
    # return encrypted_message
    return (key_matrix * np.array(message_numbers).reshape((2, 6))) % modulus

# Расшифровка сообщения с помощью обратной матрицы
def decrypt_message(encrypted_numbers, key_matrix, modulus=31):
    decrypted_message = []
    inverse_key_matrix = mod_inverse_matrix(key_matrix, modulus)
    for i in range(0, len(encrypted_numbers), 2):
        pair = np.array([encrypted_numbers[i], encrypted_numbers[i + 1]])
        decrypted_pair = np.dot(inverse_key_matrix, pair) % modulus
        decrypted_message.extend(decrypted_pair)
    return decrypted_message

# Нахождение обратной матрицы по модулю
def mod_inverse_matrix(matrix, modulus=31):
    det = int(np.round(np.linalg.det(matrix)))  # Определитель
    det_inv = pow(det, -1, modulus)  # Обратное к определителю по модулю
    adjugate_matrix = np.round(det * np.linalg.inv(matrix)).astype(int) % modulus  # Сопряженная матрица
    return (det_inv * adjugate_matrix) % modulus

# Создание случайной ключевой матрицы 2x2
def generate_random_key_matrix(modulus=31):
    return np.array([[randint(0, modulus - 1), randint(0, modulus - 1)],
                     [randint(0, modulus - 1), randint(0, modulus - 1)]])

# Исходные сообщения
message_1 = "ПРИВЕТ Я РОН"
message_2 = "АВТОМАТ ШИФР"

# Преобразуем сообщения в числовую форму
msg_1_numbers = message_to_numbers(message_1, alphabet)
msg_2_numbers = message_to_numbers(message_2, alphabet)

print(np.array(msg_1_numbers).reshape((2, 6)))
# Шаг 1: Генерация случайного ключа
key_matrix = generate_random_key_matrix()
key_matrix = np.array([18, 30, 25, 0]).reshape((2, 2))
print(key_matrix)

# Шаг 2: Шифрование двух сообщений с помощью ключевой матрицы
encrypted_msg_1 = encrypt_message(msg_1_numbers, key_matrix)
encrypted_msg_2 = encrypt_message(msg_2_numbers, key_matrix)

# Выводим результаты
print(f"Изначальный ключ:\n{key_matrix}")
print([int(i) for i in encrypted_msg_1])
print([int(i) for i in encrypted_msg_2])
print(f"Зашифрованное сообщение 1: {numbers_to_message(encrypted_msg_1, reverse_alphabet)}")
print(f"Зашифрованное сообщение 2: {numbers_to_message(encrypted_msg_2, reverse_alphabet)}")

# Шаг 3: Нахождение ключа на основе первой пары сообщений
# Используем первые две буквы из зашифрованного и исходного сообщения для нахождения ключа
known_decrypted_pairs = np.array([msg_1_numbers[:2], msg_1_numbers[6:8]], dtype=np.int64)
known_encrypted_pairs = np.array([encrypted_msg_1[:2], encrypted_msg_1[6:8]], dtype=np.int64)

# Решаем систему уравнений для нахождения ключа
found_key_matrix = np.linalg.solve(known_decrypted_pairs, known_encrypted_pairs)
found_key_matrix = np.round(found_key_matrix).astype(int) % 31

print(f"Найденный ключ:\n{found_key_matrix}")

# Шаг 4: Расшифровка второго сообщения с найденным ключом
decrypted_msg_2 = decrypt_message(encrypted_msg_2, found_key_matrix)
decrypted_message_2 = numbers_to_message(decrypted_msg_2, reverse_alphabet)

print(f"Расшифрованное сообщение 2: {decrypted_message_2}")

# Сравнение найденного ключа с оригинальным
if np.array_equal(key_matrix, found_key_matrix):
    print("Ключ был успешно восстановлен!")
else:
    print("Ошибка! Найденный ключ не совпадает с оригинальным.")
