#!/bin/bash
# This script escapes all curly brackets between <style></style> tags
# in order to be safe for python format.

sed '
/<style/,/<\/style/ s/{/{{/g;
/<style/,/<\/style/ s/}/}}/g;
/<style/,/<\/style/ s/{\({[a-zA-Z0-9_][a-zA-Z0-9_]*}\)}/\1/g;
' "$@"


