import uuid

from rest_framework import viewsets, status
from rest_framework.response import Response

from models import Blogpost, Comments
from utils import get_formatted_response

DEFAULT_OFFSET = 0
DEFAULT_MAX_SIZE = 5

class ListBlogposts(viewsets.ViewSet):
    def get(self, request, **kwargs):
        offset = request.GET.get('offset') \
            if request.GET.get('offset') else DEFAULT_OFFSET
        max_size = request.GET.get('max_size') \
            if request.GET.get('max_size') else DEFAULT_MAX_SIZE
        # May log these values and exceptions for reference
        try:
            offset = int(offset)
        except Exception as e:
            offset = DEFAULT_OFFSET
        try:
            max_size = int(max_size)
        except Exception as e:
            max_size = DEFAULT_MAX_SIZE

        blogs = list(Blogpost.objects.all().values('identifier', 'title', 'content'
            )[offset:offset+max_size])
        for blog in blogs:
            text = blog.pop('content')
            blog['content'] = '\n\n'.join(text.values())

        return Response(data=get_formatted_response(blogs), status=status.HTTP_200_OK)


class AddBlogposts(viewsets.ViewSet):
    def post(self, request):
        resp_data = {}
        title = request.data.get('title')
        desc = request.data.get('content')
        if not (title and desc):
            resp_data['message'] = 'Invalid title/content.'
            st = status.HTTP_400_BAD_REQUEST
            return Response(data=get_formatted_response(resp_data, st, False),
                            status=st)

        content_list = desc.split('\n\n')
        content = {}
        for i in range(0, len(content_list)):
            content[i+1] = content_list[i]
        obj = Blogpost.objects.create(title=title, content=content)
        resp_data['blog_id'] = obj.identifier if obj else None

        response = get_formatted_response(resp_data, status.HTTP_201_CREATED)
        return Response(data=response, status=status.HTTP_201_CREATED)


class AddComments(viewsets.ViewSet):
    def post(self, request, **kwargs):
        blog_id = kwargs.get('blog_id')
        para = kwargs.get('para_no')
        comment = request.data.get('comment')
        try:
            blog_id = uuid.UUID(blog_id)
        except Exception as e:
            st = status.HTTP_400_BAD_REQUEST
            resp_data = {'message': 'Invalid blog id - {}'.format(blog_id)}
            return Response(data=get_formatted_response(resp_data, st, False),
                            status=st)

        blog_content = list(Blogpost.objects.filter(identifier=blog_id
            ).values_list('content', flat=True))
        if not blog_content or para not in blog_content[0].keys():
            st = status.HTTP_400_BAD_REQUEST
            resp_data = {
                'message': 'Blog id and/or para no. not found'
            }
            return Response(data=get_formatted_response(resp_data, st, False),
                            status=st)

        cid = Comments.objects.create(blog_id=blog_id, para=para, message=comment)
        resp_data = {
            'message': 'Comment added successfully.'
        }
        response = get_formatted_response(resp_data, status.HTTP_201_CREATED)
        return Response(data=response, status=status.HTTP_201_CREATED)


class GetBlogpost(viewsets.ViewSet):
    def get(self, request, **kwargs):
        blog_id = kwargs.get('blog_id')
        try:
            blog_id = uuid.UUID(blog_id)
        except Exception as e:
            st = status.HTTP_400_BAD_REQUEST
            resp_data = {'message': 'Invalid blog id: {} - {}'.format(blog_id, e)}
            return Response(data=get_formatted_response(resp_data, st, False),
                            status=st)

        blog = Blogpost.objects.get(identifier=blog_id)
        comments = list(Comments.objects.filter(blog=blog).values())
        
        content = {}
        blog_comments = []
        for k, v in blog.content.iteritems():
            content[v] = []
            blog.content[int(k)] = blog.content.pop(k)

        for comment in comments:
            if comment.get('para') == 0:
                blog_comments.append(comment.get('message'))
            else:
                content.get(blog.content.get(comment.get('para')), []
                    ).append(comment['message'])

        resp_data = {
            'blog_id': blog.identifier,
            'title': blog.title,
            'content': content,
            'comments': blog_comments
        }

        return Response(data=get_formatted_response(resp_data))
