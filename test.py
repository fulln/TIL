
import re

filepath = '"vim/vim\345\256\211\350\243\205fzf\347\255\211\350\277\233\351\230\266\346\217\222\344\273\266.md" => vim/vim_plugins_fzf.md'
patt = re.compile(r'=>(.*?)$', re.S)  #最小匹配
new_value = re.findall(patt,filepath)
filepath = re.sub('^.*$',new_value[0].replace(' ', ''),filepath,1)

print(filepath)