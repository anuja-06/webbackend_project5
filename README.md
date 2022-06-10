#Service Orchestration

Initializing, setting up the environment and running the microservices.
    1. Download the project zip file.
    2. Kindly check if all the databases in var directory have data. If not, run the following commands orelse dont run i.
    3. Run the below commands on terminal.
        a. Moving to working directory: cd Downloads/Project5/fastapi/api
        b. Populate database for project 2: ./bin/init.sh
        c. Populate database for project 3: ./bin/stats.py
        d. Populate database for sharding: python3 sharding.py
        e. Populate database for project 4: python3 redisdata.py
    4. Starting the microservice: foreman start
    5. To test the microservices we are using FastAPI Swagger.
    6. Try out the service.

