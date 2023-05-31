from main import app


@app.task
def send_email_to_customer():
    
    print('find users under specific conditions...')

    data = [
        {
            'email':'demo1@example.com',
            'content':'Some email template html...',
        },
        {
            'email':'demo2@example.com',
            'content':'Some email template html...',
        }
    ]

    print('send notification event to queue')

    for d in data:
        app.send_task(
            name='notification.email.send',
            kwargs={'data':d},
            exchange='default',
            routing_key='notification.email.send'
        )