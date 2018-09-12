import re

def AnalyseText(in_fn):
    print('Analysing {}...'.format(in_fn))
    vocab = set()
    contractions = set()
    word_count = 0
    sentences_count = 0
    with(open(in_fn, 'r')) as in_file:
        for s in in_file:
            sentences_count += 1
            words = s.split(' ')
            for w in words:
                word_count += 1
                vocab.add(w)
                if "'" in w:
                    contractions.add(w)
    print('Vocabulary size : {}'.format(len(vocab)))
    print('Sentences count : {}'.format(sentences_count))
    print('Word count : {}'.format(word_count))
    print('Detected contractions : {}'.format(contractions))

def FindSplits(in_fn, train_portion):
    print('Trying split for {} with a {}% train portion...'.format(in_fn, train_portion * 100))
    corpus = []
    with(open(in_fn, 'r')) as in_file:
        for s in in_file:
            words = s.split(' ')
            for w in words:
                corpus.append(w)
    last_index = int(len(corpus) * train_portion)
    train_vocab = set()
    test_vocab = set()
    for i in range(last_index):
        train_vocab.add(corpus[i])
    for i in range(last_index, len(corpus)):
        test_vocab.add(corpus[i])
    avoids_unk = len(train_vocab.intersection(test_vocab)) == len(test_vocab)
    print('Train vocabulary size : {}'.format(len(train_vocab)))
    print('Does {}/{} split avoids UNK: {}'.format(train_portion*100, (1-train_portion)*100, avoids_unk))


def SplitWords(s):
    words = []
    word_count = 0
    for m in re.finditer(r"(^|[\s'\-`])([a-zA-Z]+\w*[a-zA-Z]*)", s):
        words.append(m.group(2))
        word_count += 1
    return words, word_count

def CleanSentence(s):
    words, wc = SplitWords(s)
    clean = []
    for w in words:
        clean.append(w + " ")
    return ''.join(clean).rstrip(), wc


def CountDuplicates(in_fn):
    print('Couting duplicates in {}...'.format(in_fn))
    num_duplicates = 0
    sentences = set()
    with(open(in_fn,'r')) as in_file:
        for s in in_file:
            if s in sentences:
                num_duplicates += 1
            else:
                sentences.add(s)
    print('Total amount of duplcates : {}'.format(num_duplicates))


def SentencesToDistinct(in_fn, out_fn, s_pool):
    print('Processing {} into {}...'.format(in_fn, out_fn))
    with(open(in_fn,'r')) as in_file:
        with(open(out_fn,'a')) as out_file:
            for s in in_file:
                cs, _ = CleanSentence(s)
                if cs not in s_pool:
                    s_pool.add(cs)
                    out_file.write(cs + '\n')


def Concatenate(out_file, *in_files):
    print('Concatenating in {}...'.format(out_file))
    with(open(out_file, 'a')) as out:
        for f in in_files:
            print('Appending {}'.format(f))
            with(open(f, 'r')) as inF:
                for s in inF:
                    out.write(s)

def AnalyseDuplicates(in_fn):
    print('analysing duplicates in {}...'.format(in_fn))
    sentences = set()
    duplicates = {}
    num_duplicates = 0
    avg_dup_len = 0.
    with(open(in_fn, 'r')) as in_file:
        for s in in_file:
            cs, wc = CleanSentence(s)
            if wc == 0:
                continue
            if cs in sentences:
                if cs in duplicates:
                    duplicates[cs] += 1
                    avg_dup_len += wc
                else:
                    duplicates[cs] = 1
                num_duplicates += 1
            else:
                sentences.add(cs)
    dup_ratio = float(num_duplicates)/(len(sentences) + num_duplicates) * 100
    print('Total amount of sentences : {}'.format(len(sentences) + num_duplicates))
    print('Total amount of duplicates : {}({}%)'.format(num_duplicates, dup_ratio))
    print('Average sentence length of a duplicate : {}'.format(avg_dup_len / num_duplicates))
    top_dups = sorted(duplicates, key=duplicates.get, reverse=True)
    TOP_N = 100
    print('Top {} duplicate sentences : '.format(TOP_N))
    for i in range(TOP_N):
        print('\t{}:{}'.format(top_dups[i], duplicates[top_dups[i]]))


# FindSplits('distinct_sentences.txt', 0.9)
AnalyseText('distinct_sentences.txt')
# Concatenate('total_sentences.txt', 'books_large_p1.txt', 'books_large_p2.txt')
# AnalyseDuplicates('books_in_sentences.txt')
# sentences = set()
# SentencesToDistinct('books_in_sentences.txt', 'distinct_sentences.txt', sentences)
# SentencesToDistinct('books_large_p2.txt', 'distinct_sentences.txt', sentences)
# CountDuplicates('books_large_p1.txt')
# CountDuplicates('books_large_p2.txt')
# CountDuplicates('distinct_sentences.txt')
