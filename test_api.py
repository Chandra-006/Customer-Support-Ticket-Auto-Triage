"""
Simple test script for the API
Run this after starting the API server with: python app.py
"""
import requests
import json

API_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_predict():
    """Test the prediction endpoint"""
    print("Testing prediction endpoint...")
    
    test_cases = [
        "The app crashes when I try to open it",
        "I forgot my password and cannot reset it",
        "It would be great to export reports as PDF",
        "I was charged twice for my subscription",
        "The dashboard loads very slowly"
    ]
    
    for text in test_cases:
        data = {"text": text}
        response = requests.post(f"{API_URL}/predict", json=data)
        print(f"\nInput: {text}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Predicted Category: {result['predicted_category']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Latency: {result['latency_ms']} ms")
        else:
            print(f"Error: {response.json()}")
    
    return True

def test_metrics():
    """Test the metrics endpoint"""
    print("\n\nTesting metrics endpoint...")
    response = requests.get(f"{API_URL}/metrics")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        metrics = response.json()
        if "model_metrics" in metrics:
            print("Model Metrics Available:")
            print(json.dumps(metrics["model_metrics"]["overall_metrics"], indent=2))
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("API TEST SUITE")
    print("=" * 60)
    print("\nMake sure the API server is running: python app.py\n")
    
    try:
        test_health_check()
        test_predict()
        test_metrics()
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("Please start the server first with: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


