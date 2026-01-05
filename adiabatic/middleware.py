"""
Custom middleware for handling dynamic Render subdomains.
Allows any host ending with .onrender.com for Render deployments.
"""
from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
import os


class DynamicAllowedHostsMiddleware(MiddlewareMixin):
    """
    Middleware that validates hosts dynamically, allowing .onrender.com subdomains.
    This should be placed before CommonMiddleware in MIDDLEWARE list.
    
    When ALLOWED_HOSTS is set to ['*'] (on Render), this middleware validates
    that only .onrender.com subdomains are allowed for security.
    """
    
    def process_request(self, request):
        # Only validate if we're on Render (ALLOWED_HOSTS contains '*')
        if '*' not in settings.ALLOWED_HOSTS:
            # Not on Render, let CommonMiddleware handle validation
            return None
        
        host = request.get_host().split(':')[0]  # Remove port if present
        
        # On Render, only allow .onrender.com subdomains
        if host.endswith('.onrender.com'):
            # Valid Render host
            return None
        
        # Also allow localhost for health checks and internal requests
        if host in ['localhost', '127.0.0.1', '0.0.0.0']:
            return None
        
        # Invalid host - reject the request
        return HttpResponseBadRequest(
            "Invalid HTTP_HOST header. You may need to add %r to ALLOWED_HOSTS." % host
        )


class DynamicCsrfMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that allows .onrender.com subdomains dynamically.
    Extends Django's CsrfViewMiddleware to validate Render subdomains.
    """
    
    def _check_origin(self, request):
        """
        Override to allow .onrender.com subdomains for CSRF validation.
        This method validates the Origin header against CSRF_TRUSTED_ORIGINS.
        """
        # Check if origin is a Render subdomain first
        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        if origin:
            # Remove protocol and check if it's a .onrender.com subdomain
            origin_clean = origin.replace('https://', '').replace('http://', '').split('/')[0]
            if origin_clean.endswith('.onrender.com'):
                return True
        
        # Also check the host header as fallback
        host = request.get_host().split(':')[0]
        if host.endswith('.onrender.com'):
            return True
        
        # If not a Render subdomain, use parent's origin check
        try:
            return super()._check_origin(request)
        except AttributeError:
            # If parent method doesn't exist, fall back to default Django behavior
            # by not overriding (let Django handle it)
            # But we've already checked Render subdomains, so if we get here
            # and it's not a Render subdomain, we should reject
            return False

