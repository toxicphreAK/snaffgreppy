from re import compile

SNAFF_RE = compile(r"^\[(?P<execution_system>).*\] (?P<found_timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}Z) \[(?P<found_type>.*)\] \{(?P<found_rating>.*)\}\<(?P<found_details>.*)\>\((?P<found_path>.*)\) (?P<found_content>.*)")
FILENAME_RE = compile(r"^([a-zA-Z0-9\s_\\.\-\(\):])+.\w*$")
PASS_RE = compile(r"[Pp][aA][sS][sS]([wW][oO][rR][dD])*|[Pp][wW][dD]")
# net use [devicename]: [path] [/user:"\domain\user"] [password] [/persistent:no]
# NETUSE_RE = compile(r"net use (?P<devicename>[\w|\*|LPT\d]:)? (?P<path>([ ]+\"(\.\/|\.\.\/|\/)?[^\/\"]+(\/[^\/\"]+)+\"[ ]+|[ ]+(\.\/|\.\.\/|\/)?[^\/\s]+(\/[^\/\s]+)+[ ]+)) (?P<user>/user:(?P<domain>[\w.]*?)\\(?P<username>.*?)) (?P<password>.*?)( /persistent:[no|yes])?")
NETUSE_RE = compile(r"net use (?P<devicename>(\w|\*|LPT\d):?) (?P<path>\\\\?.*?)(( (?P<user>/user:((?P<domain>[\w.]*)\\)?(?P<username>\S*)))|( /(p(ersistent)?|P(ERSISTENT)?):(no|NO|yes|YES))|( (?P<password>(?!/)\S*))|( /(delete|DELETE))|( /(savecred|SAVECRED))|( /(smartcard|SMARTCARD)))+")
URL_RE = compile(r"https?:\/\/(www\\*\.)?[-a-zA-Z0-9@:%\\._\+~#=$]{1,256}\\*\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+\\.~#?&//=]*)")
FILENAMEONLY_RE = compile(r"^(\w)*\.\w+$")
