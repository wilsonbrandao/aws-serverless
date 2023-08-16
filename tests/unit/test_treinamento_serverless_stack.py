import aws_cdk as core
import aws_cdk.assertions as assertions

from treinamento_serverless.treinamento_serverless_stack import TreinamentoServerlessStack

# example tests. To run these tests, uncomment this file along with the example
# resource in treinamento_serverless/treinamento_serverless_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TreinamentoServerlessStack(app, "treinamento-serverless")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
