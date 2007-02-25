#!/bin/sh
# Parse /etc/mime.types into nginx config format.
# Copyright (c) 2007 Elan Ruusamäe <glen@pld-linux.org>

mimetypes="$1"

# header
cat > mime.types <<EOF
# mimetype mapping
types {
EOF

# build mime.types from system mime.types
# get ones with extension
awk '!/^#/ && $2 { print } ' $mimetypes | \
# sort it \
LC_ALL=C sort -u | \
# build conf fragment
awk '{ printf("\t%-40s %s;\n", $1, $2)}' \
	>> mime.types

# footer
cat >> mime.types <<EOF
}
EOF
