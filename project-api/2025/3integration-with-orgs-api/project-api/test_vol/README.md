This folder is meant to be a test folder which will contain contents in the following folder structure:
```
- project_api_data_test_folder/
    - artifacts/
        - get-started-projects/
            - get_started-asset_tracking_mlc/  "*" 
        - .assets/ "*"
    - local/
        - workspace/
            - <$test-user-uuid>/  "#"
```
- #### Note: we need to change the ownership of the directory local/workspace to 9001:9001 (user:group) before starting to use it.
- #### "*" (needs to be copied from vespucci-artifacts)
- #### "#" use <$test-user-id> "00000000-0000-0000-0000-000000000000"