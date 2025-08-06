#!/usr/bin/env python3
"""
Script to ping STAIoT Craft online tool and check connectivity.
"""

import httpx
import json
import time
from datetime import datetime

# STAIoT Craft API configuration
BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3"
BEARER_TOKEN = "eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiZDk4OTE1MzgtMjcyYy00NWM2LWFmNzQtZjJhN2UyNjI4ZjcyIiwiZXZlbnRfaWQiOiI1NWNmY2UxNi03ZWMzLTQzZWEtYTMyMi03ODQ3Nzg3YTgwMzEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTMyMDU4MDIsImV4cCI6MTc1MzI5MjIwMiwiaWF0IjoxNzUzMjA1ODAyLCJqdGkiOiI4NmMzMzA5ZS02NDhjLTQ5ZDAtOTIyMS0wYjJjODcwOWU5Y2UiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kC0g3NSSUdMxRyjW6Bav-c-aibndM7T_3ayqxUd-KFA5hkFZHbwr7aCcTgYNdKz7Gt5EL0GWPr2Pq3Vn2HstJ6O_mglyquNWP-z_RjM9v59sKsDY-VtrnhcsZ7h3o_VQB9EvFdwq0f5AEYQJnrqHhQWicsjbn400EOVEraYti7oeX-oiyD8_FpPFbbqSBGBgHD9Du3SDBLQDyDylykGCo0mofr9G6iRq-uIkdElUwabTweX-sbDg_1fR6ejYkmJsHVH-KwpKxdS6rkoWss8cl8T1sWk5bcw2QGpn53_L2QAXrBRjI_J1zBNMAZirDeVm952zc0ZURB-qljm0-tkxXg"

def get_headers(token):
    """Construct HTTP headers for API requests."""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

def ping_staiotcraft():
    """Ping STAIoT Craft online tool and check connectivity."""
    print(f"🔍 Pinging STAIoT Craft online tool...")
    print(f"📍 Target URL: {BASE_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Test endpoints to check
    endpoints_to_test = [
        ("/templates/projects", "Template Projects"),
        ("/projects", "User Projects"),
        ("/", "Root Endpoint")
    ]
    
    results = []
    
    for endpoint, description in endpoints_to_test:
        url = f"{BASE_URL}{endpoint}"
        print(f"🔗 Testing {description} endpoint...")
        
        try:
            start_time = time.time()
            
            with httpx.Client(timeout=30.0) as client:
                response = client.get(
                    url, 
                    headers=get_headers(BEARER_TOKEN),
                    follow_redirects=True
                )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            status = "✅ SUCCESS" if response.status_code == 200 else f"⚠️  HTTP {response.status_code}"
            
            print(f"   Status: {status}")
            print(f"   Response Time: {response_time:.2f}ms")
            print(f"   URL: {url}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"   Data: {len(data)} items returned")
                    elif isinstance(data, dict):
                        print(f"   Data: {len(data)} keys in response")
                    else:
                        print(f"   Data: {type(data).__name__} returned")
                except json.JSONDecodeError:
                    print(f"   Data: Non-JSON response ({len(response.content)} bytes)")
            else:
                print(f"   Error: {response.text[:100]}...")
            
            results.append({
                "endpoint": description,
                "status": "SUCCESS" if response.status_code == 200 else f"HTTP_{response.status_code}",
                "response_time": response_time,
                "url": url
            })
            
        except httpx.ConnectError as e:
            print(f"   Status: ❌ CONNECTION ERROR")
            print(f"   Error: {str(e)}")
            results.append({
                "endpoint": description,
                "status": "CONNECTION_ERROR",
                "response_time": None,
                "url": url,
                "error": str(e)
            })
            
        except httpx.TimeoutException as e:
            print(f"   Status: ⏰ TIMEOUT")
            print(f"   Error: Request timed out after 30 seconds")
            results.append({
                "endpoint": description,
                "status": "TIMEOUT",
                "response_time": None,
                "url": url,
                "error": "Request timed out"
            })
            
        except Exception as e:
            print(f"   Status: ❌ UNEXPECTED ERROR")
            print(f"   Error: {str(e)}")
            results.append({
                "endpoint": description,
                "status": "UNEXPECTED_ERROR",
                "response_time": None,
                "url": url,
                "error": str(e)
            })
        
        print()
    
    # Summary
    print("📊 SUMMARY")
    print("-" * 60)
    
    successful = sum(1 for r in results if r["status"] == "SUCCESS")
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("🎉 All endpoints are accessible!")
    elif successful > 0:
        print("⚠️  Some endpoints are accessible, some are not.")
    else:
        print("💥 No endpoints are accessible. Check your connection and credentials.")
    
    print("\n📋 Detailed Results:")
    for result in results:
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        response_time_str = f"{result['response_time']:.2f}ms" if result["response_time"] else "N/A"
        print(f"   {status_icon} {result['endpoint']}: {result['status']} ({response_time_str})")
    
    return results

def test_specific_endpoints():
    """Test specific STAIoT Craft endpoints."""
    print("\n🔧 Testing Specific Endpoints")
    print("-" * 60)
    
    # Test template projects endpoint specifically
    url = f"{BASE_URL}/templates/projects"
    print(f"🎯 Testing template projects endpoint: {url}")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=get_headers(BEARER_TOKEN))
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS: Found {len(data)} template projects")
                
                if data:
                    print("📋 Available template projects:")
                    for i, project in enumerate(data[:5], 1):  # Show first 5
                        name = project.get('ai_project_name', 'Unknown')
                        desc = project.get('description', 'No description')
                        print(f"   {i}. {name}: {desc[:50]}...")
                    
                    if len(data) > 5:
                        print(f"   ... and {len(data) - 5} more projects")
                else:
                    print("   No template projects found")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 STAIoT Craft Online Tool Ping Test")
    print("=" * 60)
    
    # Run the ping test
    results = ping_staiotcraft()
    
    # Test specific endpoints
    test_specific_endpoints()
    
    print("\n🏁 Ping test completed!") 