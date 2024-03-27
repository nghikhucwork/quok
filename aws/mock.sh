#!/bin/bash

# Set the function name
function_name="noteItemsLambda"

# Set the starting and ending numbers
start=1
end=10

# Loop through the numbers
for i in $(seq $start $end); do
    # Set the payload
    payload='{"method":"POST","body":{"content":"content '$(($i + 1))'","username":"nk"}}'

    # Invoke the function
    awslocal lambda invoke --function-name $function_name \
        --payload "$payload" ./output.json
done

