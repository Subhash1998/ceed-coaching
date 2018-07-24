from allauth.account.adapter import DefaultAccountAdapter

master_url = '/mysite/dashboard/'
student_url = '/student/student_dashboard/'


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        url = super(AccountAdapter, self).get_login_redirect_url(request)
        user = request.user
        if user.user_type == "master":
            url = master_url
        elif user.user_type == "Others":
            url = student_url

        return url