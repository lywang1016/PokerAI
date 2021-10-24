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

## Game Strategy (Policy)
Now you want to build your own policy to take action. It's good to know the definition.

In folder 'policy_of_ai', the base class of Strategy is defined in file 'strategy.py'

Inside that file, Strategy class is defind with 11 attributes. Where:
- 'my_name' is the name of the AI player now need to take action. It is a string.
- 'chips' is how many chips this player have. It is a number.
- 'hand' is the two hand cards this player have. It is a list of Card class, where defined in file 'game_frame_work/deckofcards.py'
- 'flop' is the three flop cards. It is a list of Card class.
- 'turn' is the turn card. It is a Card class.
- 'river' is the river card. It is a Card class.
- 'bfo' represents the action order befor flop card. It is a list of string. Each string is the name of a player. The order of the name is the order to take action before flop.
- 'afo' represents the action order after flop card. It is a list of string. Each string is the name of a player. The order of the name is the order to take action after flop.
- 'game_log' is the log of what happend since the game start. It include every action taken by players in game. It is a list of 4 list of game log. This part will be clarified in next section.
- 'chips_to_call' is the number of chips to call if you chose "call" action. It is a number. The value 0 means the action is "check"
- 'min_raise' is the nimimum number of chips to raise if you chose "raise" action. It is a number.

In Player class the method 'your_action()' will be called by Game class, when the player's turn to take action. At this moment, load these attributes to the sub-stratagy class using 'load_attributes()' method. All attributes are given from Game. The 'action_should_take()' method of sub-stratagy class is called and the sub-stratagy object should return the action recommend to take back to the player. It is interestion to implement different stratigies for this method, and it is the point for the project.

The action should take is defined as a list which have two numbers. The first number represents for the action. It could be 0 represent "fold" action, 1 represent "check" or "call" action, and 2 represent "raise" action. The second number represent the chips bet with this action. For "fold" and "check" action, the second number is 0.

You can figure out the postion by 'my_name', 'bfo', and 'afo'. 

Information in the 11 attributes is pretty much all you need to know and legal to know to make an action, according to the game rule. Good luck!

## Game log definition
First, a ActionLog class is defined in file 'game_frame_work/game.py'. The attributes are:
- 'name' is the name who take action. It is a string.
- 'action' is the action taken. It is a string and may be "fold", "check", "call", and "raise".
- 'chip_bet ' is how much chips the player bet to the pot. It is a number.
- 'chip_left' is how much chips the player left after this action. It is a number.
- 'pot' is the total pot size after this action. It is a number.

Then in Game class, after each action taken by player, a ActionLog object will be initialized and added to corresponding log list. Notice there are two special actions called "small blind" and "big blind". These two action is assigned to small blind player and big blind player at the beginning of each game.

There are 4 different log list:
- 'log_before_flop' saves the ActionLog before flop. 
- 'log_flop' saves the ActionLog at flop.
- 'log_turn' saves the ActionLog at turn.
- 'log_river' saves the ActionLog at river.

The 4 log lists described above will be updated when any action happen during the game, and they are the components of list 'log'. Where 'log' is a variable of class Game. Also when any action happen, Game object will broadcast 'log' to all players. 

The attribute 'game_log' of Policy is same as 'log' of Game.

## Card evaluation
You may want to use some methods defined in file 'game_frame_work/evaluation.py' in your policy developent. There are detaied code comments in that file. I believe the comments should be clear enough.

## Implement your own strategy
To implement your own strategy, please first creat a file in 'policy_of_ai' folder. Currently there is an example file 'naive_policy_wly.py'. The file name has the general idea of your strategy as well as your name.

In the created file, please create subclass of class Strategy defined in 'strategy.py' and implement your own algorithm to method 'action_should_take()'.

## Simple GUI
Now there is a simple GUI just for human player. If use human strategy, for each action the human hand cards and public cards will be displayed. The game log infomation still in terminal. And the human action still taken use terminal inputs. You need to install 'matplotlib' for the simple GUI.

## Todo list
### Framework
- Get a nice GUI (Maybe not able to have it quickly. But it's OK since the project targets on build AI algorithms, not a platform to serve human players. However, it is good to have one. Nothing to lose.)

### AI developent
- Maybe can find some method in common and implement first.
- A rule based AI as baseline.