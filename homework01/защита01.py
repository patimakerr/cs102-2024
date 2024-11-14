def encrypt_growing_shift(plaintext, start, delta):
    ciphertext = ''
    shift = start
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                start_ord = ord('А')
            else:
                start_ord = ord('а')
            shifted_char = chr((ord(char) - start_ord + shift) % 32 + start_ord)
        else:
            shifted_char = char
        ciphertext += shifted_char
        shift += delta
    return ciphertext
