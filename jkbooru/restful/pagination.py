from flask_restful import Resource, reqparse
from jkbooru.model.post import Post


class Pagination(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'limit', default=15, type=int, location='args'
        )
        self.parser.add_argument(
            'page', default=1, type=int, location='args'
        )
        self.parser.add_argument(
            'tags', default=None, type=str, location='args'
        )
        super(Pagination, self).__init__()

    def get(self):
        args = self.parser.parse_args()

        pagination = Post.query.paginate(
            int(args['page']),
            per_page=10,
            error_out=False
        )
        return {
            'next': pagination.next_num,
            'prev': pagination.prev_num,
            'current': pagination.page,
            'total': pagination.pages,
            'per_page': pagination.per_page,
            'posts': [i.serialize for i in pagination.items]
        }
