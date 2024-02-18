# -*- coding: utf-8 -*-
# from odoo import http


# class Musictracker(http.Controller):
#     @http.route('/musictracker/musictracker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/musictracker/musictracker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('musictracker.listing', {
#             'root': '/musictracker/musictracker',
#             'objects': http.request.env['musictracker.musictracker'].search([]),
#         })

#     @http.route('/musictracker/musictracker/objects/<model("musictracker.musictracker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('musictracker.object', {
#             'object': obj
#         })
