import aws_cdk as cdk
import aws_cdk.aws_logs as cwlogs
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_lambda as lambda_

from constructs import Construct

# classe que recebe em seu construtor a stack responsavel por criar a lambda
# que manipula o endpoint /products
class ApiGatewayStackProps(cdk.StackProps):
    def __init__ (
        self,
        productsFetchHandler: lambda_.Function,
        productsAdminHandler: lambda_.Function,
        **kwargs
        ):
        self.productsFetchHandler = productsFetchHandler
        self.productsAdminHandler = productsAdminHandler
        self.args = kwargs


#cria stack para o serviço API GATEWAY
class ApiGatewayStack(cdk.Stack):
    #Construtor
    def __init__(self, scope: Construct, id: str, props: ApiGatewayStackProps) -> None:
        super().__init__(scope,id, **props.args)
        
        #cria grupo de logs
        logGroup = cwlogs.LogGroup(self, "EcommerceApiGatewayLogs")
        
        #Cria o serviço API GATEWAY
        api = apigateway.RestApi(self, "EcommerceApiGateway", 
            rest_api_name="EcommerceApiGateway",
            #define grupo de logs
            deploy_options= apigateway.StageOptions(
                access_log_destination=apigateway.LogGroupLogDestination(logGroup),
                access_log_format=apigateway.AccessLogFormat
                    .json_with_standard_fields(
                        http_method=True,
                        ip=True,
                        protocol=True,
                        request_time=True,
                        resource_path=True,
                        response_length=True,
                        status=True,
                        caller=True,
                        user=True
                    )
                ),
            cloud_watch_role=True
            )
        
        #Integração com as funções do Lambda recebida pelo construtor em props
        productsFetchintegration = apigateway.LambdaIntegration(props.productsFetchHandler)
        productsAdminintegration = apigateway.LambdaIntegration(props.productsAdminHandler)
        
        #cria path do api gateway (root representa '/') + add_resource
        productsResource = api.root.add_resource("products")
        #adiciona ao path root do api gateway (root representa '/') o parametro id ("/{id}")
        productsIdResource = productsResource.add_resource("{id}")
        
        #GET /products
        productsResource.add_method("GET", productsFetchintegration)  #mapping do metodo GET em '/products' para a integração
        
        #/products/{id}
        productsIdResource.add_method("GET", productsFetchintegration)
        
        #POST /products
        productsResource.add_method("POST", productsAdminintegration)
        
        #PUT  /products/{id}
        productsIdResource.add_method("PUT", productsAdminintegration)
        
        #DELETE /products/{id} 
        productsIdResource.add_method("DELETE", productsAdminintegration)
        
        