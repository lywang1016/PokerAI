# PokerAI
Poker game 



## Roadmap 
If we want to implement multi-player, multi-machine game, we need network programming. [Twisted](https://twistedmatrix.com/trac/) is a great choice.  
On the other hand, if we only want to train a RL model, then we should follow the holy rules in this field, which is OpenAI [Gym](https://gym.openai.com/)  
A more ambitious goal would be to setup a network game using Twisted and in the meanwhile, with one player the RL model trained by OpenAI gym, LOL. The most ambitious project in human history :D


## How to run
```
python main.py
```

You can change the small blind number and big blind number. And you can assing player's name, initial chips, and policy you want. 

Policy 'human' will be human play and when the turn, you should input the action in terminal. 

You can also change the number of game you want to play in the for loop. The player position will automatically be changed base on the game rule.

## Policy attribute
Now you want to build your own policy. It's good to know the current set up.

In folder policy_of_ai, now there is a sample file naive_policy_wly.py

Inside that file, a policy class is defind with 11 attributes. Where:
- 'my_name' is the name of the AI player now need to take action.