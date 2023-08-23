import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_dynamodb as dynamodb_

from constructs import Construct
# cria stack para serviço LAMBDA
class ProductsAppStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs: cdk.StackProps) -> None:
        super().__init__(scope,id,**kwargs)
        
        #cria tabela no DynamoDb
        self.productsDynamoDb = dynamodb_.Table(
            self, #escopo onde o serviço é criado: propria stack
            "ProductsDdb", #id recurso
            table_name="products", 
            removal_policy=cdk.RemovalPolicy.DESTROY, #se a tabela é apagada se a stack por apagada
            partition_key=dynamodb_.Attribute(name="id", type=dynamodb_.AttributeType.STRING), # PK da tabela   
            billing_mode=dynamodb_.BillingMode.PROVISIONED,
            read_capacity=1, #qtd read request por segundo (padrão é 5)
            write_capacity=1 #qtd write request por segundo (padrão é 5) 
        )
        
        #cria um atributo e recebe o metodo AWS que cria uma função lambda
        self.productsFetchHandler = lambda_.Function(
            self, 
            "ProductsFetchFunction", 
            function_name="ProductsFetchFunction",
            code=lambda_.Code.from_asset("lambda/products/"), #indica o arquivo que contém o code da função
            handler="productsFetchFunction.handler", #indica o método inicial da função
            memory_size=128,
            timeout=cdk.Duration.seconds(5),
            runtime=lambda_.Runtime.PYTHON_3_10,
            environment={
                "PRODUCTS_DDB": self.productsDynamoDb.table_name #cria variavel de ambiente na lambda com da tabela do dynamo
            }
        )
        
        self.productsAdminHandler = lambda_.Function(
            self, 
            "ProductsAdminFunction", 
            function_name="ProductsAdminFunction",
            code=lambda_.Code.from_asset("lambda/products/"), #indica o arquivo que contém o code da função
            handler="productsAdminFunction.handler", #indica o método inicial da função
            memory_size=128,
            timeout=cdk.Duration.seconds(5),
            runtime=lambda_.Runtime.PYTHON_3_10,
            environment={
                "PRODUCTS_DDB": self.productsDynamoDb.table_name #cria variavel de ambiente na lambda com da tabela do dynamo
            }
        )
        
        #dar permissões para as roles atreladas as lambdas
        self.productsDynamoDb.grant_read_data(self.productsFetchHandler)
        self.productsDynamoDb.grant_write_data(self.productsAdminHandler)
        
        
        
        

