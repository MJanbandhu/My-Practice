# -*- coding: utf-8 -*-
"""Working with RDDs in PySpark (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rVtMrL1Q1R0M2ikQcN0X6OSYsgkxPt19

### Getting Setup (On Google Colab)

* Begin by installing some pip packages and the java development kit.
"""

!pip install pyspark --quiet
#!pip install -U -q PyDrive --quiet
#!apt install openjdk-8-jdk-headless &> /dev/null

"""* Then set the java environmental variable"""

RDD -- Resilient Distributed Datasets

import os
os.environ["JAVA_HOME"] = "/lib/jvm/java-11-openjdk-amd64"

"""* Then connect to a SparkSession, setting the spark ui port to `4050`."""

from pyspark import SparkContext, SparkConf

conf = SparkConf().set('spark.ui.port', '4050').setAppName("films").setMaster("local[2]")
sc = SparkContext.getOrCreate(conf=conf)

"""* Then we need to install ngrok which will allow us to place our local spark ui on the web."""

!wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip &> /dev/null
!unzip ngrok-stable-linux-amd64.zip &> /dev/null
get_ipython().system_raw('./ngrok http 4050 &')

"""* And finally we get a link our Spark UI"""

!curl -s http://localhost:4040/api/tunnels | python3 -c \
    "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

"""### Looking Under the Hood

Now  let's again create an RDD from our movie records.
"""

movies = ['dark knight', 'dunkirk', 'pulp fiction', 'avatar']

movies_rdd = sc.parallelize(movies)
movies_rdd

"""And then let's capitalize the movies, and select the movies that begin with `d`."""

movies_rdd.collect() #action

movies_rdd.take(3) #actions

movies[0].title()

movies

transform=lambda i:i.title()
movies_title=[transform(i) for i in movies]

movies_title

movies_title_rdd=movies_rdd.map(transform) ## transformation

movies_title_rdd.collect()

movies_rdd.collect()

movies_rdd.filter(lambda movies : movies[0]=='d').collect()



movies_rdd.map(lambda movie: movie.title()).take(2)
#transformations -- lazy transformations
## once you apply a transformation only the function is created but it is not applied
## you need an action to apply the transformation across your rdd

rdd2.collect()

rdd1=movies_rdd.map(lambda movies :movies.title()).collect()

rdd1

rdd2=movies_rdd.map(lambda movies : movies.title()).collect()

rdd2

type(rdd2)

type(movies_rdd)

movies_rdd.map(lambda movies :movies.title()).collect()

"""Now as we know, Spark will partition the dataset across the cores of the executors, and then map through the records in parallel, returning all of the results.

> <img src="https://github.com/jigsawlabs-student/pyspark-rdds/blob/main/parallel.png?raw=1" width="60%">

Now let's change the function so that this time, instead of returning all of the results, we just return the first result.
"""

movies_rdd.map(lambda movie: movie.title()).take(1)

"""Now if we think about, this previous step, here we would not have to map through all of the steps just to return a single result.  And it turns out if we look at Spark, we can see that even though the dataset was distributed -- it only needed to perform work on a single partition to return one result.

> <img src="https://github.com/jigsawlabs-student/pyspark-rdds/blob/main/individual_task.png?raw=1" width="80%">

This ability, to see the end result that needs to be returned, and to work efficiently to only take the needed steps to return those results, is a valuable feature when working with large datasets.  And we can better see how Spark accomplishes it in the next section.

### A little experiment

If we run the code below, notice that nothing is returned.
"""

movies_rdd.map(lambda movie: movie.title())

"""And even if we chain the map and the filter methods, still nothing is returned."""

movies_rdd.map(lambda movie: movie.title()).filter(lambda movie: movie[0] == 'D').collect()

"""It's only when we add a collect function on the end, will some data be returned."""

movies_rdd.filter(lambda movie: movie[0] == 'd').map(lambda movie: movie.title()).collect()

"""So above, nothing was returned when we ran the `map` and `collect` functions, because when we only executed those functions, Spark did not actually act on the data.  Then in the third line we finally did act on the data.  We told Spark that we want to both transform, and filter the data, and then return all of the results.  

So it's only when we called the `collect` function that Spark's driver determined the tasks to then send off to the executors and return the results.

### Transformations and Actions

So above we can see that the functions `map` and `filter` do not actually perform any work on our data.  Instead steps are only kicked off when we call the `collect` method.

In Spark, the methods that kick off tasks and return results are called **actions** (eg. collect).  And methods like `map` and `transform` that do not are called **transformations**.

1. Transformations

So we already saw that transformations include `map` and `filter`, and our transformations do not actually return results to our users.  Here's a couple other transformations.

* sample

The `sample` method allows us to take a random sample from our dataset.
"""



movies_rdd.sample(fraction = 0.5, withReplacement = False).collect()

"""> Notice that it does not return any data.

* distinct
"""

movies_rdd.distinct().collect()

"""> Distinct finds the unique results.  Notice that it also does not return data.

Finally, we have already seen `map`, which provides a one to one transformation of our records, and `select` which filters our data.  In each case, our transformations do not return data to us.

2. Actions

Actions are a bit more about the end result.  So far we've learned about `collect`, which returns *all* of the results of a series of transformations.  

* Take

We've also seen `take`, which limits our results to a subset.
"""

movies_rdd.distinct().take(2)

"""> So `take` is similar to the `LIMIT` function in SQL. Notice that here our records are returned.

* Count
"""

movies_rdd.distinct().count()

"""Count simply counts the results."""