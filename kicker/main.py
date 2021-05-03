import yaml
from typing import Dict
from argo.workflows.client import ApiClient, WorkflowServiceApi, Configuration, V1alpha1WorkflowCreateRequest


def create():
    config = Configuration(host="http://localhost:2746")
    client = ApiClient(configuration=config)
    service = WorkflowServiceApi(api_client=client)

    manifest: Dict[str, any] = get_manifest()

    # # parameters under spec.arguments.parameters are global and can be used by {{ workflow.parameter.name }}
    if 'arguments' not in manifest['spec']:
        manifest['spec']['arguments'] = {'parameters': get_params_as_yaml()}
    elif 'parameters' in manifest['spec']['arguments']:
        manifest['spec']['arguments']['parameters'].extend(get_params_as_yaml())
    else:
        manifest['spec']['arguments']['parameters'] = get_params_as_yaml()

    return service.create_workflow(namespace="da-mottak-dev", body=V1alpha1WorkflowCreateRequest(workflow=manifest))


def get_manifest():
    with open(r'workflows/verify-overforingspakke.yaml') as file:
        return yaml.load(file)


def get_params_as_yaml():
    return [{'name': k, 'value': v} for k, v in get_params().items()]


def get_params():
     return {
            'TUSD_OBJEKT_NAVN': "72f715df8dfdde7330e7e7f97835781e",
            'EKSTERN_ID': "59e92013-f3ed-4e9f-9af5-0afe2686bb87",
            'SJEKKSUM': "d262cf2464916920da5bd1c8335256332cfcc68e4ae517482da7e78aec28d219",
            'KOORDINATOR_EPOST': "kriwal@arkivverket.no",
            'ARKIVUTTREKK_OBJ_ID': "f75a0629-e798-4938-a0c6-ea86bb2885ec",
            'ARKIVUTTREKK_TITTEL': "Arkivgeneratorkomisjonen -- Et sikkelig bra arkiv",
            'CHECKSUM_TAG': '55c3d5fb0ccca55b3a6ab51971a5fe32d1626db9',
            'AVSCAN_TAG': 'a9ef264e8cba61112f309087c2eaf76cdd81c2f8',
            'MAILER_TAG': '55c3d5fb0ccca55b3a6ab51971a5fe32d1626db9'
     }


if __name__ == '__main__':
    tmp = create()
    print(create)
