# pip install instaloader

import instaloader

inst = instaloader.Instaloader()

name = "fukuokamachivbc"
inst.download_profile(name,profile_pic_only=True)

#loader = Instaloader()
#loader.load_session_from_file('USER')
#loader.download_feed_posts(max_count=20, fast_update=True,
#    post_filter=lambda post: post.viewer_has_liked)

inst.load_session_from_file(name)
inst.download_feed_posts(max_count=3, fast_update=True,post_filter=lambda post: post.viewer_has_liked)



