#!/bin/bash

# Check if HTTP redirects to HTTPS
http_response=$(curl -s -o /dev/null -w "%{http_code}" http://example.com)
if [ "$http_response" -ne 301 ]; then
  echo "HTTP to HTTPS redirect failed"
  exit 1
fi

# Check if HTTPS returns the correct content
https_content=$(curl -s https://example.com)
if [[ "$https_content" != *"Hello World!"* ]]; then
  echo "Incorrect content served over HTTPS"
  exit 1
fi

echo "All tests passed"
exit 0
