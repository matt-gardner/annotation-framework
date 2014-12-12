# Annotation Framework

This is a simple Django app that lets you take the results of some prediction task and annotate
them, using a pooled evaluation setup (i.e., take the top k results from each method, put them
into a pool, annotate the pool, compute precision and recall over the instances in the pool).

As of now the data import script is pretty specific to the format of the prediction task I wrote
this for, but it shouldn't be too hard to modify the import script for some new task, if you want
to use this.
