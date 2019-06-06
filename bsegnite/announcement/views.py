from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Announcement, Company, Category, Subcategory, Custom, Customcat, Customsubcat
from django.contrib.auth import(authenticate,
	get_user_model,
	login,
	logout,
	)
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .form import SignupForm,DateChoose,LoginForm
from django.views.decorators.csrf import csrf_exempt



from django.http import HttpResponse
from django.core.mail import EmailMessage

from dal import autocomplete
from django.shortcuts import render_to_response
from django.views.decorators.http import condition
from django.http import StreamingHttpResponse
import json
from django.http import JsonResponse
from django.core import serializers
# from .forms import UserLoginForm

from django.template import loader, Context

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import time
# datetime_object = datetime.datetime.strptime('Jan 5 2019', '%b %d %Y')
# today_min = datetime.datetime.combine(datetime_object, datetime.time.min)
# today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

# today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
# today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
@csrf_exempt
def post_announcement(request):
	

	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	# def get_form(self):
	# 	form = get_form(DateChoose)
	# 	form.fields['pub_date'].widget = DateTimePickerInput()
	# 	return form
	form = DateChoose()
	# forms = CompanyForm()
	# catchoices = None
	subcatchoices = None
	# check = None
	viewsubcat = None

	if request.method == 'POST':
		form = DateChoose(request.POST)
		# forms = CompanyForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			start = form.cleaned_data.get('start_date')
			end = form.cleaned_data.get('end_date')
			# choices = form.cleaned_data.get('categories')
			data = request.POST.copy()
			catchoices = data.getlist('categorylist')
			print(catchoices)
			subcatchoices = data.getlist('subcategorylist')
			if start and end:
				today_min = datetime.datetime.combine(start,datetime.time.min)
				today_max = datetime.datetime.combine(end,datetime.time.max) 
	print("hello 1st")
	query = Announcement.objects.filter(ca_datetime__range=(today_min, today_max)).order_by('-ca_datetime')
	print("Hello 2nd")
	totsubcat= 0
	countsubcat = dict()
	for r in range(1,50):
		countsubcat[r] = query.filter(su_id = r).count()
		totsubcat = totsubcat + countsubcat[r]

	if subcatchoices:
		query_set = list()
		query_set = query.filter(su_id__in = subcatchoices)
		viewsubcat = Subcategory.objects.filter(su_id__in = subcatchoices)

	else:
		query_set = query
	def gen():
		yield t.render(context_data,request)
		if viewsubcat:
			cat = ''
			for i in viewsubcat:
				cat = cat + "{} | ".format(i.su_name)
		else:
			cat = "ALL"
		string = '<div class="card mb-3"><div class="card-header"><i class="fas fa-table"></i>Viewing : <b>{}</b></div><div class="card-body"><div class="table-responsive" id="dvData"><table class="table table-bordered" id="dataTable" width="100%" cellspacing="0" data-order = \'[[4, "desc"]]\'><thead><tr><th>Head</th><th>Description</th><th>Company</th><th>Date</th><th>Pdf</th></tr></thead><tfoot><tr><th>Head</th><th>Description</th><th>Company</th><th>Date</th><th>Pdf</th></tr></tfoot>'.format(cat)
		yield string
		for x in query_set:
			# date = x.ca_datetime
			# objDate = datetime.datetime.strptime(x.ca_datetime, '%m/%d/%y')
			date = datetime.datetime.strftime(x.ca_datetime,'%Y/%m/%d %H:%M')
			if x.ca_data:
				yield '<tr><td>{}</td><td>{}</td><td><a href="/company/{}">{}</a></td><td width=170vw>{}</td><td><a href={} target="_blank"><i class="icon-file-pdf"></i></a></td></tr>'.format(x.ca_head,x.ca_desc,x.c_id,x.c,date,x.ca_data)
			else:
				yield '<tr><td>{}</td><td>{}</td><td><a href="/company/{}">{}</a></td><td width=170vw>{}</td><td></td></tr>'.format(x.ca_head,x.ca_desc,x.c_id,x.c,date)	
		yield '<script type="text/javascript">$(\'#dataTable\').dataTable( {"sDom": \'<"wrapper"lfptip>\',} );</script>'
	context_data={
		"form":form,
		"countsubcat":countsubcat,
		"totcountsubcat":totsubcat,
		"checkingsubcat": subcatchoices,
		"viewingsubcat" :viewsubcat,
	}
	t = get_template('index.html')
	
	response = StreamingHttpResponse(gen())
	return response
		# "forms":forms,
		# "countcat":count,
		# "checkingcat": catchoices,
		# "form":get_form(),	
	# }
	# t = loader.get_template('index.html')
	# print(type(t))
	 

	# response = HttpResponse(index.html)
	# response["query_set"] = [gen()]
	# return response
	# return render(request,"index.html",context_data)
	# return StreamingHttpResponse(gen(),  status=200, content_type='text/event-stream')
	# context_data = serializers.serialize('json', context_data)
	# print(type(context_data))

	# return HttpResponse(context_data, content_type='application/json')

	# return JsonResponse(context_data, safe=False)
	# context_data = json.dumps(query_set)
	# context_data = json.loads(context_data)
	# for i in range(0,query_set.count(),1000):
	# 	try:
	# 		yield render(request,"index.html",{"query_set" : query_set[i-1000:i], "form": form ,"checkingsubcat": subcatchoices,
	# 	"viewingsubcat" :viewsubcat,
	# 	"countsubcat":countsubcat,
	# 	"totcountsubcat":totsubcat,} )
	# 	except:
	# 		pass
	# return StreamingHttpResponse(request,"index.html",query_set)
	# return render(request,"index.html",context_data)
	# return form

def post_chart(request):
	return render(request,"charts.html")

def post_company_ann(request, cid):
	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
	
	form = DateChoose()

	subcatchoices = None

	viewsubcat = None

	if request.method == 'POST':
		form = DateChoose(request.POST)
		# forms = CompanyForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			start = form.cleaned_data.get('start_date')
			end = form.cleaned_data.get('end_date')
			# choices = form.cleaned_data.get('categories')
			data = request.POST.copy()
			catchoices = data.getlist('categorylist')
			print(catchoices)
			subcatchoices = data.getlist('subcategorylist')
			if start and end:
				today_min = datetime.datetime.combine(start,datetime.time.min)
				today_max = datetime.datetime.combine(end,datetime.time.max) 
	queryset=Announcement.objects.filter(c_id= cid).order_by('-ca_datetime')
	query = queryset.filter(ca_datetime__range=(today_min, today_max)).order_by('-ca_datetime')

	totsubcat=0
	countsubcat = {}
	for r in range(1,50):
		countsubcat[r] = query.filter(su_id = r).count()
		totsubcat = totsubcat + countsubcat[r]

	if subcatchoices:
		query_set = []
		query_set = query.filter(su_id__in = subcatchoices)
		viewsubcat = Subcategory.objects.filter(su_id__in = subcatchoices)

	else:
		query_set = query

	companyname = Company.objects.filter(c_id = cid)
	context_data={
		"query_set":query_set,
		"form":form,
		# "forms":forms,
		# "countcat":count,
		"countsubcat":countsubcat,
		"totcountsubcat":totsubcat,
		# "checkingcat": catchoices,
		"checkingsubcat": subcatchoices,
		"viewingsubcat" :viewsubcat,
		"companydetails" : companyname[0],
		# "form":get_form(),
	}
	
	return render(request,"company_ann.html",context_data)
	return form

def post_tables(request):
	# queryset=Announcement.objects.filter(ca_datetime__range=(today_min, today_max)).order_by('-ca_datetime')
	context_data={
		# "query_set":queryset,
	}
	return render(request,"tables.html",context_data)

def post_company(request):
	queryset=Company.objects.all()
	context_data={
		"query_set":queryset,
	}
	return render(request,"company.html",context_data)

def post_forgotpassword(request):
	return render(request,"forgotpassword.html",{})

def post_logout(request):
	logout(request)
	return redirect("/")		


def post_customize(request):
	if request.method == 'POST':
		try:
			if request.POST['add']:
				to_add = request.POST['add']
			print(to_add)
			print(request.POST['add'])
		except:
			pass
		try:
			if request.POST['remove']:
				to_remove = request.POST['remove']
		except:
			pass
		try:
			if request.POST['addcompcat']:
				to_add_cat = request.POST['addcompcat']
		except:
			pass
		try:
			if request.POST['removecompcat']:
				to_remove_cat = request.POST['removecompcat']
		except:
			pass
		try:
			if request.POST['addcat']:
				to_add_main_cat = request.POST['addcat']
		except:
			pass
		try:
			if request.POST['removecat']:
				to_remove_main_cat = request.POST['removecat']
		except:
			pass
		try:
			if to_add:
				# adding company to custom
				Custom.objects.create(u_id=request.user.id, c_id = to_add)
		except:
			pass
		try:
			if to_remove:
				trying = Custom.objects.filter(c_id = to_remove, u_id=request.user.id).delete()
				print(trying)
				#removing company from custo
		except:
			pass
		try:
			if to_add_cat:
				# adding company to custom
				Customsubcat.objects.create(u_id=request.user.id, su_id = to_add_cat)
		except:
			pass
		try:
			if to_remove_cat:
				Customsubcat.objects.filter(su_id = to_remove_cat, u_id=request.user.id).delete()
				#removing company from custo
		except:
			pass
		try:
			if to_add_main_cat:
				# adding company to custom
				Customcat.objects.create(u_id=request.user.id, su_id = to_add_main_cat)
		except:
			pass
		try:
			if to_remove_main_cat:
				Customcat.objects.filter(su_id = to_remove_main_cat, u_id=request.user.id).delete()
				#removing company from custo
		except:
			pass
	queryset=Company.objects.all()
	custom_queryset = Custom.objects.filter(u_id = request.user.id)
	fav_company = queryset.filter(c_id__in= custom_queryset.values('c_id'))
	fav_company_count = fav_company.count()
	print(fav_company_count)
	to_add_company = queryset.exclude(c_id__in= custom_queryset.values('c_id'))

	categoryquery = Subcategory.objects.all()
	cat_query = Customsubcat.objects.filter(u_id = request.user.id)
	fav_category = categoryquery.filter(su_id__in = cat_query.values('su_id'))
	to_add_category = categoryquery.exclude(su_id__in = cat_query.values('su_id'))

	main_cat_query = Customcat.objects.filter(u_id = request.user.id)
	fav_main_category = categoryquery.filter(su_id__in = main_cat_query.values('su_id'))
	to_add_main_category = categoryquery.exclude(su_id__in = main_cat_query.values('su_id'))
	
	context_data={
		"to_add_company":to_add_company,
		"fav_company" : fav_company,
		"fav_company_count" : fav_company_count,
		"to_add_category":to_add_category,
		"fav_category" : fav_category,
		"to_add_main_category":to_add_main_category,
		"fav_main_category" : fav_main_category,
	}
	return render(request,"customize.html",context_data)

def post_login(request):
	if request.method == 'POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			password = form.cleaned_data.get("password")
			user = authenticate(username = email, password = password)
			if user is not None:
				login(request,user)
				return redirect('/')
			else:
				message = "Invalid Email id or Password. Please Try Again!!"
				return render(request,"login.html",{'form':form,'message':message})

	else:
		form = LoginForm()
	return render(request,"login.html",{'form':form})

def post_register(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			to_email = form.cleaned_data.get('email')
			user.username = to_email
			user_list=User.objects.all()
			for query in user_list:
				if user.username in query.username:
					error = "Email Already Exists . "
					return render(request, 'register.html', {'form': form,'error':error})
			user.save()
			current_site = get_current_site(request)
			message = render_to_string('account_activation_email.html', {
				'user':user, 
				'domain':current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
			})
			mail_subject = 'Activate your account.'
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			messages = 'Please confirm your email address to complete the registration'
			return render(request, 'register.html', {'form': form,'message':messages})
			# return HttpResponse('Please confirm your email address to complete the registration')
	else:
		form = SignupForm()
	return render(request, 'register.html', {'form': form})

# def account_activation_sent(request):
#     return render(request, "account_activation_sent.html")


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		print(uid)
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		login(request, user)
		return redirect('/')
	else:
		return HttpResponse('Activation link is invalid!')

def dashboard(request):
	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

	query = Announcement.objects.filter(ca_datetime__range=(today_min, today_max)).order_by('-ca_datetime')

	if request.user.is_authenticated:
		query_set_company = []
		query_set_category = []
		custom_queryset = Custom.objects.filter(u_id = request.user.id)
		customsubcat_queryset = Customsubcat.objects.filter(u_id = request.user.id)
		customcat_queryset = Customcat.objects.filter(u_id = request.user.id)
		query_set_company = query.filter(c_id__in= custom_queryset.values('c_id'))
		if customsubcat_queryset:
			query_set_company = query_set_company.filter(su_id__in= customsubcat_queryset.values('su_id'))
		query_set_category = query.filter(su_id__in= customcat_queryset.values('su_id'))
		query_set = query_set_company | query_set_category
		context_data={
			"query_set":query_set,
		}
	return render(request,"dashboard.html",context_data)

def dashboard(request):
	today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
	today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

	query = Announcement.objects.filter(ca_datetime__range=(today_min, today_max)).order_by('-ca_datetime')

	if request.user.is_authenticated:
		query_set_company = []
		query_set_category = []
		custom_queryset = Custom.objects.filter(u_id = request.user.id)
		customsubcat_queryset = Customsubcat.objects.filter(u_id = request.user.id)
		customcat_queryset = Customcat.objects.filter(u_id = request.user.id)
		query_set_company = query.filter(c_id__in= custom_queryset.values('c_id'))
		if customsubcat_queryset:
			query_set_company = query_set_company.filter(su_id__in= customsubcat_queryset.values('su_id'))
		query_set_category = query.filter(su_id__in= customcat_queryset.values('su_id'))
		query_set = query_set_company | query_set_category
		context_data={
			"query_set":query_set,
		}
	return render(request,"dashboard.html",context_data)		

# class CompanyAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         # if not self.request.user.is_authenticated():
#         #     return Company.objects.none()
#         if request.method == 'POST':
#             form = CompanyForm(request.POST)
#         else:
#         	form = CompanyForm()
#         qs = Company.objects.all()

#         if self.q:
#             qs = qs.filter(c_name__icontains=self.q)
#         return render(request,"index.html",{'forms':form,'qs':qs})

def search_companies(request):
	try: 
		if request.method == 'POST':
			search_company = request.POST['search_company']
		else:
			search_company = ''
		if search_company:
			companies_query1 = Company.objects.filter(c_name__icontains = search_company)
			companies_query2 = Company.objects.filter(c_id__istartswith = search_company)
			companies_query3 = Company.objects.filter(c_indus__icontains = search_company)
			companies_query4 = Company.objects.filter(c_acro__icontains = search_company)
			companies = companies_query1 | companies_query2 | companies_query3 |companies_query4
			companies = companies[:5]
			return render_to_response('ajax_search.html',{'companies':companies})
		else:
			companies = "No match found"
			return render(request,'ajax_search.html',{'companies':companies})

	except:
		return render(request,'ajax_search.html',{})

# def search_company(request):
# 	if request.methods == 'POST':
# 		search_result = request.POST['search_company']
# 	else:
# 		search_result = ""

# 	result = Company.objects.filter(c_id__contains=search_result)

# 	return render(request,'ajax_search.html',{'results': result})

def aboutus(request):
	return render(request,'about.html', {})