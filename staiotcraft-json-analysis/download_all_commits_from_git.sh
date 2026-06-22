# /bin/sh
# 1. Create a target directory outside your Git repo to avoid clutter
mkdir -p ../file_history
file_name="/Users/hemduttdabral/projects/vespucci-artifacts/projects/get_started_smart_asset_tracking_mlc/ai_get_started_smart_asset_tracking_mlc.json"
# 2. Loop through every commit hash that modified this specific file
git log --follow --format=%H -- "$file_name" | while read -r hash; do
    # Get the short commit hash and commit date for clean naming
    short_hash=$(git rev-parse --short "$hash")
    commit_date=$(git log -1 --format=%cd --date=format:'%Y%m%d_%H%M%S' "$hash")
    
    # Extract the file at that specific commit and save it
    git show "${hash}:$file_name" > "../file_history/${commit_date}_${short_hash}_$file_name" 2>/dev/null
done
