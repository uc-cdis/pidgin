# Pidgin

A core metadata service

## Concept

Pidgin is a lightweight API on top of [Peregrine](https://github.com/uc-cdis/peregrine). It takes a file's GUID as input, queries Peregrine for information about this file and returns an abstract of the file to the user.

Pidgin powers the "Download file" page, accessible from the "Files" page of the [Windmill data portal](https://github.com/uc-cdis/data-portal).

## Usage

Pidgin has a single endpoint: `/<GUID of a file>`. By default, this endpoint returns the core metadata as a JSON document. However, bibliography and JSON-LD schema.org formats are also supported. The user can specify the format of the output using the `Accept` header as follows:

```bash
Accept: application/json # for JSON format
Accept: x-bibtex # for bibliography format
Accept: application/vnd.schemaorg.ld+json # for JSON-LD format
```

## API documentation

[OpenAPI documentation available here.](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/uc-cdis/pidgin/master/openapi/swagger.yml)

The YAML file containing the OpenAPI documentation can be found in the `openapi` folder; see the README in that folder for more details.

### Quickstart with Helm

You can now deploy individual services via Helm!

If you are looking to deploy all Gen3 services, that can be done via the Gen3 Helm chart.
Instructions for deploying all Gen3 services with Helm can be found [here](https://github.com/uc-cdis/gen3-helm#readme).

To deploy the pidgin service:
```bash
helm repo add gen3 https://helm.gen3.org
helm repo update
helm upgrade --install gen3/pidgin
```
These commands will add the Gen3 helm chart repo and install the pidgin service to your Kubernetes cluster.

Deploying pidgin this way will use the defaults that are defined in this [values.yaml file](https://github.com/uc-cdis/gen3-helm/blob/master/helm/pidgin/values.yaml)
You can learn more about these values by accessing the pidgin [README.md](https://github.com/uc-cdis/gen3-helm/blob/master/helm/pidgin/README.md)

If you would like to override any of the default values, simply copy the above values.yaml file into a local file and make any changes needed.

You can then supply your new values file with the following command:
```bash
helm upgrade --install gen3/pidgin -f values.yaml
```

If you are using Docker Build to create new images for testing, you can deploy them via Helm by replacing the .image.repository value with the name of your local image.
You will also want to set the .image.pullPolicy to "never" so kubernetes will look locally for your image.
Here is an example:
```bash
image:
  repository: <image name from docker image ls>
  pullPolicy: Never
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""
```

Re-run the following command to update your helm deployment to use the new image:
```bash
helm upgrade --install gen3/pidgin
```

You can also store your images in a local registry. Kind and Minikube are popular for their local registries:
- https://kind.sigs.k8s.io/docs/user/local-registry/
- https://minikube.sigs.k8s.io/docs/handbook/registry/#enabling-insecure-registries

Dependencies:
Pidgin relies on Peregrine to run. Please view the [Peregrine Quick Start Guide](https://github.com/uc-cdis/peregrine) for more information.
