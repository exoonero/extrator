import re

regex = r'(\d{3})-?(\d{3})-?(\d{3})-?(\d{2})'
substitution = r'\1\2\3-\4'

text = '456-495-567-34 234345334-53234123234-23'
result = re.sub(regex, substitution, text)

print(result)