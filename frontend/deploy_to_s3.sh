#!/bin/sh

file_list=(
    css/font-awesome.css
    css/shoelace.css
    css/styles.css
    axios.min.js
    identity_pool.js
    jquery.js
    voice-translator-config.js
    voice-translator.html
    voice-translator.js
)

bucket_name="voice-translator-translatorbucket-kvuovdlq7o4a"

for file in "${file_list[@]}"; do
    aws s3 cp $file s3://${bucket_name}/$file --acl public-read
done