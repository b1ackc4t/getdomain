import re

f = open("source.txt", 'r', encoding='UTF-8')
# text = f.read()
text = 'kwejlw.dfa.sfw.hgw___asd__ewl.fjwhefwejwh.dfdsdbaidu.com，..baidu.com , sadf.baidu.com'
str1 = 'baidu.com'
# $ 是整行匹配，所以是以它为结尾的意思 同理。 ^py& 意思为整行匹配
# \w\d\s [特殊字符]
# *.+?  {n,m}
# r 取消\ 转义符的转义, 把\当做单独的字符,就不会转义\n 使得字符串为原生字符串，使用它自己的规则
res_access = r'[0-9a-zA-ZA-ZA-Z\\_.]+' + r'[.]' + str1
domains = re.findall(res_access, text)
print(domains)
