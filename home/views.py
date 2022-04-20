from django.shortcuts import render
from plotly.offline import plot
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
import plotly.graph_objects as go
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(redirect_field_name='login')
def home(request):
	def scatter():
		x1 = [1, 2, 3, 4]
		y1 = [38, 35, 25, 45]

		trace = go.Scatter(
			x=x1,
			y=y1
		)
		layout = dict(
			title='Simple Graph',
			xaxis=dict(range=[min(x1), max(x1)]),
			yaxis=dict(range=[min(y1), max(y1)])
		)
		fig = go.Figure(data=[trace], layout=layout)
		plot_div = plot(fig, output_type='div', include_plotlyjs=False)
		return plot_div

	context = {
		'plot': scatter()
	}
	return render(request, 'welcome.html', context)


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('students:course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result
