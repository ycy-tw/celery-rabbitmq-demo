# celery-rabbitmq-demo

1. Run a rabbimq container
    ```
    docker run --name rabbitmq-demo -p 5672:5672 rabbitmq:3-management
    ```


2. Open a terminal, run consumer app and keep the terminal open.
    ```
    cd consumer/
    poetry shell && poetry install
    celery -A main.app worker --loglevel=info -Q email -n demo-consumer
    ```

3. Open another terminal, run producer app and keep the terminal open also.

    ```
    cd producer/
    poetry shell && poetry install
    celery -A main.app worker --loglevel=info --beat -n demo-producer
    ```


4. After few minutes, you should see the task was sent from producer to consumer.(The task will be executed per minute which defined at `producer/main.py` )
    
    Producer:
    ```
    (producer-py3.10) ycy@YCY-Mac producer % celery -A main.app worker --loglevel=info --beat -n demo-producer


    celery@demo-producer v5.2.7 (dawn-chorus)

    macOS-12.5-arm64-arm-64bit 2023-08-15 23:35:45

    [config]
    .> app:         producer:0x107168b50
    .> transport:   amqp://guest:**@localhost:5672//
    .> results:     disabled://
    .> concurrency: 8 (prefork)
    .> task events: OFF (enable -E to monitor tasks in this worker)

    [queues]
    .> celery           exchange=default(direct) key=celery


    [tasks]
    . tasks.send_email_to_customer

    [2023-08-15 23:35:45,708: INFO/Beat] beat: Starting...
    [2023-08-15 23:35:45,736: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
    [2023-08-15 23:35:45,737: INFO/Beat] Scheduler: Sending due task send_email_to_customer (tasks.send_email_to_customer)
    [2023-08-15 23:35:45,746: INFO/MainProcess] mingle: searching for neighbors
    [2023-08-15 23:35:46,781: INFO/MainProcess] mingle: sync with 1 nodes
    [2023-08-15 23:35:46,781: INFO/MainProcess] mingle: sync complete
    [2023-08-15 23:35:46,828: INFO/MainProcess] celery@demo-producer ready.
    [2023-08-15 23:35:46,829: INFO/MainProcess] Task tasks.send_email_to_customer[d132f747-14b8-41a2-9a55-af7b78897a39] received
    [2023-08-15 23:35:46,937: WARNING/ForkPoolWorker-9] find users under specific conditions...
    [2023-08-15 23:35:46,938: WARNING/ForkPoolWorker-9] send notification event to queue
    [2023-08-15 23:35:46,986: INFO/ForkPoolWorker-9] Task tasks.send_email_to_customer[d132f747-14b8-41a2-9a55-af7b78897a39] succeeded in 0.050595708191394806s: None
    [2023-08-15 23:36:00,001: INFO/Beat] Scheduler: Sending due task send_email_to_customer (tasks.send_email_to_customer)
    [2023-08-15 23:36:00,017: INFO/MainProcess] Task tasks.send_email_to_customer[083276b0-6de0-4f3e-ad62-d26d4597b1e4] received
    [2023-08-15 23:36:00,018: WARNING/ForkPoolWorker-9] find users under specific conditions...
    [2023-08-15 23:36:00,019: WARNING/ForkPoolWorker-9] send notification event to queue
    [2023-08-15 23:36:00,020: INFO/ForkPoolWorker-9] Task tasks.send_email_to_customer[083276b0-6de0-4f3e-ad62-d26d4597b1e4] succeeded in 0.0016347495838999748s: None
    ```

    Consumer:
    ```
    (consumer-py3.10) ycy@YCY-Mac consumer % celery -A main.app worker --loglevel=info -Q email -n demo-consumer


    celery@demo-consumer v5.2.7 (dawn-chorus)

    macOS-12.5-arm64-arm-64bit 2023-08-15 23:35:36

    [config]
    .> app:         consumer:0x106cf2f20
    .> transport:   amqp://guest:**@localhost:5672//
    .> results:     disabled://
    .> concurrency: 8 (prefork)
    .> task events: OFF (enable -E to monitor tasks in this worker)

    [queues]
    .> email            exchange=default(direct) key=notification.email.send


    [tasks]
    . notification.email.send

    [2023-08-15 23:35:36,506: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
    [2023-08-15 23:35:36,513: INFO/MainProcess] mingle: searching for neighbors
    [2023-08-15 23:35:37,544: INFO/MainProcess] mingle: all alone
    [2023-08-15 23:35:37,585: INFO/MainProcess] celery@demo-consumer ready.
    [2023-08-15 23:35:45,763: INFO/MainProcess] sync with celery@demo-producer
    [2023-08-15 23:35:46,992: INFO/MainProcess] Task notification.email.send[5e970f81-5660-49df-9059-c80963e5b468] received
    [2023-08-15 23:35:46,993: INFO/MainProcess] Task notification.email.send[b1db7641-7e82-408f-a062-2cef9c5b2896] received
    [2023-08-15 23:35:46,995: WARNING/ForkPoolWorker-8] receive data={'email': 'demo1@example.com', 'content': 'Some email template html...'}
    [2023-08-15 23:35:46,995: WARNING/ForkPoolWorker-1] receive data={'email': 'demo2@example.com', 'content': 'Some email template html...'}
    [2023-08-15 23:35:46,996: WARNING/ForkPoolWorker-8] send email...
    [2023-08-15 23:35:46,996: WARNING/ForkPoolWorker-1] send email...
    [2023-08-15 23:35:46,996: INFO/ForkPoolWorker-8] Task notification.email.send[5e970f81-5660-49df-9059-c80963e5b468] succeeded in 0.001990749966353178s: None
    [2023-08-15 23:35:46,996: INFO/ForkPoolWorker-1] Task notification.email.send[b1db7641-7e82-408f-a062-2cef9c5b2896] succeeded in 0.00241637509316206s: None
    [2023-08-15 23:36:00,023: INFO/MainProcess] Task notification.email.send[d2c75b1a-0bd9-49b6-bdeb-0692800b4976] received
    [2023-08-15 23:36:00,023: INFO/MainProcess] Task notification.email.send[89aef441-fd4e-4950-a19e-4d71550319da] received
    [2023-08-15 23:36:00,024: WARNING/ForkPoolWorker-1] receive data={'email': 'demo2@example.com', 'content': 'Some email template html...'}
    [2023-08-15 23:36:00,024: WARNING/ForkPoolWorker-8] receive data={'email': 'demo1@example.com', 'content': 'Some email template html...'}
    [2023-08-15 23:36:00,024: WARNING/ForkPoolWorker-1] send email...
    [2023-08-15 23:36:00,024: WARNING/ForkPoolWorker-8] send email...
    [2023-08-15 23:36:00,024: INFO/ForkPoolWorker-1] Task notification.email.send[89aef441-fd4e-4950-a19e-4d71550319da] succeeded in 0.0005670841783285141s: None
    [2023-08-15 23:36:00,024: INFO/ForkPoolWorker-8] Task notification.email.send[d2c75b1a-0bd9-49b6-bdeb-0692800b4976] succeeded in 0.0006682910025119781s: None
    ```