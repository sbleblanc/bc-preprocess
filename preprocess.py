import re

def CleanSentence(s):
    word_count = 0
    cleaned = []
    for m in re.finditer(r"\w?['\w]*\w", s):
        cleaned.append(m.group() + ' ')
        word_count += 1
    return ''.join(cleaned).rstrip(), word_count


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
                if s not in s_pool:
                    s_pool.add(s)
                    out_file.write(s)


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


AnalyseDuplicates('total_sentences.txt')
#sentences = set()
#SentencesToDistinct('books_large_p1.txt', 'distinct_sentences.txt', sentences)
#SentencesToDistinct('books_large_p2.txt', 'distinct_sentences.txt', sentences)
#CountDuplicates('books_large_p1.txt')
#CountDuplicates('books_large_p2.txt')
#CountDuplicates('distinct_sentences.txt')
