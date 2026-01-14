"""
Custom middleware for handling dynamic Render subdomains.
Allows any host ending with .onrender.com for Render deployments.
Also allows custom domains from ALLOWED_HOSTS environment variable.
"""
from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
import os


class DynamicAllowedHostsMiddleware(MiddlewareMixin):
    """
    Middleware that validates hosts dynamically, allowing .onrender.com subdomains
    and custom domains from ALLOWED_HOSTS environment variable.
    This should be placed before CommonMiddleware in MIDDLEWARE list.
    
    When ALLOWED_HOSTS is set to ['*'] (on Render), this middleware validates
    that only .onrender.com subdomains or custom domains from env are allowed for security.
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Store original ALLOWED_HOSTS from environment before it was overwritten
        _allowed_hosts_env = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0')
        self.custom_allowed_hosts = [host.strip() for host in _allowed_hosts_env.split(',') if host.strip()]
    
    def process_request(self, request):
        # Only validate if we're on Render (ALLOWED_HOSTS contains '*')
        if '*' not in settings.ALLOWED_HOSTS:
            # Not on Render, let CommonMiddleware handle validation
            return None
        
        host = request.get_host().split(':')[0]  # Remove port if present
        
        # Check if host is in custom allowed hosts from environment
        # This handles custom domains like www.adiabatic.biz
        for allowed_host in self.custom_allowed_hosts:
            # Support wildcard patterns like *.adiabatic.biz
            if '*' in allowed_host:
                # Convert *.adiabatic.biz to .adiabatic.biz for endswith check
                domain_suffix = allowed_host.replace('*', '')
                if host.endswith(domain_suffix) or host == domain_suffix.lstrip('.'):
                    return None
            elif host == allowed_host:
                return None
        
        # On Render, allow .onrender.com subdomains
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
    Custom CSRF middleware that allows .onrender.com subdomains and custom domains dynamically.
    Extends Django's CsrfViewMiddleware to validate Render subdomains and custom domains.
    """
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Store original CSRF_TRUSTED_ORIGINS from environment
        _csrf_origins_env = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://localhost')
        self.custom_csrf_origins = [origin.strip() for origin in _csrf_origins_env.split(',') if origin.strip()]
    
    def _check_origin(self, request):
        """
        Override to allow .onrender.com subdomains and custom domains for CSRF validation.
        This method validates the Origin header against CSRF_TRUSTED_ORIGINS.
        """
        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        if origin:
            # Remove protocol and path
            origin_clean = origin.replace('https://', '').replace('http://', '').split('/')[0]
            
            # Check if origin is in custom CSRF trusted origins from environment
            for trusted_origin in self.custom_csrf_origins:
                trusted_clean = trusted_origin.replace('https://', '').replace('http://', '').split('/')[0]
                # Support wildcard patterns
                if '*' in trusted_clean:
                    domain_suffix = trusted_clean.replace('*', '')
                    if origin_clean.endswith(domain_suffix) or origin_clean == domain_suffix.lstrip('.'):
                        return True
                elif origin_clean == trusted_clean:
                    return True
            
            # Check if origin is a Render subdomain
            if origin_clean.endswith('.onrender.com'):
                return True
        
        # Also check the host header as fallback
        host = request.get_host().split(':')[0]
        
        # Check custom domains from CSRF_TRUSTED_ORIGINS
        for trusted_origin in self.custom_csrf_origins:
            trusted_clean = trusted_origin.replace('https://', '').replace('http://', '').split('/')[0]
            if '*' in trusted_clean:
                domain_suffix = trusted_clean.replace('*', '')
                if host.endswith(domain_suffix) or host == domain_suffix.lstrip('.'):
                    return True
            elif host == trusted_clean:
                return True
        
        # Check if host is a Render subdomain
        if host.endswith('.onrender.com'):
            return True
        
        # If not a Render subdomain or custom domain, use parent's origin check
        try:
            return super()._check_origin(request)
        except AttributeError:
            # If parent method doesn't exist, fall back to default Django behavior
            return False

