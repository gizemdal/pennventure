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

Monday February 25th:

I met with CCB in the morning to discuss how to add more dimentions to Player-NPC relationships. He suggested that I could create a multiclass classifier and train on different categories of interactions such as friendly, romantic, hostile, etc.
He also sent me a research paper "Learning to Speak and Act in a Fantasy Text Adventure Game" where they discuss how to assign
interesting roles and characteristics to NPC characters. The techniques described there might be a bit beyond my project but
it could be useful as a source.

I found several sentiment analysis data online that I could potentially use to train a multiclass classifier. I will likely focus on this after Alpha review.

Tuesday February 26th:

Started working on a mini example game to explore data structures


