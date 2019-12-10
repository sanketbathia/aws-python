import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
client = boto3.client('ecs')
pipeline = boto3.client('codepipeline')


def restart_service(event, context):
    # Process own expected event
    print(str(event))
    inputParam = json.loads(event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters'])
    service_name = inputParam["service_name"]
    cluster = inputParam["cluster"]
    job_id = event['CodePipeline.job']['id']
    try:
        print("Service Name : " + str(service_name))
        print("Cluster Name : " + str(cluster))
        logger.info("Starting restart of {0} service in {1} cluster".format(service_name, cluster))
        response = client.list_tasks(cluster=cluster, serviceName=service_name)
        tasks = response.get('taskArns', [])
        logger.info("Service is running {0} underlying tasks".format(len(tasks)))
        for task in tasks:
            logger.info("Stopping tasks {0}".format(tasks))
            client.stop_task(cluster=cluster, task=task)

        logger.info("Completed service restart")

        response = pipeline.put_job_success_result(
            jobId=job_id
        )
    except Exception as e:
        print('Function failed due to exception.')
        print(e)
        traceback.print_exc()
        response = code_pipeline.put_job_failure_result(jobId=job_id, failureDetails={'message': str(e), 'type': 'JobFailed'})
    return response