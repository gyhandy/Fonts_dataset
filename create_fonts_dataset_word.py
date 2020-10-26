#encoding: utf-8
'''
Create a font dataset:
Content / size / color(Font) / color(background) / style
E.g. A / 64/ red / blue / arial
'''
import os
import pygame

##
# 10 colors in RGB to choose from (back ground and font)
Colors = {'red': (220, 20, 60), 'orange': (255,165,0), 'Yellow': (255,255,0), 'green': (0,128,0), 'cyan' : (0,255,255),
         'blue': (0,0,255), 'purple': (128,0,128), 'pink': (255,192,203), 'chocolate': (210,105,30), 'silver': (192,192,192)}
# 3 Sizes of fonts
Sizes = {'small': 20, 'medium': 40, 'large': 60}
# Styles. All_fonts is the set of all styles in the current OS, we exclude useless fonts in this set.
All_fonts = pygame.font.get_fonts()
useless_fonts = ['notocoloremoji', 'droidsansfallback', 'gubbi', 'kalapi', 'lklug',  'mrykacstqurn', 'ori1uni','pothana2000','vemana2000',
                'navilu', 'opensymbol', 'padmmaa', 'raghumalayalam', 'saab', 'samyakdevanagari']
useless_fontsets = ['kacst', 'lohit', 'sam']

# throw away the useless
for useless_font in useless_fonts:
    if useless_font in All_fonts:
        All_fonts.remove(useless_font)
temp = All_fonts.copy()
for useless_font in temp: # check every one
    for set in useless_fontsets:
        if set in useless_font:
            try:
                All_fonts.remove(useless_font)
            except:
                print(useless_font)
# 52 letters
Letters = list(range(65, 91)) + list(range(97, 123))
Integers = list(range(48, 58))
single_set = Letters + Integers
words = []
img_size = 128


# generate words using a depth-first-search, max_w_len is the maximum length of the words, for now is one(single characters)
max_w_len = 1

'''
dfs takes a list L containing the single characters and use them to construct words of all permutations of characters 
with a maximum length of max_w_len
dfs also takes an empty string as a starting point
'''
def dfs(w, L):
    if len(w)==max_w_len:
        return
    for l in L:
        words.append(w+chr(l))
        dfs(w+chr(l), L)


dfs('', single_set)

# directory to save the dataset
font_dir = './fonts'
if not os.path.exists(font_dir):
    os.makedirs(font_dir)


# initialize pygame and start to generate the dataset
pygame.init()
screen = pygame.display.set_mode((img_size, img_size)) # image size Fix(128 * 128)
cnt = 0

# use loops to iterate all the attribute sets
for word in words: # 1st round for words
    print(word)
    for size in Sizes.keys():  # 2nd round for size
        print(size)
        for font_color in Colors.keys():  # 3rd round for font_color
            for back_color in Colors.keys():  # 4th round for back_color
                # if not back_color == font_color:''' should not be same '''
                for font in All_fonts:  # 5th round for fonts
                    if not font_color == back_color:
                        cnt +=1
                        # print(cnt)
                        try:
                            # 1 set back_color
                            screen.fill(Colors[back_color]) # background color
                            # 2 set letter/word
                            # selected_letter = chr(letter)
                            selected_letter = word
                            # 3,4 set font and size
                            selected_font = pygame.font.SysFont(font, Sizes[size]) # size and bold or not
                            font_size = selected_font.size(selected_letter);
                            # 5 set font_color

                            rtext = selected_font.render(selected_letter, True, Colors[font_color], Colors[back_color])
                            # 6 render
                            drawX = img_size / 2 - (font_size[0] / 2.0)
                            drawY = img_size / 2 - (font_size[1] / 2.0)
                            # screen.blit(rtext, (img_size/2, img_size/2))
                            # screen.blit(rtext, (img_size / 4, 0))
                            screen.blit(rtext, (drawX, drawY)) # because
                            # Save images in a specific path E.g. A / 64/ red / blue / arial
                            img_name = selected_letter + '_' + size + '_' + font_color + '_' + back_color + '_' + font + ".png"
                            img_path = os.path.join(font_dir, selected_letter, size, font_color, back_color, font)
                            if not os.path.exists(img_path):
                                os.makedirs(img_path)
                            pygame.image.save(screen, os.path.join(img_path, img_name))
                        except:
                            # print(letter, size, font_color, back_color, font)
                            print(word, size, font_color, back_color, font)
                    else:
                        break
print('finished')

