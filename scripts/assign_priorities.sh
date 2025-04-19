#!/bin/bash

# Ensure priority labels exist
if ! gh label list | grep -q "priority:high"; then
    gh label create "priority:high" -c "#FF0000" -d "High priority task that needs immediate attention"
fi

if ! gh label list | grep -q "priority:medium"; then
    gh label create "priority:medium" -c "#FFA500" -d "Medium priority task"
fi

if ! gh label list | grep -q "priority:low"; then
    gh label create "priority:low" -c "#008000" -d "Low priority task that can be addressed later"
fi

# Get issues without priority labels
issues=$(gh issue list --json number,title,body,labels --jq '.[] | select(([.labels[].name] | map(contains("priority:")) | any | not)) | .number')

for issue in $issues; do
    # Get issue details
    body=$(gh issue view $issue --json body --jq .body)
    
    # Apply priority based on keywords
    if echo "$body" | grep -iE "security|data|critical|urgent|blocking|incident|compliance" > /dev/null; then
        echo "Assigning high priority to issue #$issue"
        gh issue edit $issue --add-label "priority:high"
    elif echo "$body" | grep -iE "performance|integration|monitoring|api|cache|async" > /dev/null; then
        echo "Assigning medium priority to issue #$issue"
        gh issue edit $issue --add-label "priority:medium"
    else
        echo "Assigning low priority to issue #$issue"
        gh issue edit $issue --add-label "priority:low"
    fi
done

echo "Priority assignment complete!" 