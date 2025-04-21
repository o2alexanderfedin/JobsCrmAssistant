#!/usr/bin/env python3
import os

frontmatter = """---
description: "Standards for implementing internationalization across the application"
globs: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", 
        "locales/**/*"]
alwaysApply: false
---

"""

file_path = ".cursor/rules/270-internationalization.mdc"

try:
    # Verify file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        exit(1)
        
    # Read the current content
    with open(file_path, "r") as f:
        content = f.read()
        print(f"Read {len(content)} characters from file")
    
    # Add frontmatter
    new_content = frontmatter + content
    print(f"New content has {len(new_content)} characters")
    
    # Write the file
    with open(file_path, "w") as f:
        f.write(new_content)
        print(f"Wrote {len(new_content)} characters to file")
    
    # Verify the write was successful
    with open(file_path, "r") as f:
        verify_content = f.read()
        if verify_content.startswith("---"):
            print("SUCCESS: Frontmatter added correctly")
        else:
            print("ERROR: Frontmatter wasn't added correctly")
            print(f"File begins with: {verify_content[:50]}...")
            
except Exception as e:
    print(f"Error: {str(e)}") 