from django.shortcuts import render


def privacy_policy_view(request):
    template = "includes/privacy_policy.html"
    return render(request,template)