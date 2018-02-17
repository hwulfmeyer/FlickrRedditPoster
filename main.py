from flickrapi import FlickrAPI, FlickrError, shorturl
import praw
import argparse
import config_my as config

def search_flickr_sorted(searchpage, flickrtaglist):
    """
    Searches flickr for photos with specific tags
    :param searchpage: the result-page to return from the search, starts at 1
    :param flickrtaglist: list of tags(strings) seperate by comma
    :return: list where every element is a link(string) to a flickr photo
    """
    flickr = FlickrAPI(config.flickr_apikey, '', format='parsed-json')
    photolist = []
    photoset = None
    try:
        photoset = flickr.photos.search(tags=flickrtaglist,
                                        sort='relevance',
                                        tag_mode='all',
                                        media="photos",
                                        extras='views',
                                        per_page=100,
                                        page=searchpage)
    except FlickrError as e:
        print('Flickr API error:' + e.code)

    for photo in photoset['photos']['photo']:
        photolist.append(["http://flic.kr/p/" + shorturl.encode(photo['id']), int(photo['views'])])
    photolist.sort(key=lambda x: x[1], reverse=True)
    return [i[0] for i in photolist]


def linkpost_reddit(subredditname, submissiontitle, taglist):
    reddit = praw.Reddit(client_id=config.reddit_clientid,
                         client_secret=config.reddit_clientsecret,
                         user_agent=config.reddit_useragent,
                         username=config.reddit_username,
                         password=config.reddit_password)
    subreddit = reddit.subreddit(subredditname)
    submission = None
    is_submitted = False
    photo_counter = 0
    page_counter = 1
    photolist = search_flickr_sorted(page_counter, taglist)

    while not is_submitted:
        try:
            submission = subreddit.submit(title=submissiontitle, url=photolist[photo_counter], resubmit=False)
            is_submitted = True
        except praw.exceptions.APIException:
            print('Already submitted: ' + str(photo_counter) + ':' + str(page_counter) + '  (photo:page)')
            photo_counter = photo_counter + 1
            if photo_counter >= len(photolist):
                page_counter = page_counter + 1
                photo_counter = 0
                photolist = search_flickr_sorted(page_counter, taglist)
    if is_submitted:
        print("Sucessfully submitted new Photo: " + str(submission.shortlink)
              + '   ' + str(photo_counter) + ':' + str(page_counter) + '  (photo:page)')


if __name__ == "__main__":
    # example: main.py -s Subredditname -i "Title of the Submission" -t "tag1a tag1b" "tag2a tag2b" "tag3"
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags', '-t', nargs='+', type=str, dest='tags', default=[])
    parser.add_argument('--submtitle', '-i', type=str)
    parser.add_argument('--subname', '-s', type=str)
    a = parser.parse_args()
    print(a)
    linkpost_reddit(subredditname=a.subname, submissiontitle=a.submtitle, taglist=a.tags)
