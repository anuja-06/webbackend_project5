#Service Orchestration

To this point, the services you’ve built have been entirely independent of each other, even going so far as to use separate databases. 
Even when you place the services behind a reverse proxy like Traefik so that all APIs can all be accessed through a common hostname and port (sometimes called the Gateway Routing pattern), the responsibility falls on the client to manage gameplay.

While this may be an entirely reasonable thing to do for a rich client such as a desktop or mobile app, a simpler, unified interface may be preferable for a web version of the game. In this final project you’ll implement the Backends for Frontends pattern to unify the services behind a single, much simpler API, orchestrating calls behind the scenes to coordinate functionality across services.

The following are the learning goals for this project:

1.Understanding several different cloud design patterns for coordinating microservices.

2.Coordinating stateful and stateless services to accomplish a high-level task.

3.Gaining experience integrating services from several different teams.

4.Using an HTTP client library to make HTTP calls and parse JSON results.

5.Making and coordinating asynchronous calls to API calls to proceed in parallel.


