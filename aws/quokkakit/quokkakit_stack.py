from aws_cdk import (
    Stack,
    aws_events,
    Duration,
    aws_events_targets,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb_,
    RemovalPolicy
)
from constructs import Construct
    
class QuokkakitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Table
        note_table = dynamodb_.TableV2(self, "NoteItemsTable",
            partition_key=dynamodb_.Attribute(name="id", type=dynamodb_.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            table_name='NoteItemsTable',
            sort_key=dynamodb_.Attribute(
                name="timestamp",
                type=dynamodb_.AttributeType.NUMBER
            ),
        )

        note_table.add_global_secondary_index(
            index_name="username_idx",
            partition_key=dynamodb_.Attribute(name="username", type=dynamodb_.AttributeType.STRING),
            sort_key=dynamodb_.Attribute(
                name="timestamp",
                type=dynamodb_.AttributeType.NUMBER
            )
        )

        note_table.add_global_secondary_index(
            index_name="timestamp_idx",
            partition_key=dynamodb_.Attribute(name="timestamp", type=dynamodb_.AttributeType.NUMBER)
        )

        note_table.add_global_secondary_index(
            index_name="src_idx",
            partition_key=dynamodb_.Attribute(name="src", type=dynamodb_.AttributeType.STRING),
            sort_key=dynamodb_.Attribute(
                name="timestamp",
                type=dynamodb_.AttributeType.NUMBER
            )
        )

        # Create Lambda
        note_lambda = lambda_.Function(self, "noteItemsLambda",
                                                function_name='noteItemsLambda',
                                                runtime=lambda_.Runtime.PYTHON_3_9,
                                                handler="quokka.lambda_handler",
                                                code=lambda_.Code.from_asset("./quokkakit/lambdas"))
        
        note_lambda.add_environment("NoteItemsTable", note_table.table_name)
        note_table.grant_full_access(note_lambda)

        # create a Cloudwatch Event rule
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
        )

        # Add target to Cloudwatch Event
        one_minute_rule.add_target(aws_events_targets.LambdaFunction(note_lambda))
