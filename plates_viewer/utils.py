from uuid import UUID, uuid4
from .models import PlatesDatabase
from plates_viewer import db
from re import match


class Plate:
    PLATE_LETTERS = ['а', 'в', 'с', 'е', 'н', 'к', 'м', 'о', 'р', 'т', 'х', 'у',
                     'a', 'b', 'c', 'e', 'h', 'k', 'm', 'o', 'p', 't', 'x', 'y']
    plate_pattern = fr'{PLATE_LETTERS}\d{{3}}{PLATE_LETTERS}{{2}}\d{{2,3}}'

    let_trans = str.maketrans(''.join(PLATE_LETTERS[:12]), ''.join(PLATE_LETTERS[12:]), '1234567890')
    dig_trans = str.maketrans('1234567890', '1234567890', ''.join(PLATE_LETTERS))

    def __init__(self, value):
        self.value = value
        self.letters = value.translate(self.let_trans)
        self.digits = int(value.translate(self.dig_trans)[:3])
        self.region = int(value.translate(self.dig_trans)[3:])

    @staticmethod
    def check(plate_chars):
        result = match(pattern=Plate.plate_pattern, string=plate_chars)
        return bool(result)

    def get_char_increment(self):
        def let_increment(self):
            letter_idx = self.PLATE_LETTERS.index(self.letters[-1])
            self.letters = self.letters[:-1]
            if letter_idx == 23:
                if self.letters == '':
                    self.letters = 'a'
                    self.region += 100
                else:
                    let_increment(self)
                    self.letters += 'a'
            else:
                self.new_letter = self.PLATE_LETTERS[letter_idx + 1]
                self.letters += self.new_letter
        self.digits += 1
        if self.digits == 1000:
            self.digits = 1
            let_increment(self)

    def show(self):
        return self.letters[0] + str(self.digits) + self.letters[1:3] + str(self.region)

    plate = property(fget=show)


def is_uuid(plate_id):
    try:
        UUID(plate_id)
        return True
    except ValueError:
        return False


def generate_plate(last_plate, amount):
    last_plate = Plate(last_plate)
    for _ in range(amount):
        last_plate.get_char_increment()
        db.session.add(PlatesDatabase(last_plate.plate))
