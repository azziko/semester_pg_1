# Rock Paper Scissors game
- [How to start playing](#how-to-start-playing)
- [For developers](#for-developers)

## How to start playing:
Press the start button and choose one of the available options. Currently the bot features 2 modes, which are playing against the bot and playing against another player, that are accessible by the commands [/play_bot](https://t.me/rps_online_bot) and [/play_online](https://t.me/rps_online_bot) respectively. After choosing either of the options, the keyboard will pop up so you can make a choice. 

![Player screenshot](/img/screen1.jpg)

In the online mode, the results are not shown until both players choose an option. You can see the result after both players made their choices. It is allowed to change your option as long as your opponent has not chosen one. 

In order to close the keyboard and leave the current mode, press the ‘Close’ button. After that you and your opponent will no longer be matched and you can search for other opponents. 

As a default mode, you are always playing against a bot, unless matched with some other player. Notably, if you send either rock, paper or scissors into the chat, while not being matched to an opponent, you will receive a response from the bot.

![Player screenshot](/img/screen2.jpg)

## For developers:
- [Intro](#intro)
- [How to run](#how-to-run)
- [Logic](#logic)
- [Client](#client)
- [Handler](#handler)
- [Players pool](#players-pool)
- [TODO](#todo)

### Intro:
The program utilizes interface of Telegram Messenger and works with its API in order to process requests of a user and react accordingly. This is worth mentioning that the program establishes webhook connection before running in order to receive requests. This approach is superior to traditional long-polling, since it does not require us to constantly send request for updates to Telegram server, but instead react only when an update is sent.

We use ngrok as destination server for testing, since it allows to anchor webhook to our local host. 

### How to run:
```
- create bot and get token
- create a config directory with a file named config.json and paste there the following:
{
  'tg-token': 'SPECIFY_YOUR_TOKEN_HERE'
}
- run ngrok on port 5000
- build and run server
```

### Logic:
This is the core of our program, which is responsible for the game processing and monitoring players(read [players pool](#players-pool)).

### Client: 
The role of a client in our case plays Telegram, but thanks to the convenient structure of [Handler](#handler) class, it can be replaced with any other messenger(discord, for example) without having to rewrite other modules. 

The main goal of the client module is to establishing webhook connection, working with API and communicating with user.

### Handler
Handler is a connection point of all of our modules. As a parametr it takes a client. As long as client implements all the necessary methods we do not care what client it is. It has only one method route, which reacts according to the command received. 

### Players pool: 
Currently the pull is implemented using the internal memory. While it is an easy solution, our program becomes vulnerable to data loses and memory overflows.
```python
class Matchmaker:
    def __init__(self):
        self.players_db = []
        self.players_waiting = []
```
<strong>*Note:*</strong> the better solution would be to create an interface for database with all the necessary methods implemented so that we can modulate our program even more.

### TODO:
Although our program is fully functioning there are still improvements to be made. One of them could be introducing an actual database(basic NoSQL database would suffice) in place of our current implementation. 

As another justified UX improvement I see is graceful shutdown. Currently, when our program exits, users are not notified of that event, so when two players are matched, they might keep waiting for a response from their opponent without knowing that program has actually crashed.  

Router could be separated into different methods each processing request according to the command sent.
