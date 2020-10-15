from PIL import Image
from numpy import *
import os, sys

morse_dict = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.',
    'G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..',
    'M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.',
    'S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
    'Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--',
    '4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-',',':'--..--','?':'..--..',"'":'.----.','/':'-..-.','(':'-.--.-',
    ')':'-.--.-',':':'---...',';':'-.-.-.','=':'-...-','+':'.-.-.','-':'-....-',
    '_':'..--.-','"':'.-..-.','$':'...-..-','':''
    }

def getLetterForMorse(morse):
    for key, value in morse_dict.iteritems():
        if(value == morse):
            return str(key)

def decoder(im):
    W, H = im.size
    px = im.load()
    array = []

    #extract pixels, pass it to array
    for x in range(W):
        for y in range(H):
            array.append(px[x,y])

    #get background color and pixel color
    background = array[0]
    for i in range(len(array)):
        if array[i] != background:
            mypixel = array[i]
            break

    subanswer = "x"

    #detect if blank or pixel on each column and generate preanswer
    for i in range(3, 68, 3):
        if (array[i] == background) and (array[i + 1] == background) and (array[i + 2] == background):
            subanswer = subanswer + "x"
        else:
            subanswer = subanswer + "-"

    answer = ""
    removex = 0
    #detect how many blank spaces at the end to remove them
    for i in range(len(subanswer) - 1, 0, -1):
        if subanswer[i] == "x":
            removex += 1
        else:
            break

    answer = subanswer[1:-removex]

    #print answer
    morse = ""

    #translate the answer to a simpler morse code to look for into the dictionary
    i = 0
    while i < len(answer):
        if answer[i] == "-":
            if(i < len(answer) - 2):
                if answer[i + 1] == "-":
                    if answer[i + 2] == "-":
                        morse = morse + "-"
                        i = i + 3
                    else:
                        i += 1
                else:
                    morse = morse + "."
                    i += 1
            else:
                morse = morse + "."
                i += 1
        else:
            i += 1

    final = getLetterForMorse(morse)
    return final

#crop image depending on size of original
def split_image(img,index):
    left_top = 0 + (index * 2)
    right_bottom = 3 + (index * 2)
    box = (0, left_top, 25, right_bottom)
    crop = img.crop(box)
    return crop

def main():
    #load image
    img = Image.open(r"pwd.png")
    W, H = img.size
    password = []

    #check size of image
    if H > 3:
        size = ((H - 3) / 2) + 1
    else:
        size = 1

    if size == 1:
        password.append(decoder(img))
    else:
        for i in range(size):
            crop = split_image(img, i)
            password.append(decoder(crop))

    finalpass = ""
    for c in range(len(password)):
        finalpass = finalpass + password[c]

    print finalpass

if __name__ == '__main__':
    main()
