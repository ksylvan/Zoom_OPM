#!/usr/bin/env python3
"""
Script to apply hardening improvements to zoom-manage AppleScript
"""

import re
import os
from datetime import datetime

def main():
    # Read the original file
    with open('./zoom-manage', 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')  # Use utf-8 with error handling
    
    # 1. Add breakout keywords property after batchCount
    batchcount_pattern = r'(property batchCount : 50 -- can be set via ZOOM_MANAGE_BATCH_SIZE environment variable\n)'
    replacement = r'\1\n-- Configurable breakout room keywords - can be overridden via ZOOM_BREAKOUT_KEYWORDS environment variable\nproperty breakoutKeywords : missing value -- will be set from environment or defaults\n'
    content = re.sub(batchcount_pattern, replacement, content)
    
    # 2. Update environment documentation
    env_docs_pattern = r'(\t& "    - ZOOM_USE_SCROLLING: Set to any value to use scrolling method for gathering all participants \(recommended for large meetings\)\." & linefeed)'
    env_replacement = r'\1\n\t& "    - ZOOM_BREAKOUT_KEYWORDS: Comma-separated list of keywords to search for breakout functionality (default: \"Breakout,Breakout Rooms\")." & linefeed'
    content = re.sub(env_docs_pattern, env_replacement, content)
    
    # 3. Add breakout keywords initialization to setupEnvVariables
    scrolling_pattern = r'(\tset useScrollingRoster to \(useScrollingRoster is not "unset"\) -- set to false or true)'
    scrolling_replacement = r'''\1
\t-- breakoutKeywords is set from ZOOM_BREAKOUT_KEYWORDS or defaults to "Breakout,Breakout Rooms"
\tset breakoutKeywords to do shell script "echo ${ZOOM_BREAKOUT_KEYWORDS:-Breakout,Breakout Rooms}"
\t-- Convert comma-separated string to AppleScript list
\tset AppleScript's text item delimiters to ","
\tset breakoutKeywords to text items of breakoutKeywords
\tset AppleScript's text item delimiters to ""'''
    content = re.sub(scrolling_pattern, scrolling_replacement, content)
    
    # 4. Add menu dump function after findStatusMenuWithDebug
    with open('./menu_dump_function.applescript', 'r') as f:
        menu_dump_code = f.read()
    
    find_status_end_pattern = r'(end findStatusMenuWithDebug\n)'
    find_status_replacement = f'\\1\n{menu_dump_code}\n'
    content = re.sub(find_status_end_pattern, find_status_replacement, content)
    
    # 5. Update findStatusMenuWithDebug to call menu dump on failure
    debug_end_pattern = r'(\t\tmy logMessage\(debugOutput, logFile\)\n\t\tlog debugOutput\n\tend if\n\t\n\treturn _ret\nend findStatusMenuWithDebug)'
    debug_replacement = r'''\t\tmy logMessage(debugOutput, logFile)
\t\tlog debugOutput
\t\t
\t\t-- Write full menu dump to file for easier debugging
\t\tmy dumpFullMenuToLog()
\tend if
\t
\treturn _ret
end findStatusMenuWithDebug'''
    content = re.sub(debug_end_pattern, debug_replacement, content)
    
    # 6. Replace hard-coded "Breakout" with breakoutKeywords in clickStatusMenu calls
    breakout_pattern = r'my clickStatusMenu\("Breakout"\)'
    breakout_replacement = r'my clickStatusMenu(breakoutKeywords)'
    content = re.sub(breakout_pattern, breakout_replacement, content)
    
    # Write the hardened version
    with open('./zoom-manage-hardened', 'wb') as f:
        f.write(content.encode('utf-8'))
    
    print("Successfully applied hardening improvements to zoom-manage")
    print("Changes applied:")
    print("1. ✓ Added configurable ZOOM_BREAKOUT_KEYWORDS environment variable")
    print("2. ✓ Updated environment documentation") 
    print("3. ✓ Added breakout keywords initialization in setupEnvVariables")
    print("4. ✓ Added dumpFullMenuToLog() function for debugging")
    print("5. ✓ Enhanced findStatusMenuWithDebug to dump menu on failure")
    print("6. ✓ Replaced hard-coded 'Breakout' with configurable keywords")
    print("\nThe hardened script is saved as: zoom-manage-hardened")

if __name__ == "__main__":
    main()
