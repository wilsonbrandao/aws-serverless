import json

#event é o evento que gerou o trigger da lambda
#context são imformações do serviço que triggou a lambda
def handler(event, context):
   # lambdaRequestId = context["aws_request_id"]    
   # apiRequestId = event.resquestContext.requestId
    
   # print(f"API Gateway RequestId: {apiRequestId} - Lambda RequestId: {lambdaRequestId}")
    
    method = event["httpMethod"]
    if event["resource"] == "/products":
        if method == "GET":
            print("GET")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "GET Products - OK"
                })
            }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Bad Request"
                })
            }