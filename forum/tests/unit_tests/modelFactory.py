from django.contrib.auth.models import User
from forum.models import Board, Post, Reply, UserProfile

# count of each model objects created
#these are used to make sure two function calls don't create objects with the same values for unique fields
user_cc= 0
post_cc= 0
board_cc= 0

class UserFactory:
    # This number is appended to unique field values
    obj_count = 0

    @classmethod
    def nextid(cls):
        cls.obj_count +=1
        return cls.obj_count

    @classmethod
    def createUsers(cls,n, staff= False):
        uname= 'username'
        pw= 'password'

        users= []
        for x in range(n):
            u_id  = str(cls.nextid())
            name = uname + u_id
            u = User.objects.create_user(username=name, password=pw)
            u.is_staff = staff
            u.email = "%s@forum.rog" % (uname+ u_id,)
            u.save()

            up = UserProfile.objects.create(user= u)
            users.append(u)

        return users

    @classmethod

    def createUser(cls, uname, pw, staff=False):
        u = User.objects.create_user(username= uname, password= pw)
        UserProfile.objects.create(user= u)
        u.is_staff = staff
        u.save()

        return u

class BoardFactory:
    # This number is appended to unique field values
    obj_count = 0

    @classmethod
    def nextid(cls):
        cls.obj_count +=1
        return cls.obj_count

    @classmethod
    def createBoards(cls,n):
        title = 'Board'

        boards= []
        for x in range(n):
            t = title + str(cls.nextid())
            b = Board.objects.create(title=t)
            boards.append(b)

        return boards

class PostFactory:
    # This number is appended to unique field values
    obj_count = 0

    @classmethod
    def nextid(cls):
        cls.obj_count +=1
        return cls.obj_count

    @classmethod
    def createPosts(cls, n, author=None, board= None):
        title = 'PostTitle'
        content = 'PostContent'

        if author is None:
            author = UserFactory.createUsers(1)[0]
        if board is None:
            board = BoardFactory.createBoards(1)[0]

        posts= []
        for x in range(n):
            t = title + str(cls.nextid())
            p = Post.objects.create(title=t, board= board, creator=author.userprofile)
            p.updateContent(content)
            p.save()
            posts.append(p)

        return posts


class ReplyFactory:
    # This number is appended to unique field values
    obj_count = 0

    @classmethod
    def nextid(cls):
        cls.obj_count +=1
        return cls.obj_count

    @classmethod
    def createReplies(cls, n, user=None, post=None):
        content = 'ReplyContent'

        if user is None:
            user = UserFactory.createUsers(1)[0]

        if post is None:
            post = PostFactory.createPosts(1)[0]

        replies= []
        for x in range(n):
            r = Reply.objects.create(reply_to=post, creator= user.userprofile)
            r.updateContent(content)
            r.save()
            replies.append(r)

        return replies
