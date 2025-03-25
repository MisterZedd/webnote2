#!/usr/bin/python3

import urllib.parse

# Function to decode URL-encoded text
def decode(text):
    try:
        # Try to decode URL encoding
        decoded = urllib.parse.unquote_plus(text)
        return decoded
    except:
        # Return original if decoding fails
        return text
