# *-* coding: utf-8 *-*
# Maintainers:
# Ahmet Küçük <ahmetkucuk4@gmail.com>
# Zekeriya Akgül <zkry.akgul@gmail.com>

from app import app
from flask import Response, Blueprint, request, jsonify, session
from app.api.models import User
from app.auth.utils import login_smtp, create_imap_account, create_gmail_account, create_microsoft_account, delete_account
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

import os
import requests
import traceback

class MailApi(Resource):

    API_LIST = [
        "events",
        "calenders",
        "drafts",
        "sends",
        "folders",
        "labels",
        "messages",
        "threads",
        "contacts"
    ]
    
    @jwt_required
    def dispatch_request(self, *args, **kwargs):

        api_name = kwargs['api']

        if not api_name.split('/')[0] in self.API_LIST:
            resp =  jsonify({'status': False})
            resp.status_code = 404
            return resp

        account_id = session.get('account_id', False)

        if not account_id:
            resp =  jsonify({'status': False, 'code': 'MA-100', 'content': 'Could not verify authorization credentials'})
            resp.status_code = 500
            return resp

        URL = os.path.join(app.config['SYNC_ENGINE_API_URL'], api_name)

        requests_args = {}
        headers = dict(request.headers)
        params = request.args.copy()

        for key in list(headers.keys()):
            if key.lower() == 'content-length':
                del headers[key]

        requests_args['data'] = request.data
        requests_args['headers'] = headers
        requests_args['params'] = params
        requests_args['auth'] = requests.auth.HTTPBasicAuth(account_id, '')

        response = requests.request(request.method, URL, **requests_args)

        proxy_response = Response(
            response.content,
            status=response.status_code,
            mimetype='application/json'
        )

        return proxy_response

class AccountApi(Resource):

    @jwt_required
    def get(self):
        return jsonify({'test': 'success', 'status': True}, mimetype="application/json", status_code=200)

    # @jwt_required
    def post(self):
        if not request.is_json:
            resp = jsonify({'status': False, "content": "Missing JSON in request"})
            resp.status_code = 400
            return resp
        
        body = request.get_json()

        username = body.get('username', '')
        account_type = body.get('account_type', '') # generic,gmail,microsoft
        email = body.get('email', '')

        if not username or not account_type:
            resp = jsonify({'status': False, 'code': 'AA-100', 'content': 'User credentials are missing'})
            resp.status_code = 400
            return resp

        user = User.query.filter_by(username=username).first()
        if not user.has_account(email):
            try:
                if account_type == "generic":
                    password = body.get('password', '')
                    create_imap_account(username, email, password, body)
                    resp = jsonify({'status': True, 'code': 'AA-101', 'content': 'New account was added'})
                    resp.status_code = 200
                    return resp
                elif account_type == "gmail":
                    create_gmail_account(username, email, body)
                    resp = jsonify({'status': True, 'code': 'AA-101', 'content': 'New account was added'})
                    resp.status_code = 200
                    return resp
                elif account_type == "microsoft":
                    create_microsoft_account(username, email, body)
                    resp = jsonify({'status': True, 'code': 'AA-101', 'content': 'New account was added'})
                    resp.status_code = 200
                    return resp
            except Exception as e:
                traceback.print_exc()
                resp = jsonify({'status': False, 'code': 'AA-102', 'content': 'Something went wrong while adding new account'})
                resp.status_code = 500
                return resp 
        else:
            resp =  jsonify({'status': False, 'code': 'AA-103', 'content': 'User already have this account'})
            resp.status_code = 500
            return resp

    @jwt_required
    def put(self):
        if not request.is_json:
            resp = jsonify({'status': False, "content": "Missing JSON in request"})
            resp.status_code = 400
            return resp
        return Response({'test': 'success', 'status': True}, mimetype="application/json", status=200)

    # @jwt_required
    def delete(self):
        if not request.is_json:
            resp = jsonify({'status': False, "content": "Missing JSON in request"})
            resp.status_code = 400
            return resp
        
        body = request.get_json()

        username = body.get('username', '')
        email = body.get('email', '')
        user = User.query.filter_by(username=username).first()

        if not user.has_account(email):
            resp = jsonify({'status': False, 'code': 'AD-100', 'content': 'User does not have this account'})
            resp.status_code = 400
            return resp 

        status = delete_account(owner_username=username, email=email)

        if status:
            resp = jsonify({'status': True, 'code': 'AD-101', 'content': 'Account is successfully deleted'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'status': False, 'code': 'AD-102', 'content': 'Something went wrong while deleting account'})
            resp.status_code = 500
            return resp 