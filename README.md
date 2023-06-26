## Project Description - 

1. ActivityFeedClient - This contains the client code which could be connected via terminal to receive all the notifications from the server

2. ActivityFeedServer - This contains the server code which is taking care of all the activity feed management.

## Scope of project

1. Once server is up and running and a client connects to the server, client will print a message `WebSocket connection is open` indicating our websocket connection is successfully created.
2. Register a user with `username` and `password`.
3. Login using login api to fetch the access token that is to be used as bearer token as auth for other apis.
4. To queue the task, have used `celery` which is running on top of local redis data storage. Also need to start celery as a different process which will take care of tasks on queues.
4. Once we call the `file-edit` api, it's stored as tasks in celery queue and from there notifications will be triggered to all the clients connected and event is recorded.
5. ActionList api gives an understanding of the latest activities that happened in a project. ( Intentionally I haven't put any pagination around it, as wasn't sure about it's functional expectations )

## Server 

It's a Django channels application is written in `python` using `Django rest framework`. There are two API endpoints for handling HTTP requests and one websocket url to handle server-client websocket connection.

The code has been deployed on AWS EC2 instance.
We are using Daphne as a web server for managing and handling WebSocket connections.

Have used this in combination with nginx to make the system more robust, it could help us handling things like load balancing, service discovery, serving static files ( CDN ), etc.

Using celery for enqueuing tasks.

## Client

Written in python, it's a script to create authenticated websocket connection with the server and receive any notification that comes in.

## Running Client and Server application


## Pre-requisites -

* python installed >= 3.10

* Clone this project on local
    ```
    git clone https://github.com/Blank000/ActivityFeed.git
    ```
    or download and unzip from 
    
    https://github.com/Blank000/ActivityFeed/archive/refs/heads/main.zip

### How to run client 

1. Change directory - 
    > cd <PROJECT_ROOT_DIR>/ActivityFeedClient/

2. Run client - 

    `hostname` is an optional field with a default value pointing to the EC2 instance. To run on local, please pass `localhost` as the value or `0.0.0.0`

    > python client.py --project_id <PROJECT_ID> --token <ACCESS_TOKEN> --hostname localhost

### How to run server 

A server is already up and running on AWS Ec2, can make use of that if needed.
Below is the postman collection for that - 

> https://bold-sunset-760997.postman.co/workspace/New-Team-Workspace~ed0071e2-d426-4c90-b950-9ccbf9ccf8da/collection/7965325-b729b66b-4988-44f1-acbf-ccbc5fa9301d?action=share&creator=7965325

## APIs and Websocket URLs

1. API Endpoint to register user - `http://{{hostname}}:8000/user/register/`
2. API Endpoint to login user - `http://{{hostname}}:8000/user/token/`
3. Websocket url for client to connect to the server - `http://{{hostname}}/ws/projects/<int:project_id>/`
4. API endpoint to call a file-edit event (or activity) - `http://{{hostname}}/api/projects/<int:project_id>/file-edit/`
5. API endpoint to fetch the latest activities against a project - `http://{{hostname}}/api/projects/<int:project_id>/actions/`


__Want to run your own server, please follow the below steps__ - 

1. Create Python virtual environment - 
    
    Before running this move to any directory where you want to create your virtual environments. Let's consider that directory here is $HOME

    > cd $HOME
   
    Create envrionments as below - 

    * Using virtualenv - 

        > virtualenv <ENV_NAME>

        > source $HOME/<ENV_NAME>/bin/activate

    * Using python -m -

        > python -m venv <ENV_NAME>
        
        > source $HOME/<ENV_NAME>/bin/activate

2. Install dependencies - 

    > pip3 install -r <PROJECT_ROOT_DIR>/ActivityFeedServer/requirements.txt

3. Run migrations - 

    > python3 manage.py makemigrations notifications
    > python3 manage.py migrate

3. Run Daphne web server on local - 

    > cd <PROJECT_ROOT_DIR>/ActivityFeedServer/

    > $HOME/<ENV_NAME>/bin/daphne -b 0.0.0.0 -p 8000 activity_feed.asgi:application

### How to run celery 

It's already up and running on AWS Ec2, can make use of that if needed.
Note - __Be in the same virtual environment as the one while seting up server.__
If trying to run on local, can follow below steps - 

1.  Running celery worker process - 

    > cd <PROJECT_ROOT_DIR>/ActivityFeedServer/

    > celery --app=activity_feed worker --loglevel=info -E

Now the server is up and running and ready to be tested.
