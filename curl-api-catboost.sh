#!/bin/sh

curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
	"config":{
		"profile":"cat-test-model"
	},
	"data":{
		"amount": "25.00",
		"bank_currency":"840",
        "bin":"400022",
        "country":"USA",
		"day_of_week":"2",
		"hour":"00",
		"is_city_resolved":"1",
		"is_gender_undefined":"1",
		"latitude":"38.2981",
		"longitude":"-77.4826",
		"phone_2_norm": "01"
	}
}' \
 'http://192.168.0.105:8037/api/v2/check_order/'