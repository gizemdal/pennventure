## My Project Blog

A project blog where I write down short summaries of my work whenever possible. Blog start date: Feb 24th, 2020
______

Sunday February 24th:

I reworked on the Plot and Plot Point classes to follow the adjacency list implementation from Graph(V, E).
Every vertex in a plot graph is a plot point.
Every edge going from one plot point to another is a list of preconditions to reach the other plot point.

I decided to represent my conditions as (condition category, condition item) tuples where a condition category represents
the type of condition ('is item in player inventory?', 'does location have item?', etc.). The condition item can be an
Item object, a Location object, a (NPC, Item) object tuple and more depending on the condition category. For now I have
about 4 categories but I'm looking to improve that.

I'm looking for ways to add dimention to character relationships. I want relationships to be an item that Drama Manager
could use to adjust the plot but for now relationship is defined as a (short term, long term) relationship score tuple.
It would be nice to add more complexity and layers to it.
