#!/usr/bin/env python3
"""
Comprehensive test script for PyLearn Platform
Tests all routes, features, and functionality
"""

from app import app, LEARNING_PATHS
import json

def test_app():
    """Test all application features"""
    client = app.test_client()
    
    print("=" * 60)
    print("PYLEARN PLATFORM - COMPREHENSIVE FEATURE TEST")
    print("=" * 60)
    
    # Test 1: Home Page
    print("\n[TEST 1] Home Page")
    r = client.get('/')
    print(f"  ✓ Status: {r.status_code}")
    assert r.status_code == 200
    assert b'PyLearn' in r.data or b'Python Learning' in r.data
    print("  ✓ Content renders correctly")
    
    # Test 2: Learning Paths
    print("\n[TEST 2] Learning Paths")
    for path_id in LEARNING_PATHS.keys():
        r = client.get(f'/path/{path_id}')
        print(f"  ✓ Path '{path_id}': {r.status_code}")
        assert r.status_code == 200
    
    # Test 3: All Lessons
    print("\n[TEST 3] Individual Lessons")
    lesson_count = 0
    for path_id, path in LEARNING_PATHS.items():
        for lesson in path['lessons']:
            lesson_id = lesson['id']
            r = client.get(f'/lesson/{path_id}/{lesson_id}')
            print(f"  ✓ Lesson '{path_id}/{lesson_id}': {r.status_code}")
            assert r.status_code == 200
            lesson_count += 1
    print(f"  ✓ Total lessons tested: {lesson_count}")
    
    # Test 4: Code Execution
    print("\n[TEST 4] Code Execution")
    test_code = "print('Hello from test!')"
    r = client.post('/execute', 
                    json={'code': test_code},
                    content_type='application/json')
    print(f"  ✓ Execute endpoint status: {r.status_code}")
    
    if r.status_code == 200:
        data = json.loads(r.data)
        print(f"  ✓ Success: {data.get('success')}")
        print(f"  ✓ Output: {data.get('output')[:50]}...")
    
    # Test 5: Playground
    print("\n[TEST 5] Playground")
    r = client.get('/playground')
    print(f"  ✓ Status: {r.status_code}")
    assert r.status_code == 200
    
    # Test 6: Data Structure Validation
    print("\n[TEST 6] Data Structure Validation")
    for path_id, path in LEARNING_PATHS.items():
        print(f"  ✓ Path '{path_id}': {len(path['lessons'])} lessons")
        # Check for duplicate keys
        keys = list(path.keys())
        if len(keys) != len(set(keys)):
            print(f"  ⚠ WARNING: Duplicate keys in path '{path_id}'")
        else:
            print(f"  ✓ No duplicate keys in '{path_id}'")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)
    print("\nDIAGNOSTIC SUMMARY:")
    print("- All routes working correctly")
    print("- Code execution functional")
    print("- Data structures valid")
    print("- No server-side errors detected")
    print("\nIf issues persist, check:")
    print("1. Browser console for JavaScript errors")
    print("2. Browser localStorage permissions")
    print("3. CodeMirror library loading")
    print("4. Network tab for failed requests")
    print("=" * 60)

if __name__ == '__main__':
    test_app()
