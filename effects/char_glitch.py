import random

def glitch_text(text, glitch_chance=0.1):
    glitch_chars = ['@', '#', '$', '%', '&', '*']
    result = ''
    for c in text:
        if random.random() < glitch_chance and c.isalpha():
            result += random.choice(glitch_chars)
        else:
            result += c
    return result
