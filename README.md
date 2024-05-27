# edited-task
[home task for edited](https://docs.google.com/document/d/177-MTuV6p0TL_Pyq98JAXzr2et_iuBGRBzbkQ0KnVHc/edit#heading=h.9dfe7slnyrce)

 # steps to locally run
 setup pipenv with:

 `pip install pipenv`

 install packages with:

 `pipenv sync`

 start your own database(modify the configuration if needed)

 start the server with:

 `pipenv run server`

# setup docker
execute:

`docker-compose up -d`

# Explanation

the current workflow is:
* send a request with URL and depth
* start up a browser 
* fetch URL
* take a screenshot
* parse for "href" attributes on the elements
* get only up to the required depth
* redirect the browser to that URL 
* take a screenshot
* save in the uniquely generated UUID folder
* close the browser
* return URLs and paths to images
* save in the database the original URL and reference to the file
* return the UUID to the client


This is a quite bare-bones solution to the task.
* It will not be able to fetch sub images of a link fetched without getting the ID from the DB
* It will not work inside the docker container since it's missing chrome as a browser

For the solution to have a chance to even get close to the required performance, it needs to have a more scalable approach.
The current approach with on request to start up a browser and get the results would impact other requests.
A way to fix that is to start up a thread or a schedule an event for later (very near future).
An alternative approach would be to use remote connections to a separate set of containers existing for the purpose to browse asynchronously.

Improvements:
* Adding unit and e2e tests is a must.
* the images should not be stored on the docker, external volumes or external blob storage should be used.
* alternative unique names should be considered.
* adding pre-commit hooks
* extending the isAlive endpoint with more details like, number of workers and their independent status, can also be quite helpful
* adding an event system would greatly improve monitoring

The aspects of the application that needs to be monitored are:
* Storage space - to know when to switch to a different one or perform clean up
* CPU utilization - do we need to scale up the instances or reduce them
* workers - if extend the isAlive endpoint or use a table inside the database, we can monitor the status of the different instances are they - are they all processing, when did they start and so on.