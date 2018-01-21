from django.urls import reverse

class UrlContainer:
    @classmethod
    def getHomePageUrl(cls):
        return reverse('forum:homepage')

    @classmethod
    def getDeletePostUrl(cls):
        return reverse('forum:delete_post')

    @classmethod
    def getRestorePostUrl(cls):
        return reverse('forum:restore_post')

    @classmethod
    def getLoginPageUrl(self):
        return reverse('forum:loginpage')

    @classmethod
    def getPostDetailUrl(self, post_id):
        return  reverse('forum:post_detail', args=[post_id])

    @classmethod
    def getAboutPage(cls):
        return reverse('forum:about_page')

    @classmethod
    def getRegisterPage(cls):
        return reverse('forum:registration_page')

    @classmethod
    def getUserDetailUrl(cls, user_id):
        return reverse('forum:user_detail', args=[user_id])

    @classmethod
    def getDeletedPostsUrl(cls):
        return reverse('forum:deleted_posts')

    @classmethod
    def getDeleteReplyUrl(cls):
        return reverse('forum:delete_reply')

    @classmethod
    def getEditPostUrl(cls):
        return reverse('forum:edit_post')

    @classmethod
    def getCreatePostUrl(cls):
        return reverse('forum:create_post')

    @classmethod
    def getMarkDownToHtmlUrl(cls):
        return reverse('forum:markdown_to_html')

    @classmethod
    def getEditUserProfileUrl(cls, user_id):
        return reverse('forum:edit_user', args=[user_id])

    @classmethod
    def getCreateReplyUrl(cls):
        return reverse('forum:create_reply')

    @classmethod
    def getEditReplyUrl(cls):
        return reverse('forum:edit_reply')


class TemplateNames:
    edit_reply_editor = 'forum/edit_reply_editor.html'
    user_profile_editor = 'forum/edit_user_editor.html'
    home_page= 'forum/home_page.html'
    about_page= 'forum/about_page.html'
    login_page = 'forum/login_page.html'
    board_posts= 'forum/board_posts.html'
    user_detail = 'forum/user_detail.html'
    post_detail = 'forum/post_detail.html'
    show_message = 'forum/show_message.html'
    deleted_posts= 'forum/deleted_posts.html'
    edit_post_editor= 'forum/edit_post_editor.html'
    registration_page = 'forum/registration_page.html'
    create_post_editor= 'forum/create_post_editor.html'
    global_base_template= 'forum/global_base_template.html'
    layout_base_template= 'forum/layout_base_template.html'
