#!/bin/bash

echo "Running mesh quality check..."

./bin/xcheck_quality_external_mesh << EOF
3
EOF

echo "Done."