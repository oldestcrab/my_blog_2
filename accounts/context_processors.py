from .forms import LoginForm

def login_modal_form(request):
    """添加全局模板变量

    :param request: request
    :return: 登录表单实例化
    """
    return {'login_modal_form': LoginForm()}