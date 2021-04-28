from xpinyin import Pinyin

p = Pinyin()
result1 = p.get_pinyin('baidu')
s = result1.split('-')
flag = [s[i][0] for i in range(len(s))]
flag = ''.join(flag)
print(flag)