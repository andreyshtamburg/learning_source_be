from flask_restplus import Resource, Namespace

ls_ns = Namespace('ls')


@ls_ns.route("/test")
class Source(Resource):

    @ls_ns.doc(validate=True)
    def get(self):
        return "Hello"
