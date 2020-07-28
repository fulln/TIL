
import re

filepath = "{leetcoded => leetcode}/easy/removeDuplicates.md"
patt = re.compile(r'=>(.*?)}', re.S)  #最小匹配
new_value = re.findall(patt,filepath)
filepath = re.sub('{(.*?)}',new_value[0].replace(' ', ''),filepath,1)

print(filepath)