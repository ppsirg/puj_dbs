# neo4j

to run neo4j use docker:

```
docker run \
>     --publish=7474:7474 --publish=7687:7687 \
>     --volume=$HOME/neo4j/data:/data \
>     neo4j

```

as seen on https://neo4j.com/developer/docker-run-neo4j/

password pujdb.2020