class ProtectAdminMiddleware(object):
	def process_request(self, request):
		if request.path.startswith("/admin") and request.META["SERVER_PORT"] != "8000":
			raise Http404