![Project Logo](icon.png)

Smack automatically blocks unproductive websites - no need to set-up a whitelist/blacklist that is outsmarted, or too big/small! Smack also adapts
to your current needs dynamically. 

## Getting started

Smack is available for Windows, Mac and Linux.

First, get an Anthropic API-key at https://console.anthropic.com/dashboard and load some cash on it (1 buck is plenty, but 5 is minimum).


##### Release (recommended)

Under the release tab (to the right), click on it. Then download the .zip file corresponding to your OS, unzip, and voilà, there's the executable! Drag-and-drop to your favourite location and double-click when ready. Make sure to carefully follow the instructions it gives!

##### Source

The entry-point is smack.py, so if you run that (with necessary dependencies) you're good to go.




## FAQ

#### How much do the API calls cost?

I've barely gone upwards of 5 cents a day. With time, it will also get more efficient as it gets to know your most frequent (productive and unproductive) websites.

#### It doesn't seem to work for some browsers (Linux)

Yeah, unfortunately Wayland seems to interfere with the functioning of the program. It does work for Brave. If somebody knows any good tab-reading libraries/utilities for Linux, let me know! (Currently, we use xdotool).

#### Where is all my data stored?
All data is stored in the respective config directory of an OS. Note your API-key is stored in plaintext.

#### It misclassified something
First, kill Smack.
1. Give a better task prompt when it queries you at startup.
2. Change your self-description (it is located in a file under .config/Smack/) so that it better matches you.
3. If it's a website (e.g. "mywork.com") with a non-changing title, you can ctrl+f in whiteblacklist.json and change "mywork.com": false to "mywork.com": true. Then restart Smack.
4. (Advanced, needs source code) If the title of the tab changes regularly (e.g. "Lecture 27.09.2024 - VLC Media Player"), add the word (e.g. "VLC", or "Lecture") to the dictionary in wildcardlist. You could also add it to the system prompt, though that'll increase your token costs.

A very advanced use-case (if you have the money), is to store these misclassified examples, and later finetune your own model on e.g. Anthropic. I really couldn't imagine that's necessary though. I have very specific requirements and still do great with the current setup.

#### How do you recommend using this?

I'd let it calibrate to you for a day. I set the program to turn on at startup. Afterwards, for the sake of habit, don't mess with it!

#### Why not just use Freedom/ColdTurkey etc.?

I love ColdTurkey! Sadly, I use Linux. Moreover, generic blacklists didn't quite work for me - I loved reading _anything_, so blocking youtube.com made me end up on Wikipedia, blocking Wikipedia on Our World in Data, etc. etc. Moreover, I may want to access Wikipedia pages related to programming, but not the Wikipedia controversies section of [insert favourite celebrity here].

No more of that! Smack is extremely intelligent by default.

#### What if I want to just have fun on weekends?

Next time you run the program, say so in the prompt!

#### What are good model providers? 

With personal testing, OpenAI, Anthropic and Google's LLM's performed well. Unfortunately, Mistral's LLM did not yet have broad enough knowledge for this task.

I'd recommend choosing based on:

1. Price
2. Whether you can pay (OpenAI requires credit cards, for example)
