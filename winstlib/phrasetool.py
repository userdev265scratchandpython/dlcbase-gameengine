# Phraser tool module.
# This module's whole purpose is to phrase the game config.
# The config must be in expected format:
# Key : Value
# or
# Key : Value1@!;@Value2
# The second option is a list while the first is a string.

# Below are the imports.

from winstlib import flags

# Below is the code to phrase stuff.

def phrase_w(lines: list = []) -> dict:
    """
    Phraze a Winst config style config.

    Args:
        lines: Lines of the configuration file.

    Returns:
        Configuration keys and values.

    """
    config = {}
    for line in lines:
        if " : " in line:
            # Split key and value(s).
            a = line.split(" : ")
            # Make sure the line is not malformed.
            if len(a) == 2:
                # Get the key.
                key = a[0].lstrip().rstrip().lstrip(" ").rstrip(" ")
                # Value list and string handling.
                if "@!;@" in a[1]:
                    # List handling.
                    val = a[1].lstrip().rstrip().lstrip(" ").rstrip(" ").split("@!;@")
                else:
                    # String handing.
                    val = a[1].lstrip().rstrip().lstrip(" ").rstrip(" ")
                # Avoid overriding an existing key.
                if key not in config:
                    config[key] = val
                else:
                    print("Duplicate key, avoiding override")
            else:
                # Raise the phrasing error flag if configuration is malformed.
                flags.raiseflag("PhraseError")
        else:
            # Avoid treating a comment as an error.
            if not line.startswith("# "):
                # Avoid treating empty lines as errors.
                if len(line) > 2:
                    # Raise an error on malformed config.
                    flags.raiseflag("PhraseError")
    # Make sure no errors happened or return blank configuration to aviod errors.
    if not flags.getflag("PhraseError"):
        return config
    else:
        return {}
