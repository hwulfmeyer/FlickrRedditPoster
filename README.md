# FlickrRedditPoster
## Resources

Flickr Python Library: https://stuvel.eu/flickrapi-doc/  
Flickr API Doc: https://www.flickr.com/services/api/  
Reddit Python Library: https://praw.readthedocs.io  
Reddit API Doc: https://www.reddit.com/dev/api  


## What does it do?

You run the program in the commandline, specifiy a subreddit, a submission title and a 
arbitrary number of tags to search for (on flickr).  
The programm will fetch a result page with 100 photos and will try to submit one photo to the specified subreddit.
If it has been already submitted the script will go for the next photo and so on. If all photos on one result page already have been submitted it will fetch the second result page and go on with that.  
This goes as long as it hasn't succesfully submitted a photo.


## How to use?

The rogram works as a commandline script.  
Run it like so: main.py -s "Subredditname" -i "Title of the Submission" -t "tag1a tag1b" "tag2a tag2b" "tag3"  
It will automatically do everything and will print out some "debug" statements.
Befor you can run it you have to adapt the config.py and change the import statement in the main.py for the config.py.
Adapting the config.py also means you have to get your own api access keys etc. from flickr and reddit.  
You also have to install the above listed libraries on your system.
