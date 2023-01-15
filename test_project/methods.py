from postgresql import PlatesViewer


def plates_autoincrement(amount):
    plate = PlatesViewer.get_plates(['plate'], 'ORDER BY pk DESC LIMIT 1')[0][0]
    letters = plate[0]+plate[4:6]
    digits = int(plate[1:4])
    print(letters, digits)
    digits += 1
    if digits > 999:
        digits = '001'


def translit(plate, translit_dict):
    for letter in plate:
        if letter in translit_dict:
            plate = plate.replace(letter, translit_dict[letter])
    return plate

def generate_plates(request):
    amount = request.args.get('amount')
    try:
        plates_autoincrement(int(amount) if amount else 1)
    except ValueError: