from apps.user_app.models import User


class UserProfileController:
    @staticmethod
    def get_user_profile(user_id):
        user = User.get_user_by_id(user_id=user_id)
        user_profile_data = {
            'avatar': user.avatar if user.avatar else 'http://localhost:5000/static/images/user_avatar.png',
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'capacity': user.capacity
        }
        return user_profile_data
