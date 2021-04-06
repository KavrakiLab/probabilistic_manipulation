# Running the code

## Install PRISM
Follow directions [here](https://github.com/prismmodelchecker/prism)

## Install ltlf_for_prism (optional)
If you want to use LTLf, follow the directions [here](https://github.com/andrewmw94/ltlf_prism)



## Creating the MDP

```python3 print_mdp.py 3block.config.py > 3block/domain.nm```

(Note the '.' rather than a '/' for "3block.config")

This saves the domain MDP in 3block/domain.nm

## Create a specification

```python3 helper_tools.py 3block.config.py > 3block/spec.props```

(Again, note the '.' rather than a '/' for "3block.config")

This saves the specification in 3block/spec.props


## Run PRISM on the problem

(Optional) You may want to alias some command to add prism to your path. I added the following to my .bashrc:

```alias pmc='export PATH=$PATH:/home/awells/Development/prism/prism/bin'```

Then I run:
```pmc```

And ``$path_to_prism/`` below is the empty string.

To run Prism on the files:

```cd 3block```

```path_to_prism/prism domain.nm spec.props```


This computes the optimal probability of satisfying the specification.

If you want to view the policy (which prism calls the adversary), run:

```prism domain.nm spec.props --pathviaautomata --exportprodstates adv_sates.txt --exportadv adv.txt```

(Note --pathviaautomata, which forces prism to construct an automata. This can be unnecessary. If you don't want to use this, you would need to modify the above to use --exportstates in the case where no product is constructed)

To construct a ``human-readable`` adversary from these:

```cd ..```

```python3 build_adversary.py 3block.config.py 3block/adv.txt 3block/adv_states.txt > 3block/readable_adversary.txt```

The first line should give the interperation of each element of the tuples. The remaining line should give an action to take for each state.