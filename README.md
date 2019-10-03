# Lucifer discord bot
Bot for discord, my own making. I will refer to the discord client from now on as Satan and the bot itself as Lucifer for simplicity's (and fun's) sake.

## Index

+ [Features](#Features)
   
   + [Song playing and queuing](#Song-playing-and-queuing) [UNDER CONSTRUCTION]

+ [Requirements](#Requirements)

## Features

### Song playing and queuing

+ Song playing

   You can use the command play to make Satan join your channel and play the requested url or query to search on youtube, from which it will play the first result.
   
   Furthermore, you can queue a song to be played next to the last one called using the same command, no additional requirements.
   
+ Pause, resume and skip

   Fair enough, you can pause, resume paused players and skip a song.
   
+ Join and leave

   Satan can leave or join your channel on command.

+ Playlist functions

   You can create a playlist and add songs to it.
   
   Calling the playlist command will add to the queue all of the songs contained by the playlist, wich you can add with the add_to_playlist command, you should also be able to remove songs from a playlist.
   
### Event managing
**_DISCLAIMER_:** This function was very specifically made for my discord server I have with my university partners, you can simply not load the cog or change/remove some functions. You can also change the images in the images folder.

+ Event adding and searching
   
   You can add events and Satan will tell you how many days left you got for the due date specified.

+ Pictures

   You can store pictures in the images/ directory for the command horario to show them, right now its used for showing the timetables of my degree

## Requirements

+ discord

   Installed with:

   ``` pip install discord ```

+ youtube-dl

   Installed with:
   
   ``` pip install youtube-dl``` 


+ ffmpeg player

   Installed with:

   ``` pip install ffmpeg-python```

+ Linux

   For windows users you could change the ' / ' to ' \\ ' but there could be more compatibility issues I'm not aware of.
