# bsrecommender
#### A collaborative filtering recommender for Beast Saber songs

Another sweet and short project: writing a (very basic, but the data that I have is limited) personalized song recommender for Beast Saber using collaborative filtering.

The app is deployed in my private kubernetes cluster and accessible at https://bsrec.onsale.duckdns.org/. It takes two arguments, a target user and a list of liked songs, which will be merged to generate the final recommendations. A sample full call would look something like this: https://bsrec.onsale.duckdns.org/?user=ggomarr&liked=9d7,30fd. The deployed version uses the bookmarks of some 15000 users to do its trick.

It returns a json with the recommendations - the idea was that it could get integrated into bsaber.com, but I may develop a web page around it at some point.

Enjoy!
