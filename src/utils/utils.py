crc8_table = [
    0,
    94,
    188,
    226,
    97,
    63,
    221,
    131,
    194,
    156,
    126,
    32,
    163,
    253,
    31,
    65,
    # Повний вміст таблиці ...
]


def checksum_crc8(data):
    check = 0
    for d in data:
        check = crc8_table[check ^ d]
    return check & 0x00FF
