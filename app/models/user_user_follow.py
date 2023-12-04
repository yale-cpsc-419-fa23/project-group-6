from app import db


class UserUserFollow(db.Model):
    UserId1 = db.Column(db.Integer, db.ForeignKey('user.UserId'), primary_key=True)
    UserId2 = db.Column(db.Integer, db.ForeignKey('user.UserId'), primary_key=True)

    def get_follower(self):
        return self.follower

    def get_followed(self):
        return self.followed
