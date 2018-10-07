### tvmaze_wrapper

Python interface to the TV Maze API

This interface always returns JSON objects except for some convenience methods
, which returns some info about shows and episodes, such as:

- Show Name
- Number of seasons
- Episodes (each episode has)
    - Number
    - Title
    - Season show

Use `single_search()` if you are pretty sure of the name of the show you are
looking for (e.g. `single_search('the big bang theory')` - Will always be 
returned one item only

Use `get_shows()` if you want to retrieve a number of possible 
matches to process for a given pattern to get the show you actually want, 
for example:

`get_shows('girls')` will gives you:

```
000139 Girls
000525 Gilmore Girls
006771 The Powerpuff Girls
022131 Brown Girls
009136 Funny Girls
000722 The Golden Girls
021949 Kaiju Girls
000911 Some Girls
003418 ANZAC Girls
013826 Soldier Girls
```

For alwost any other method you will need the show id as parameter which you
get from `get_shows()` or `single_search()`



