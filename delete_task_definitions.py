# python script to delete Task definations across regions
import boto3
from time import time

AWS_ACCESS = "Acesskey"
SECRET_KEY = "secretkey"

regions = [
    'eu-north-1',
    'ap-south-1',
    'eu-west-3',
    'us-east-2',
    'eu-west-1',
    'eu-central-1',
    'sa-east-1',
    'us-east-1',
    'ap-northeast-2',
    'ap-northeast-3',
    'eu-west-2',
    'ap-northeast-1',
    'us-west-2',
    'us-west-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1'
]


result = []
total_count = 0

begin = time()

for region_name in regions:

    count = 0

    ecs_client = boto3.client('ecs',
            region_name=region_name,
            aws_access_key_id=AWS_ACCESS,
            aws_secret_access_key=SECRET_KEY)

    task_definitions = ecs_client.list_task_definitions(status='INACTIVE')['taskDefinitionArns']

    # for task_definition in task_definitions:
    #     ecs_client.deregister_task_definition(taskDefinition=task_definition)
    #     print(f"Deleting task definition: {task_definition}")

    n = len(task_definitions)
    for i in range(0, n, 10):
        print(f"Deleting task definition: {i}:{i+len(task_definitions[i:i+10])}")
        ecs_client.delete_task_definitions(taskDefinitions=task_definitions[i:i+10])
        count += len(task_definitions[i:i+10])

    total_count += count
    result.append((region_name, count))
    print(region_name, count)

# printing Info
print('\n\nTime :', time() - begin)

print()

print(*result, sep='\n')

print('Total :', total_count)
