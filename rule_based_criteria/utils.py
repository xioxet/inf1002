def word_tokenize(message -> str) -> List<str>:
    words = []
    for word in message.split(' '):
        stripped_word = ''.join([i for i in word.lower() if i in 'abcdefghijklmnopqrstuvwxyz'])
        words.append(stripped_word)
    return words

