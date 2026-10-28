from lib import flags
def phrase_w(lines=[]):
    config = {}
    for line in lines:
        if " : " in line:
            a = line.split(" : ")
            if len(a) == 2:
                key = a[0].lstrip().rstrip().lstrip(" ").rstrip(" ")
                if "@!;@" in a[1]:
                    val = a[1].lstrip().rstrip().lstrip(" ").rstrip(" ").split("@!;@")
                else:
                    val = a[1].lstrip().rstrip().lstrip(" ").rstrip(" ")
                config[key] = val
            else:
                flags.raiseflag("PhraseError")
        else:
            flags.raiseflag("PhraseError")
    if not flags.getflag("PhraseError"):
        return config
    else:
        return {}
