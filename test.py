import re
text = '<cite>gs.<strong>hubu.edu.cn</strong></cite>'
link_regx = re.compile('<cite>(.*?)<strong>hubu.edu.cn</strong></cite>')
links = link_regx.findall(text)
print(links)