# aascraw

*aascraw* is an automated-automated web crawler/scrper library. You define the schema of desired data and provide minimal amount of example, and the library will automatically fit actions which will execute web crawling/scraping.

# How it works?

Actions of typical web crawlers can be summarised into the following two:
- First, a programme finds an axis over which the programme will iterate.
- Second, for each iteration in the loop, the programme locate and process desired elements and store into some form of storage.

Aascraw follows deliver-filter-evaluate model, whose goal is to optimise these two operations. The first action is executed by `Deliverer` class and the second actions is executed by `Filterer` class. The `Storage` class evaluates the data crawled by collaboration of `Deliverer` and `Filterer`, and provides them feedbacks so that they can optimise actions for later iterations.

# Kernels
Kernels are python funtions which receives collected record as input and returns rank. Rank is a measure of desirability of input records.

# Versioning Guide
The versions of the library follows MAJOR.MINOR.PATCH scheme. Specfically:

- PATCH - for optimisations and bug-fixes
- MINOR - for changes that affect user interfaces, i.e. public methods, new features.
- MAJOR - no plan yet.