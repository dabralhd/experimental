#!/usr/bin/env python3
"""Quick script to fetch and display the user's STAIoT Craft projects."""
import asyncio
from server_async import fetch_usr_prj_list

async def main():
    print("Fetching your STAIoT Craft projects...")
    projects = await fetch_usr_prj_list()
    
    if projects:
        print(f"\nFound {len(projects)} project(s):\n")
        for i, project_name in enumerate(projects, 1):
            print(f"  {i}. {project_name}")
    else:
        print("\nNo projects found in your workspace.")

if __name__ == "__main__":
    asyncio.run(main())


