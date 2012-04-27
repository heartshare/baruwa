#
# Baruwa - Web 2.0 MailScanner front-end.
# Copyright (C) 2010-2012  Andrew Colin Kissa <andrew@topdog.za.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# vim: ai ts=4 sts=4 et sw=4
#


from django.conf.urls.defaults import patterns, include, handler500, handler404

urlpatterns = patterns('baruwa.web.visits.views',
    (r'^$', 'index', {}, 'main-visits-index'),
    (r'^(?P<view_type>(full|url|virus|search))/$', 'index', {'list_all': 1}, 'all-visits-index'),
    (r'^(?P<view_type>(full|url|virus|search))/(?P<direction>(dsc|asc))/(?P<order_by>(id|date|hostname|username|site|category|size))/$',
    'index', {'list_all': 1}, 'all-visits-list'),
    (r'^(?P<view_type>(full|url|virus|search))/(?P<page>([0-9]+|last))/$', 'index', {'list_all': 1}, 'all-visits-page'),
    (r'^(?P<view_type>(full|url|virus|search))/(?P<page>([0-9]+|last))/(?P<direction>(dsc|asc))/(?P<order_by>(id|date|hostname|username|site|category|size))/$',
    'index', {'list_all': 1}, 'sorted-visits-page'),
    (r'^view/(?P<visit_id>(\d+))/$', 'detail', {}, 'visit-detail'),
)