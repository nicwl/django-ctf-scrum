The first flag
==============

View source. It is the first thing you see.

```html
<!--flag{3@zy-p1ck1ng5}-->
```

The second flag
===============

To get a post with over 10 000 points, you obviously need to first create a post.

Once you've created a post, you can see that it has upvote and downvote buttons. Perhaps you just need to click the upvote button 10 000 times in order to get 10 000 upvotes. Attempting this reveals that you can only vote once per post, so you either have to make 10 000 users (which would work but is a lot of effort), or you can try to work around the single-vote-per-user system.

By using "Inspect Element" (or equivalent) in your browser's dev tools, you can see that the upvote button's DOM looks like this.

```html
<form method="post" action="/vote/">
	<input type="hidden" name="post" value="2">
	<input type="hidden" name="direction" value="1">
	<button type="submit" class="vote_button up">
		<span class="glyphicon glyphicon-menu-up" aria-hidden="true"></span>
	</button>
</form>
```

The DOM for the downvote button is identical except that the "direction" input looks like this

```html
<input type="hidden" name="direction" value="-1">
```

From this, you can develop a theory that the programmer intends for every user to have at most one vote per post, and for that vote to add some value to the total score of the post. The programmer also intends for that value to be plus or minus 1. What if we modify the upvote form in Chrome dev tools so that instead of sending direction=1, we send direction=10000?

```html
<input type="hidden" name="direction" value="10000">
```

Now clicking the upvote button makes your score hit 10 000 and reveals the flag.

```
flag{v0x-p0pul1}
```

The third flag
==============

We know that the third flag is the password for ExtremeModerator. We haven't really got any more clues about how to find out what their password is. We have to look around the site and see if there's any way to get more information.

There is a menu next to the page header saying "As you like them". Clicking on this reveals 5 ways to order and filter posts on the site. Clicking on any of them adds a GET parameter to the page URL. This is the mapping of choice to GET query string.

* Most recent first: `?order=-id`
* Best users first: `?order=author__denorm_score`
* Best first: `?order=denorm_score`
* Worst first: `?order=-denorm_score`
* Your posts: `?filter=author__id%3D2`

If the last of those looks like garbage to you, you should read about URL encoding. It boils down to `?filter=(author__id=2)` in an abstract sense. Note that 2 is my user ID and may not be your user ID.

What's interesting here is that the ordering and filtering options don't seem to name the order or filtering we choose. They seem to describe how to order or filter the data in the way we want. What if we try changing these parameters? Can we set author__id to be another user's id? If we go to `?filter=author__id=1` then we get ExtremeModerator's post. Can we set filter by other author attributes (from the second ordering option it seems that we can)? If we go to `?filter=author__denorm_score%3D10000`, we only get posts from users with 10000 points. Can we filter by other attributes? Can we filter by password? Going to `?filter=author__password%3D123` when our password is 123 gives us our posts. Choosing a random value for author__password does not give us any posts.

What we have here is a way to check if any user has a particular password. This is slightly more useful from a brute-force persective than the login screen was, but still isn't particularly useful.

I don't know whether DEBUG mode was enabled during the contest, but if it was generating an error would have revealed that this is a Django application, and may have revealed the particular code which was handling the filtering and ordering in this instance. From that it would have been pretty clear that the GET parameters are being passed straight into Django's ORM, and that the double-underscores have semantic meaning. If DEBUG wasn't enabled you had to just recognise the format of the parameters or use google-fu.

Regardless, the double underscores can mean two things. In the case of `author__id` it means "First, look at the author of this post, then get the ID of that author". The other use of double underscores is to specify a comparison function. `Post.objects.filter(author__username="lolnic")` is actually a shorthand for `Post.objects.filter(author__username__exact="lolnic")`, meaning "Posts whose author's username exactly matches 'lolnic'". There are other comparison functions supported, however. One such is `startswith`. If we query the app for "Posts whose author's password starts with 'flag{'" (`?filter=author__password__startswith%3Dflag{`), we get ExtremeModerator's post. From here we can simply write a script to brute-force ExtremeModerator's password character-by-character. The script `breaker.py` will do this.

```
flag{0rm-1nj3ct1on}
```

Note: In reality this password would probably be hashed. In fact, there were workarounds put in place in this app to prevent Django's automatic password hashing. There are real (if poor) reasons that passwords would not be hashed in the wild, however (perhaps they are stored in some legacy system, or perhaps the author of the app is aggressively incompetent).