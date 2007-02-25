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
awk '{
	m = $1;
	v = substr($0, length($1));
	x = substr(v, index(v, $2));
	gsub(/\t+/, " ", x);
	printf("\t%-40s %s;\n", m, x);
}' \
	>> mime.types

# footer
cat >> mime.types <<EOF
}
EOF
