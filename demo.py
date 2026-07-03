#!/usr/bin/env python3
"""
Demo Script for URL Shortener AI Copilot

This script demonstrates all features of the URL Shortener API:
- Creating short URLs
- Redirecting to original URLs  
- Viewing analytics
- Testing the Copilot console

Run with: python demo.py
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_TIMEOUT = 5

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.END}\n")

def print_subsection(text: str):
    """Print a subsection header"""
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")

def print_success(text: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print an error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_json(data: Dict[str, Any]):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def check_health() -> bool:
    """Check if the API is running"""
    print_header("Step 1: Health Check")
    print_subsection("Checking if API is running...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        print_success(f"API is healthy!")
        print_info(f"Status: {data.get('status')}")
        print_info(f"Version: {data.get('version')}")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Make sure the backend is running on port 8000")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def demo_create_short_url() -> Dict[str, Any]:
    """Demo: Create a short URL with auto-generated code"""
    print_header("Step 2: Create Short URL (Auto-Generated Code)")
    
    url_data = {
        "original_url": "https://www.python.org/dev/peps/pep-0008/",
        "custom_alias": None
    }
    
    print_subsection("Request Data:")
    print(f"Original URL: {url_data['original_url']}")
    print(f"Custom Alias: {url_data['custom_alias']} (None = auto-generate)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/shorten",
            json=url_data,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        
        print_success("Short URL created!")
        print_subsection("\nResponse:")
        print_json(result)
        
        return result
    except Exception as e:
        print_error(f"Failed to create short URL: {str(e)}")
        return {}

def demo_create_custom_alias() -> Dict[str, Any]:
    """Demo: Create a short URL with custom alias"""
    print_header("Step 3: Create Short URL (Custom Alias)")
    
    url_data = {
        "original_url": "https://github.com/sai12334/url-shortener-ai-copilot",
        "custom_alias": "copilot-demo"
    }
    
    print_subsection("Request Data:")
    print(f"Original URL: {url_data['original_url']}")
    print(f"Custom Alias: {url_data['custom_alias']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/shorten",
            json=url_data,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        
        print_success("Short URL created with custom alias!")
        print_subsection("\nResponse:")
        print_json(result)
        
        return result
    except Exception as e:
        print_error(f"Failed to create short URL: {str(e)}")
        return {}

def demo_simulate_clicks(short_code: str, num_clicks: int = 3):
    """Demo: Simulate multiple clicks on a short URL"""
    print_header(f"Step 4: Simulate {num_clicks} Clicks on Short Code: {short_code}")
    
    print_subsection(f"Simulating {num_clicks} clicks with delays...")
    
    for i in range(1, num_clicks + 1):
        try:
            print_info(f"Click {i}/{num_clicks}...", end=" ")
            response = requests.get(
                f"{BASE_URL}/{short_code}",
                timeout=API_TIMEOUT,
                allow_redirects=False
            )
            
            if response.status_code == 307:
                print_success("Click recorded")
                print_info(f"  Redirects to: {response.headers.get('location')}")
            else:
                print_error(f"Unexpected status code: {response.status_code}")
            
            time.sleep(0.5)  # Small delay between clicks
        except Exception as e:
            print_error(f"Click failed: {str(e)}")

def demo_get_analytics(short_code: str) -> Dict[str, Any]:
    """Demo: Get analytics for a short URL"""
    print_header(f"Step 5: Get Analytics for: {short_code}")
    
    print_subsection("Fetching analytics...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/analytics/{short_code}",
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        
        print_success("Analytics retrieved!")
        print_subsection("\nAnalytics Data:")
        print_json(result)
        
        return result
    except Exception as e:
        print_error(f"Failed to get analytics: {str(e)}")
        return {}

def demo_copilot_analyze() -> Dict[str, Any]:
    """Demo: Use the Copilot console to analyze a requirement"""
    print_header("Step 6: Copilot Console - Requirement Analysis")
    
    requirement = "Build a scalable URL shortener service with APIs, persistence, and analytics."
    
    print_subsection("Request Data:")
    print(f"Requirement: {requirement}")
    
    payload = {
        "requirement": requirement,
        "context": {
            "project_type": "web-api",
            "target_users": "engineers",
            "timeframe": "2 weeks"
        }
    }
    
    try:
        print_subsection("\nSending to Copilot engine...")
        response = requests.post(
            f"{BASE_URL}/copilot/analyze",
            json=payload,
            timeout=10  # Copilot analysis may take longer
        )
        response.raise_for_status()
        result = response.json()
        
        print_success("Copilot analysis complete!")
        
        print_subsection("\nAnalysis Components:")
        if "requirement_analysis" in result:
            print(f"\n{Colors.BLUE}Requirement Analysis:{Colors.END}")
            print_json(result["requirement_analysis"])
        
        if "task_decomposition" in result:
            print(f"\n{Colors.BLUE}Task Decomposition:{Colors.END}")
            print_json(result["task_decomposition"])
        
        if "engineering_artifacts" in result:
            print(f"\n{Colors.BLUE}Engineering Artifacts:{Colors.END}")
            print_json(result["engineering_artifacts"])
        
        if "validation_report" in result:
            print(f"\n{Colors.BLUE}Validation Report:{Colors.END}")
            print_json(result["validation_report"])
        
        if "risk_analysis" in result:
            print(f"\n{Colors.BLUE}Risk Analysis:{Colors.END}")
            print_json(result["risk_analysis"])
        
        if "final_summary" in result:
            print(f"\n{Colors.BLUE}Final Summary:{Colors.END}")
            print_json(result["final_summary"])
        
        return result
    except Exception as e:
        print_error(f"Copilot analysis failed: {str(e)}")
        return {}

def print_summary():
    """Print a summary of the demo"""
    print_header("Demo Complete!")
    
    summary = f"""
{Colors.GREEN}✓ All demonstrations completed successfully!{Colors.END}

What you just saw:
  1. Health check - API is running and accessible
  2. Short URL creation with auto-generated code
  3. Short URL creation with custom alias
  4. Simulated clicks on short URLs
  5. Analytics tracking and retrieval
  6. Copilot console requirement analysis

Key Takeaways:
  • Short URLs can be generated automatically or with custom aliases
  • Each click on a short URL is tracked in the database
  • Analytics show total clicks and last-clicked timestamp
  • Copilot console provides structured requirement analysis
  • All components work together as a cohesive system

Next Steps:
  1. Explore the frontend at http://localhost:5173
  2. Try the Live Demo tab for interactive testing
  3. Read DEMO_GUIDE.md for more scenarios
  4. Check GitHub: https://github.com/sai12334/url-shortener-ai-copilot

Need help? Check README.md or ARCHITECTURE.md for more details.
"""
    print(summary)

def main():
    """Run all demos"""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║   URL Shortener AI Copilot - Complete Feature Demo               ║")
    print("║   Repository: github.com/sai12334/url-shortener-ai-copilot       ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Check if API is running
    if not check_health():
        print_error("Cannot proceed without a running API")
        print_info("Start the backend with: python -m uvicorn app.main:app --reload --port 8000")
        return
    
    # Create short URLs
    auto_url = demo_create_short_url()
    if not auto_url:
        print_error("Failed to create first short URL. Cannot continue demo.")
        return
    
    custom_url = demo_create_custom_alias()
    if not custom_url:
        print_error("Failed to create second short URL. Cannot continue demo.")
        return
    
    # Simulate clicks
    short_code1 = auto_url.get("short_code")
    short_code2 = custom_url.get("short_code")
    
    if short_code1:
        demo_simulate_clicks(short_code1, 5)
    
    if short_code2:
        demo_simulate_clicks(short_code2, 3)
    
    # Get analytics
    if short_code1:
        demo_get_analytics(short_code1)
    
    if short_code2:
        demo_get_analytics(short_code2)
    
    # Copilot analysis (optional - may take longer)
    try:
        demo_copilot_analyze()
    except Exception as e:
        print_error(f"Copilot demo skipped: {str(e)}")
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user{Colors.END}")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
