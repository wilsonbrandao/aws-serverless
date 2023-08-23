#!/usr/bin/env python3
import os

import aws_cdk as cdk

from treinamento_serverless.productsApp_stack import ProductsAppStack
from treinamento_serverless.apiGateway_stack import (ApiGatewayStack, ApiGatewayStackProps )

#app de inicialização
app = cdk.App()

#seta conta, region e tags
env = cdk.Environment(account="834293179565",region="us-east-1")
tags = {
    "cost": "ECommerce",
    "team": "Wilson"
}

#cria stack de serviços do APP (lambda, dynamodb)
productsAppStack = ProductsAppStack(app, "ProductsApp", **{
    "tags": tags,
    "env": env
    })

#cria stack de serviços do API Gateway
apiGatewayStack =  ApiGatewayStack(
    app,
    "ECommerceAPI", 
    ApiGatewayStackProps( #lambdas que integram com API gateway abstraidas em um classe props
        productsAppStack.productsFetchHandler, 
        productsAppStack.productsAdminHandler, 
        **{
            "tags": tags,
            "env": env
            }
        )
    )

#indica que a stack da API Gateway depende da stack de serviços productsAppStack
apiGatewayStack.add_dependency(productsAppStack)

app.synth()
