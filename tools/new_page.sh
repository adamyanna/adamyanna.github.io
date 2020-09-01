#!/bin/bash
if [ -z $1 ]; then
    echo "Pls input file_name as arg!"
    exit 1
fi

post_file_name="`date +%Y-%m-%d`-$1"
cat >> $(dirname $0)/../_posts/$post_file_name.md << EOF
---
title: $1 
author: Teddy
date: $(date +%Y-%m-%d) $(date +%H:%M:%S) +0800
categories: []
tags: []
---
EOF

echo "New post create file name $post_file_name"
