import re


values = [
    "<#818849848941871146>",
    "<@!173583403055054848>",
    "<@&823987120900145173>,",
    "<#818849848941871147>",
    "<@!172002275412279296>",
    "weifwoeifrwe",
    "1231203810230123890123019"
]
for value in values:
    idStr = re.match(r"<.+?([0-9]+)>", value.strip())
    if idStr:
        print(idStr.groups()[0])
    else:
        print("No match")