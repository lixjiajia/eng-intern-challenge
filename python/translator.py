import re
import argparse

braille_map = {
    'a' : 'O.....', 'b' : 'O.O...', 'c' : 'OO....', 'd': 'OO.O..', 'e' : 'O..O..', 'f' : 'OOO...', 'g':'OOOO..', 'h' : 'O.OO..', 'i':'.OO...',
    'j' : '.OOO..', 'k' : 'O...O.', 'l' : 'O.O.O.', 'm' : 'OO..O.', 'n' : 'OO.OO.', 'o' : 'O..OO.', 'p' : 'OOO.O.', 'q' : 'OOOOO.', 'r' : 'O.OOO.',
    's' : '.OO.O.', 't' : '.OOOO.', 'u' : 'O...OO', 'v' : 'O.O.OO', 'w' : '.OOO.O', 'x' : 'OO..OO', 'y' : 'OO.OOO', 'z' : 'O..OOO',
    '1' : 'O.....', '2' : 'O.O...', '3' : 'OO....', '4' : 'OO.O..', '5' : 'O..O..', '6' : 'OOO...', '7' : 'OOOO..', '8' : 'O.OO..', '9' : '.OO...',
    '0' : '.OOO..', 'CAP' : '.....O', 'DEC' : '.O...O', 'NUM' : '.O.OOO', '.' : '..OO.O', ',' : '..O...', '?' : '..O.OO', '!' : '..OOO.', 
    ':' : '..OO..', ';' : '..O.O.', '-' : '....OO', '/' : '.O..O.', '<' : '.OO..O', '>' : 'O..OO.', '(' : 'O.O..O', ')' : '.O.OO.', ' ' : '......'
}
english_let_map = {v: k for k,v in braille_map.items() if k.isalpha()}
number_map = {'O.....': '1', 'O.O...': '2', 'OO....': '3', 'OO.O..': '4', 'O..O..': '5', 'OOO...': '6', 'OOOO..': '7', 'O.OO..': '8', '.OO...': '9', '.OOO..': '0', '..OO.O':'.', '..O...': ',', '..O.OO': '?', '..OOO.': '!', '..OO..': ':', '..O.O.': ';', '....OO': '-', '.O..O.': '/', '.OO..O': '<', 'O.O..O': '(', '.O.OO.': ')', '......': ' '}


def isEnglish(input_text):
    return bool(re.match(r'^[A-Za-z0-9\s,.!?]+$', input_text))

def isBraille(input_text):
    return bool(re.match('^[O.]+$', input_text)) and len(input_text) % 6 == 0

def translateToBraille(english):
    translation = []
    isNumber = False
    for i in english:
        if i.isupper():
            translation.append(braille_map['CAP'])
            translation.append(braille_map[i.lower()])
            isNumber = False
        elif i.isdigit():
            if not isNumber:
                translation.append(braille_map['NUM'])
                isNumber = True
            translation.append(braille_map[i])
        elif i == ' ':
            translation.append(braille_map[i])
            isNumber = False
        else:
            translation.append(braille_map[i])
            isNumber = False
    return ''.join(translation)

def translateToEnglish(braille):
    translation = []
    i = 0
    isCapital = False
    isNumber = False

    while i < len(braille):
        seq = braille[i:i+6]
        if seq == braille_map['CAP']:
            isCapital = True

        elif seq == braille_map['DEC'] or seq == braille_map['NUM']:
            isNumber = True
      
        elif seq == braille_map[' ']:
            translation.append(' ')
            isNumber = False
        else:
            char = english_let_map.get(seq, number_map.get(seq))
            
            if isCapital:
                translation.append(char.upper())
                isCapital = False
            elif isNumber:
                translation.append(number_map[seq])
            else:
                translation.append(char)
        i += 6

    return ''.join(translation)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+', type=str, help = 'text to be translated')
    args = parser.parse_args()
    input_text = ' '.join(args.text)

    if isBraille(input_text):
        print(translateToEnglish(input_text))
    elif isEnglish(input_text):
        print(translateToBraille(input_text))
    
    else:
        return "Invalid input text."


if __name__ == "__main__":
    main()
