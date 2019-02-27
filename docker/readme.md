
## Some useful commands

### Run a command inside a container

```
docker exec -it container_name command
eg: docker run -it namenode bash 
```

### Run hdfs command
Hdfs mostly have the same command as linux file manager, i.e *ls, rm, mkdir, cat, etc.*

```
hdfs dfs -command
eg: hdfs dfs -mkdir /folder
```