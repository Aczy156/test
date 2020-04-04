
class todo:
    def __init__(self ,id ,text ,done ,user_id):
        self.id = id
        self.text = text
        self.done = done
        self.user_id = user_id

    # return {k: getattr(self, k) for k in ('id', 'text', 'done')}
    def to_json(self):
        return ''
