#!/usr/bin/env python3
"""
WealthFlow Agent - Integration Test Suite
Tests the complete system integration and functionality.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Test configuration
API_BASE_URL = "http://localhost:5000/api/wealthflow"
FRONTEND_URL = "http://localhost:5173"

class WealthFlowIntegrationTest:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def log_test(self, test_name, success, message=""):
        """Log test result."""
        status = "PASS" if success else "FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        if success:
            self.passed += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.failed += 1
            print(f"❌ {test_name}: {status} - {message}")
    
    def test_api_health(self):
        """Test API health endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("API Health Check", True)
                    return True
                else:
                    self.log_test("API Health Check", False, "API returned success=False")
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("API Health Check", False, str(e))
        return False
    
    def test_portfolio_endpoint(self):
        """Test portfolio data endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/portfolio", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    portfolio = data["data"]
                    required_fields = ["account_info", "positions"]
                    if all(field in portfolio for field in required_fields):
                        self.log_test("Portfolio Endpoint", True)
                        return True
                    else:
                        self.log_test("Portfolio Endpoint", False, "Missing required fields")
                else:
                    self.log_test("Portfolio Endpoint", False, "Invalid response format")
            else:
                self.log_test("Portfolio Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Portfolio Endpoint", False, str(e))
        return False
    
    def test_opportunities_endpoint(self):
        """Test opportunities endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/opportunities", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    opportunities = data["data"]
                    if isinstance(opportunities, list) and len(opportunities) > 0:
                        # Check if opportunities have required fields
                        required_fields = ["symbol", "type", "score", "current_price"]
                        first_opp = opportunities[0]
                        if all(field in first_opp for field in required_fields):
                            self.log_test("Opportunities Endpoint", True)
                            return True
                        else:
                            self.log_test("Opportunities Endpoint", False, "Missing required fields in opportunities")
                    else:
                        self.log_test("Opportunities Endpoint", False, "No opportunities returned")
                else:
                    self.log_test("Opportunities Endpoint", False, "Invalid response format")
            else:
                self.log_test("Opportunities Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Opportunities Endpoint", False, str(e))
        return False
    
    def test_alerts_endpoint(self):
        """Test alerts endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/alerts", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    alerts = data["data"]
                    if isinstance(alerts, list):
                        self.log_test("Alerts Endpoint", True)
                        return True
                    else:
                        self.log_test("Alerts Endpoint", False, "Alerts data is not a list")
                else:
                    self.log_test("Alerts Endpoint", False, "Invalid response format")
            else:
                self.log_test("Alerts Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Alerts Endpoint", False, str(e))
        return False
    
    def test_strategies_endpoint(self):
        """Test strategies endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/strategies", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    self.log_test("Strategies Endpoint", True)
                    return True
                else:
                    self.log_test("Strategies Endpoint", False, "Invalid response format")
            else:
                self.log_test("Strategies Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Strategies Endpoint", False, str(e))
        return False
    
    def test_monitoring_status(self):
        """Test monitoring status endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/monitoring/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    status = data["data"]
                    required_fields = ["running", "monitored_stocks", "monitored_cryptos"]
                    if all(field in status for field in required_fields):
                        self.log_test("Monitoring Status", True)
                        return True
                    else:
                        self.log_test("Monitoring Status", False, "Missing required fields")
                else:
                    self.log_test("Monitoring Status", False, "Invalid response format")
            else:
                self.log_test("Monitoring Status", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Monitoring Status", False, str(e))
        return False
    
    def test_daily_report(self):
        """Test daily report endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/reports/daily", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    report = data["data"]
                    required_fields = ["date", "top_opportunities", "market_sentiment"]
                    if all(field in report for field in required_fields):
                        self.log_test("Daily Report", True)
                        return True
                    else:
                        self.log_test("Daily Report", False, "Missing required fields")
                else:
                    self.log_test("Daily Report", False, "Invalid response format")
            else:
                self.log_test("Daily Report", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Daily Report", False, str(e))
        return False
    
    def test_news_endpoint(self):
        """Test news endpoint."""
        try:
            response = requests.get(f"{API_BASE_URL}/news", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "data" in data:
                    news = data["data"]
                    if isinstance(news, list):
                        self.log_test("News Endpoint", True)
                        return True
                    else:
                        self.log_test("News Endpoint", False, "News data is not a list")
                else:
                    self.log_test("News Endpoint", False, "Invalid response format")
            else:
                self.log_test("News Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("News Endpoint", False, str(e))
        return False
    
    def test_signal_execution(self):
        """Test signal execution endpoint."""
        try:
            test_signal = {
                "symbol": "AAPL",
                "action": "buy",
                "quantity": 1,
                "price": 150.0,
                "order_type": "market",
                "strategy": "test_strategy"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/execute-signal",
                json=test_signal,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Signal Execution", True)
                    return True
                else:
                    self.log_test("Signal Execution", False, "Execution failed")
            else:
                self.log_test("Signal Execution", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Signal Execution", False, str(e))
        return False
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible."""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                if "WealthFlow" in response.text:
                    self.log_test("Frontend Accessibility", True)
                    return True
                else:
                    self.log_test("Frontend Accessibility", False, "WealthFlow not found in response")
            else:
                self.log_test("Frontend Accessibility", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Accessibility", False, str(e))
        return False
    
    def run_all_tests(self):
        """Run all integration tests."""
        print("🚀 Starting WealthFlow Agent Integration Tests")
        print("=" * 60)
        
        # API Tests
        print("\n📡 Testing API Endpoints:")
        self.test_api_health()
        self.test_portfolio_endpoint()
        self.test_opportunities_endpoint()
        self.test_alerts_endpoint()
        self.test_strategies_endpoint()
        self.test_monitoring_status()
        self.test_daily_report()
        self.test_news_endpoint()
        self.test_signal_execution()
        
        # Frontend Tests
        print("\n🖥️  Testing Frontend:")
        self.test_frontend_accessibility()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary:")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed == 0:
            print("\n🎉 All tests passed! WealthFlow Agent is ready for deployment.")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Please check the issues above.")
        
        return self.failed == 0

def main():
    """Main test function."""
    print("WealthFlow Agent - Integration Test Suite")
    print("Testing system integration and API functionality...")
    
    # Wait a moment for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(2)
    
    # Run tests
    tester = WealthFlowIntegrationTest()
    success = tester.run_all_tests()
    
    # Save test results
    with open("integration_test_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "passed": tester.passed,
                "failed": tester.failed,
                "success_rate": tester.passed / (tester.passed + tester.failed) * 100
            },
            "results": tester.test_results
        }, f, indent=2)
    
    print(f"\n📄 Test results saved to: integration_test_results.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

