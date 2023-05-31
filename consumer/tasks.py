from main import app


@app.task(name='notification.email.send')
def send_email(data):
    print(f'receive {data=}')
    print('send email...')