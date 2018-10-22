# OpenAPI spec

This is the [OpenAPI](https://github.com/OAI/OpenAPI-Specification)/[Swagger](https://swagger.io/) specification of Pidgin's REST API, which can be visualized [here](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/uc-cdis/pidgin/master/openapi/swagger.yml).

# Swagger Tool

The specification in `swagger.yaml` is generated using [Flasgger](https://github.com/rochacbruno/flasgger).

To update the documentation:
* update the docstring of the endpoints impacted by the changes;
* run `python run.py`;
* hit the `/swagger` endpoint to update `swagger.yaml` automatically;
* git push the updated `swagger.yaml`.

Note that the specification can be validated using the [Swagger editor](http://editor.swagger.io) and that it can be visualized by hitting the `/apidocs` endpoint in a browser.
