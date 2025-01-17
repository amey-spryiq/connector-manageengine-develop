""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """
SORT_ORDER = {
    "Ascending": "asc",
    "Descending": "desc"
}
REQUEST_ENDPOINT = '/api/v3/requests/'
REQUESTER_ENDPOINT = '/api/v3/users/'

ADD_TASK = '/api/v3/requests/{request_id}/tasks'
EDIT_TASK = '/api/v3/requests/{request_id}/tasks/{task_id}'
GET_TASK = '/api/v3/requests/{request_id}/tasks/{task_id}'
GET_LIST_TASK = '/api/v3/requests/{request_id}/tasks'


