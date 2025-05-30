from datetime import timedelta
import os
from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# from dotenv import load_dotenv
# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s$io6_xls$2hgu)%n(8w8&4pfiw0-vzju-ow!^b(2h2*wc!m3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'accounts',  # Make sure this is here
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_multiple_model',
    'tinymce',
    'home',
    'about',
    'blog',
    'orders',
    'ntc',
    'koshiinvest',
    'django_summernote',
    'solo',
    'corsheaders',
    'baliyo',
    'finance_management',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yachu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'yachu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "yachu",
        "USER": "vishal",
        "PASSWORD": "DatabaseUserPassword",
        "HOST": "localhost",
        "PORT": "",
    }
}

DATA_UPLOAD_MAX_MEMORY_SIZE = None


AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

CKEDITOR_UPLOAD_PATH = 'uploads/'

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')
CORS_ALLOW_ALL_ORIGINS = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = "SAMEORIGIN"

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Hikingbees Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Hikingbees",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Hikingbees",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Hikingbees Admin",
    # Copyright on the footer
    "copyright": "Baliyo Software",
    "search_model": ["blog.post", "activity.activity"],
    # Field name on user model that contains avatar FileField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["home", "activity", "blog"],
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
}

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'toolbar': [
            ['style', ['style',]],
            ['font', ['fontname', 'fontsize', 'bold',
                      'italic', 'strikethrough', 'clear',]],
            ['color', ['forecolor', 'backcolor', ]],
            ['para', ['ul', 'ol', 'height']],
            ['insert', ['link']],
            ['misc', ['picture', 'fullscreen', 'codeview', 'print', 'help', ]],
        ],
        'fontNames': ['Roboto'],
    }
}
SUMMERNOTE_THEME = 'bs4'

TINYMCE_DEFAULT_CONFIG = {
    "height": "780",
    "width": "780",
    "entity_encoding": "raw",
    "menubar": "file edit view insert format tools table help",
    "plugins": 'print preview paste importcss searchreplace autolink autosave save code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap emoticons quickbars',
    "toolbar": "fullscreen preview | undo redo | bold italic forecolor backcolor | formatselect | image link | "
    "alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | fontsizeselect "
    "emoticons | ",
    "custom_undo_redo_levels": 50,
    "quickbars_insert_toolbar": False,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "content_style": "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }",
}
CORS_ALLOWED_ORIGINS = [
    "https://commander-stages-bridges-conventions.trycloudflare.com",
]
CSRF_TRUSTED_ORIGINS = [
    'https://commander-stages-bridges-conventions.trycloudflare.com']

UNFOLD = {
    "SITE_HEADER": _("Yachu Admin"),
    "SITE_TITLE": _("Yachu Admin"),
    "THEME": "dark",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation_expanded": True,
        "navigation": [
            {
                "title": _("Basic"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:accounts_customuser_changelist"),
                    },
                ],
            },

            {
                "title": _("Blog and Event"),
                "separator": True,
                "items": [
                    {
                        "title": _("Blogs"),
                        "icon": "post",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:blog_post_changelist"),
                    },
                    {
                        "title": _("Events"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:blog_event_changelist"),
                    },
                ],
            },
            {
                "title": _("Site Management"),
                "separator": True,
                "items": [
                    {
                        "title": _("Site Configuration"),
                        "icon": "list",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_siteconfiguration_change", args=[1]),
                    },
                    {
                        "title": _("FAQ"),
                        "icon": "help",
                        "link": reverse_lazy("admin:home_faq_changelist"),
                    },
                    {
                        "title": _("Team members"),
                        "icon": "people",
                        "link": reverse_lazy("admin:home_teammember_changelist"),
                    },
                    {
                        "title": _("Testimonial"),
                        "icon": "wc",
                        "link": reverse_lazy("admin:home_testimonial_changelist"),
                    },
                    {
                        "title": _("Banners"),
                        "icon": "web",
                        "link": reverse_lazy("admin:home_banners_changelist"),
                    },
                    {
                        "title": _("Image gallery"),
                        "icon": "gallery_thumbnail",
                        "link": reverse_lazy("admin:home_imagegallery_changelist"),
                    },
                    {
                        "title": _("Video gallery"),
                        "icon": "sort",
                        "link": reverse_lazy("admin:home_videogallery_changelist"),
                    },
                    {
                        "title": _("Products"),
                        "icon": "add_box",
                        "link": reverse_lazy("admin:home_product_changelist"),
                    },
                    {
                        "title": _("Franchise"),
                        "icon": "people",
                        "link": reverse_lazy("admin:about_franchise_changelist"),
                    },
                ],
            },
        ],
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

""" # DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
 """


# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.resend.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'resend'
# EMAIL_HOST_PASSWORD = os.getenv("RESEND_APIKEY", default="")

# DEFAULT_FROM_EMAIL = 'Baliyo Ventures <info@baliyoventures.com>'
# SERVER_EMAIL = 'info@baliyoventures.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'biratexpo2025@gmail.com'
EMAIL_HOST_PASSWORD = 'bokk emuw glri hybr'

DEFAULT_FROM_EMAIL = 'Birat Expo 2025 <biratexpo2025@gmail.com>'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
}
