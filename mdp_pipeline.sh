#!/bin/bash
echo "Creating MDP and specification for $1"
python3 print_domain.py $1.config.py > $1/domain.nm
python3 helper_tools.py $1.config.py > $1/spec.props

echo "Run PRISM on the problem"
prism $1/domain.nm $1/spec.props --pathviaautomata --exportprodstates $1/adv_states.txt --exportadv $1/adv.txt

echo "Translate to human readable adversary..."
python3 build_adversary.py $1.config.py $1/adv.txt $1/adv_states.txt > $1/readable_adversary.txt
echo "Finished!"
