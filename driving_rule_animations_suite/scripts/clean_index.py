path = 'C:/tx_dmv/driving_rule_animations_suite/index.html'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

dup = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\n            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">'
single = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">'
if dup in t:
    t = t.replace(dup, single)
    print('Replaced LF duplicate')
else:
    dup_crlf = '<tr class="hover:bg-[#181F2B] bg-emerald-500/5">\r\n            <tr class="hover:bg-[#181F2B] bg-emerald-500/5">'
    if dup_crlf in t:
        t = t.replace(dup_crlf, single)
        print('Replaced CRLF duplicate')

with open(path, 'w', encoding='utf-8') as f:
    f.write(t)
