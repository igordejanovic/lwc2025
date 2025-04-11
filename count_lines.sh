#!/bin/sh
cloc --read-lang-def=textx-cloc-defs.txt ./textx-lang-ql/questlang
cloc ./textx-gen-ql-web/qlweb --include-lang=python,jsx,"jinja template",javascript,typescript,html

#scc --count-as tx:C ./textx-lang-ql/questlang --include-ext py,tx
#scc ./textx-gen-ql-web/qlweb --include-ext py,jsx,tsx,ts,js,jinja,html
