from json import load
import re
import yaml


class 轉到臺灣言語資料庫:
    萌典檔名 = 'dict-amis-mp.json'
    目標檔名 = 'dict-amis-mp.yaml'

    def 轉成資料庫yaml(self):
        全部資料 = {
            '來源': {'名': '世光神父 (Maurice Poinsot) 及博利亞神父 (Louis Pourrias)',
                   '書名': ' Dictionnaire Amis-Français',
                   '教會': "Missions Etrangères de Paris",
                   },
            '版權': 'Creative Commons 姓名標示-非商業性 3.0 Unported License',
            '著作所在地': '花蓮鐵份部落',
            '著作年': '1996',
            '語言腔口': '阿美語',
                    '種類': '字詞',
            '相關資料組': [],

        }
        相關資料組 = 全部資料['相關資料組']
        for 族語, 法語 in self.整理族語華語對齊詞條():
            if 法語:
                這筆資料 = {
                    '外語語言': '法語',
                    '外語資料': 法語,
                    '下層': [{'文本資料': 族語}],
                }
            else:
                這筆資料 = {'文本資料': 族語}
            相關資料組.append(這筆資料)
        with open(self.目標檔名, 'w') as 檔案:
            yaml.dump(全部資料, 檔案, default_flow_style=False, allow_unicode=True)

    def 整理族語華語對齊詞條(self):
        '''
            "def":
        "definitions":
    "heteronyms":
            "synonyms":
    "title":
'''
        with open(self.萌典檔名) as 檔案:
            for 一筆族語 in load(檔案):
                族語 = 一筆族語['title']
                for heteronym in 一筆族語['heteronyms']:
                    for definition in heteronym['definitions']:
                        for 結果 in self._definitions(族語, definition):
                            yield 結果

    def _definitions(self, 族語, definition):
        try:
            法語詞義 = definition['def']
            yield 族語, 法語詞義
        except KeyError:
            yield 族語, None
        try:
            synonyms = definition.pop('synonyms')
        except KeyError:
            pass
        else:
            for synonym in synonyms:
                for 結果 in self._definitions(synonym, definition):
                    yield 結果

for 結果 in 轉到臺灣言語資料庫().整理族語華語對齊詞條():
    print(結果)

轉到臺灣言語資料庫().轉成資料庫yaml()
