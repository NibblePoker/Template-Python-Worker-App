# NibblePoker's Python Worker App Template
Template for a simple threaded worker-based applications in Python.

This template has successfully been used internally for "[nibblepoker.lu](https://nibblepoker.lu)" since 2021
and has finally been made public for easier referencing and usage in future projects.

The whole demo totals at around 300 LoC and is quite easy to modify.<br>
It can also be taken appart and re-incorporated in other project freely due to the very permissive license.


## Customization

### Application's Name
The application's name can be changed in '[app/app.py](app/app.py)', and you just need to adapt the following lines:
```python
# > Printing the logs header
print_header(logger, "My App")
```

### Workers
Workers are simple objects that extend a common class and point to a thread's main function.

A short example can be found in '[my_app/workers/example.py](my_app/workers/example.py)'.

If you want to add your own, you just need to edit the following lines in '[app/app.py](app/app.py)' to include your own.
```python
# > Preparing workers.
logger.info("Preparing workers...")
workers: list[Worker] = list()
workers.append(create_example_worker(
    config=config,
    name_suffix="demo",
    sleep_count=5,
    sleep_length_ms=750,
))
```


## Usage

### Any Host
```shell
cd app/
python ./app.py
```

### Docker-compose
```shell
docker-compose up --build -d
```


## Licenses
This project is dual-licensed under the following open-source licenses.<br>
You can choose the one that best suits your needs:
1. [MIT License](LICENSE-MIT)<br>
   &nbsp;&nbsp;● Just include the `LICENSE-MIT` file and be done with it while using an OSI license.

2. [CC0 1.0 Universal (CC0 1.0) (Public Domain)](LICENSE-CC0)<br>
   &nbsp;&nbsp;● Do whatever you want with it.<br>
   &nbsp;&nbsp;● No credit, mentions or anything else is needed.<br>
   &nbsp;&nbsp;● Just have fun programming :)
