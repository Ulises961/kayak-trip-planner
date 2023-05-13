# Testing


To test the API you can use pytest, for example
```bash
pytest Test/
========================================================= test session starts =========================================================
platform linux -- Python 3.10.11, pytest-7.3.1, pluggy-1.0.0 -- /home/bsultan/.local/share/virtualenvs/kayak-trip-planner-KtTF46qY/bin/python
cachedir: .pytest_cache
rootdir: /home/bsultan/Desktop/kayak-trip-planner
collected 10 items                                                                                                                    

Tests/0_user_resource_test.py::test_user_post PASSED                                                                            [ 10%]
Tests/0_user_resource_test.py::test_user_extra_arguments PASSED                                                                 [ 20%]
Tests/0_user_resource_test.py::test_user_missing_arguments PASSED                                                               [ 30%]
Tests/0_user_resource_test.py::test_get_all_users PASSED                                                                        [ 40%]
Tests/1_trip_resource_test.py::test_insert_trip_w_itinerary_and_inventory PASSED                                                [ 50%]
Tests/1_trip_resource_test.py::test_insert_trip_w_itinerary_and_empty_inventory PASSED                                          [ 60%]
Tests/1_trip_resource_test.py::test_insert_trip_w_o_itinerary PASSED                                                            [ 70%]
Tests/1_trip_resource_test.py::test_get_all_trips PASSED                                                                        [ 80%]
Tests/1_trip_resource_test.py::test_get_trip_by_id PASSED                                                                       [ 90%]
Tests/2_day_resource_test.py::test_insert_day_with_sea_and_weather PASSED                                                       [100%]

========================================================= 10 passed in 1.13s ==========================================================

```

## Creating new tests

To add tests to this API you can add a test file inside the Tests folder.
