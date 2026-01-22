from django.urls import path, include
from basic_app.views import (
    PostList,
    AboutView,
    PostDetail,
    CreatePost,
    UpdatePost,
    DeletePost,
    DraftList,
    createComment,
    commentApprove,
    commentRemove,
    postPublish,
    postDetail,
    banUser,
)

app_name = "blog"
urlpatterns = [
    path("", PostList.as_view(), name="list"),
    path("draft", DraftList.as_view(), name="drafts"),
    path("about", AboutView.as_view(), name="about"),
    path("postdetail/<int:pk>", PostDetail.as_view(), name="detail"),
    path("postdelete/<int:pk>", DeletePost.as_view(), name="delete"),
    path("update/<int:pk>", UpdatePost.as_view(), name="update"),
    path("createPost", CreatePost.as_view(), name="createPost"),
    path("postPublish/<int:pk>", postPublish, name="postPublish"),
    path("createComment/<int:pk>", createComment, name="createComment"),
    path("commentApprove/<int:pk>", commentApprove, name="commentApprove"),
    path("commentRemove/<int:pk>", commentRemove, name="commentRemove"),
    path("ban/<int:userpk>/<int:postpk>", banUser, name="ban"),
]
