import aws_cdk as core
import aws_cdk.assertions as assertions

from quokkakit.quokkakit_stack import QuokkakitStack


def test_aws_stack():
    app = core.App()
    stack = QuokkakitStack(app, "QuokkakitStack")
    template = assertions.Template.from_stack(stack)

    template = assertions.Template.from_stack(stack)
    envCapture = assertions.Capture()

    template.resource_count_is("AWS::DynamoDB::GlobalTable", 1)

    template.has_resource_properties("AWS::Lambda::Function", {
            "Handler": "quokka.lambda_handler",
            "Environment": envCapture,
    })

if __name__ == '__main__':
    test_aws_stack()
