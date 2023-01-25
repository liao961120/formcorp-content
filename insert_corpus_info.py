#%%
import json
import requests


class CorpusInfoSummary():

    def __init__(self):
        self.meta = self.request()
        self.LANG = {
            'kanakanavu': "卡那卡那富語",
            'rukai': "魯凱語",
            'saisiyat': "賽夏語",
            'tsou': "鄒語",
            'kavalan': "噶瑪蘭語",
            'amis': "阿美語",
            'seediq': "賽德克語",
            'atayal': "泰雅語",
            'sakizaya': "撒奇萊雅語",
            'bunun': "布農語"
        }
        self.anchor = '<!-- Auto Generated Content: Corpus Summary -->'

    def request(self):
        url = 'https://yongfu.name/glossParser/text-meta.json'
        resp = requests.get(url)
        meta = json.loads(resp.content)
        return meta


    def get_lang_textnum(self, lang):
        lang = lang.lower()
        text_info = {
            # 'story': 0,
            # 'sent': 0
            'story_num': 0,
            'sentence_num': 0,
            'grammar_sent_num': 0,
            'word_class_sent_num': 0,
        }

        for name, data in self.meta.items():
            if lang not in name.lower(): continue

            # Sentence num
            text_info['sentence_num'] = data['summary']['sentence']['sent_num']
            text_info['grammar_sent_num'] = data['summary']['grammar']['sent_num']
            # Count stories
            for text in data['text']:
                if text['type'] != 'Sentence' and \
                    text['type'] != 'WordClass':    # WordClass no data available as 2023-01-25
                    text_info['story_num'] += 1
        
        return text_info['story_num'], text_info['sentence_num'], \
            text_info['grammar_sent_num'], text_info['word_class_sent_num']


    def generate_sentence(self):
        info = {}
        for lang_en, lang_zh in self.LANG.items():
            info[lang_zh] = self.get_lang_textnum(lang_en)
        langs = list(info.keys())

        sent1 = f"目前語料庫中已建置**{'**、**'.join(langs[:-1])}**以及**{langs[-1]}**資料庫。"
        sent2 = '；'.join( f"{k}有 {v[0]} 筆口述語料、{v[1]} 句例句語料、文法書 {v[2]} 句例句及詞類專書 {v[3]} 句例句" for k, v in info.items() ) + '。'
        
        return sent1 + sent2
    

    def generate_sentence_en(self):
        info = {}
        for lang_en, lang_zh in self.LANG.items():
            info[lang_en.capitalize()] = self.get_lang_textnum(lang_en)
        langs = list(info.keys())

        sent1 = f"Currently, the corpus contains data collected from {len(langs)} different languages: **{'**, **'.join(langs[:-1])}**, and **{langs[-1]}**. "
        # info = list(info.items())
        
        sent2 = '; '.join( f"{v[0]} texts with audio recordings  (TWAs), {v[1]} elicited sentences, {v[2]} example sentences from Grammar Books, and {v[3]} sentences from Word Class Books were collected for {k}" for k, v in info.items() ) + '.'

        # k, v = info[0]
        # sent2_0 = f"{int_to_en(v[0]).capitalize()} texts with audio recordings (TWAs) and {v[1]} elicited sentences were collected for {k}, "
        
        # sent2 = ', '.join( f"{v[0]} TWAs and {v[1]} elicited sentences" for k, v in info[1:-1])

        # k, v= info[-1]
        # sent2_n = ', and ' + f"{f'{v[0]} TWAs' if v[0] != 0 else ''}{' and ' if v[0] != 0 and v[1] != 0 else ''}{f'{v[1]} elicited sentences' if v[1] != 0 else ''} for {k}."
        
        #return sent1 + sent2_0 + sent2 + sent2_n
        return sent1 + sent2
    

    def insert_corpus_info(self, md, en=False):
        sentence = self.generate_sentence_en() if en else self.generate_sentence()
        return md.replace(self.anchor, sentence)



def int_to_en(num):
    """From Stackoverflow
    https://stackoverflow.com/questions/8982163/how-do-i-tell-python-to-convert-integers-into-words/32640407#answer-32640407
    """
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)

    raise AssertionError('num is too large: %s' % str(num))