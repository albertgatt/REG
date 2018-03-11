# REG
Simple Python API for Referring Expression Generation.

# Purpose
This is an implementation of a generic procedure for selecting the content of referring expressions, for later realisation as natrual language strings. 

# Definition
A referring expression (or description) of an object is a set of properties of that object which, in a particular domain, single it out from other objects. For example, given a small blue chair, a large red chair, and a table, the expression *the table* suffices to single out the table, but in order to refer to either of the chairs, one would need to include at least one more property (say, its colour or its size).

The approach taken here follows classic REG algorithms in viewing the process of selceting what to say as a search through the properties of the intended referent. 

A discussion of Referring Expression Generation algorithms can be found here:
> Emiel Krahmer and Kees van Deemter (2012). [Computational Generation of Referring Expressions: A Survey.](https://www.mitpressjournals.org/action/showCitFormats?doi=10.1162/COLI_a_00088) Computational Linguistics 2012 38:1, 173-218

# Usage
We assume that the entities in a domain, and their properties, are represented in a file in csv (comma-separated values) format. See the example in *domain_ex.csv*. Note the following:
- The top row of the file specifies the attributes
- Each entity occupies a subsequent row, and is represented as a list of values for the attributes in question
- Reference to an entity is by row number, starting from 0 (so the first entity in *domain_ex.csv* is a big blue chair with a diamond pattern

The algorithm is used as follws:

```
reg = REGenerator('domain_ex.csv')
description = reg.make_re(0)
print(description)
```

# Search Heuristics
Currently, the assumption is that properties are tested in the order of attributes in the domain file. The strategy is basically that of [Dale and Reiter's Incremental Algorithm](https://arxiv.org/abs/cmp-lg/9504020), where properties are selected in order of preference. This can of course be changed.

The main thing to consider when changing the selection behaviour of the algorithm is the following method:

```
__compare(p1, p2)
```

This takes two properties and compares them, to prioritise one over the other in the search. This is what determines how properties are sorted, and in which order they are returned by `pick_property()`.
