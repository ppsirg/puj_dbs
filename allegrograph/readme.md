# allegrograph

to run allegrograph use:

´´´
docker run -it --rm \
         --shm-size 1g \
         -v agdata:/agraph/data \
         -v agconfig:/agraph/etc \
         -e AGRAPH_SUPER_USER=admin \
         -e AGRAPH_SUPER_PASSWORD=pass \
         -p 10000-10035:10000-10035 \
         --name agraph-instance-1 \
         franzinc/agraph:v7.0.0
´´´
docker run -it --rm --shm-size 1g -v agdata:/agraph/data -v agconfig:/agraph/etc -e AGRAPH_SUPER_USER=admin -e AGRAPH_SUPER_PASSWORD=pass -p 10000-10035:10000-10035  --name agraph-instance-1 franzinc/agraph:v7.0.0