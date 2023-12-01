# python script to delete ECS Cluters across regions 
import boto3


AWS_ACCESS = "Accesskey"
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

for region_name in regions:

    ecs_client = boto3.client('ecs',
            region_name=region_name,
            aws_access_key_id=AWS_ACCESS,
            aws_secret_access_key=SECRET_KEY)

    clusters = ecs_client.list_clusters()['clusterArns']

    # print(clusters)

    count = 0
    for cluster in clusters:

        services = ecs_client.list_services(cluster=cluster)['serviceArns']

        # Delete each service
        for service in services:

            ecs_client.update_service(cluster=cluster, service=service, desiredCount=0)

            print(f"Waiting for service tasks to stop: {service}")
            ecs_client.get_waiter('services_stable').wait(
                cluster=cluster,
                services=[service],
                WaiterConfig={
                    'Delay': 6,
                    'MaxAttempts': 30
                }
            )

            print(f"Deleting service: {service}")
            ecs_client.delete_service(cluster=cluster, service=service)

        print(f"Deleting ECS cluster: {cluster}")
        ecs_client.delete_cluster(cluster=cluster)

        count += 1

    print(region_name, count)
    result.append((region_name, count))

# No of deleted clusters per region(INFO)
print(*result, sep='\n')
