#!/bin/sh

curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{"config": {"profile": "cat_3-75-015_seed_45_2021-01-26"},
"data": {"amount": "158.85",
"bank_currency": "840",
"bin": "510932",
"day_of_week": "2",
"hour": "00",
"is_city_resolved": "1",
"is_gender_undefined": "1",
"latitude": "undef",
"longitude": "undef",
"phone_2_norm": "20"}
}' \
 'http://0.0.0.0:8011/api/v3/check_order/'
