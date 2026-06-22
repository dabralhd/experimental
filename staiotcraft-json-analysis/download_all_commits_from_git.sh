# /bin/sh
# 1. Create a target directory outside your Git repo to avoid clutter
mkdir -p ../file_history

# 2. Loop through every commit hash that modified this specific file
git log --follow --format=%H -- "path/to/your/file.txt" | while read -r hash; do
    # Get the short commit hash and commit date for clean naming
    short_hash=$(git rev-parse --short "$hash")
    commit_date=$(git log -1 --format=%cd --date=format:'%Y%m%d_%H%M%S' "$hash")
    
    # Extract the file at that specific commit and save it
    git show "${hash}:path/to/your/file.txt" > "../file_history/${commit_date}_${short_hash}_file.txt" 2>/dev/null
done
