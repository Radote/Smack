![Project Logo](icon.png)


Smack automatically blocks unproductive websites - no need to set-up a whitelist/blacklist that is outsmarted, or too big/small! Smack also adapts
to your current needs dynamically.


## Getting started 
First, get an Anthropic API-key at https://console.anthropic.com/dashboard and load some cash on it.

### Linux
With a release:

Grab the executable under dist/ and put it on your PC in your favourite spot. Double-click and you're good to go!

From source:
1. Clone the project to your favourite directory of choice.
2. Customize the starting prompt in smack.py under is_productive.
3. Run the program (e.g. python smack.py) and you're good to go! 



## FAQ
#### How much do the API calls cost?
I've barely gone upwards of 5 cents a day. With time, it will also get more efficient as it gets to know your most frequent (productive and unproductive) websites.

#### It doesn't seem to work for some browsers
Yeah, unfortunately Wayland seems to interfere with the functioning of the program. It does work for Brave. If somebody knows any good tab-reading libraries/utilities for Linux, let me know! (Currently, we use xdotool). 

#### It misclassified something
1. Give a better task prompt when it queries you at startup.
2. Describe yourself in the system message in function is_productive. (Keep it short to keep it cheap!)
3. If it's a specific website with a non-changing title, you can ctrl+f in whiteblacklist.json and change the value to "True", then restart Smack.
4. If the title of the tab changes regularly (e.g. "Lecture 27.09.2024 - VLC Media Player"), add the word (e.g. "VLC", or "Lecture") to the dictionary in safe_words. You could also add it to the system prompt, though that'll increase your token costs.

A very advanced use-case (if you have the money), is to store these misclassified examples, and later finetune your own model on e.g. Anthropic. I really couldn't imagine that's necessary though. I have very specific requirements and still do great with the current setup.


#### Is there Windows/Mac support?
Not yet! Windows support should be trivial with PyGetWindow. I have no clue about Mac, though. Perhaps it'll work out of the box due to the common UNIX core.

#### How do you recommend using this?
I'd let it calibrate to you for a day. I set the program to turn on at startup. Afterwards, for the sake of habit, don't mess with it! 

#### Why not just use Freedom/ColdTurkey etc.?  
I love ColdTurkey! Sadly, I use Linux. Moreover, generic blacklists didn't quite work for me - I loved reading *anything*, so blocking youtube.com made me end up on Wikipedia, blocking Wikipedia on Our World in Data, etc. etc. Moreover, I may want to access Wikipedia pages related to programming, but not the Wikipedia page of [insert controversial celebrity here].

No more of that! Smack is extremely intelligent by default.

#### What if I want to just have fun on weekends?
Next time you run the program, say so in the prompt!

That said, while it is running, you can't change it. It's a bit like a [Ulysses pact](https://en.wikipedia.org/wiki/Ulysses_pact), or a commitment contract for the behavioural economists and married people.

#### What are good model providers?
With personal testing, OpenAI, Anthropic and Google's LLM's performed well. Unfortunately, Mistral's LLM did not yet have broad enough knowledge for this task.

I'd recommend choosing based on:
1) Price
2) Whether you can pay (OpenAI requires credit cards, for example)

