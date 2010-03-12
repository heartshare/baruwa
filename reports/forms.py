# vim: ai ts=4 sts=4 et sw=4

from django import forms
from django.forms.fields import email_re
#from reports.views import d_query

FILTER_ITEMS = (
    ('id','Message ID'),
    ('size','Size'),
    ('from_address','From Address'),
    ('from_domain', 'From Domain'),
    ('to_address','To Address'),
    ('to_domain','To Domain'),
    ('subject','Subject'),
    ('clientip','Received from'),
    ('archive','Is Archived'),
    ('isspam','Is spam'),
    ('ishighspam','Is high spam'),
    ('issaspam','Is SA spam'),
    ('isrblspam','Is RBL listed'),
    ('spamwhitelisted','Is whitelisted'),
    ('spamblacklisted','Is blacklisted'),
    ('sascore','SA score'),
    ('spamreport','Spam report'),
    ('virusinfected','Is virus infected'),
    ('nameinfected','Is name infected'),
    ('otherinfected','Is other infected'),
    ('ismcp','Is MCP'),
    ('ishighmcp','Is high MCP'),
    ('issamcp','Is SA MCP'),
    ('mcpwhitelisted','Is mcp whitelisted'),
    ('mcpblacklisted','Is mcp blacklisted'),
    ('mcpsascore','MCP SA score'),
    ('mcpreport','MCP report'),
    ('date','Date'),
    ('time','Time'),
    ('headers','Headers'),
    ('quarantined','Is quarantined'),
)

FILTER_BY = (
    (1,'is equal to'),
    (2,'is not equal to'),
    (3,'is greater than'),
    (4,'is less than'),
    (5,'contains'),
    (6,'does not contain'),
    (7,'matches regex'),
    (8,'does not match regex'),
    (9,'is null'),
    (10,'is not null'),
    (11,'is true'),
    (12,'is false'),
)

EMPTY_VALUES = (None, '')

BOOL_FIELDS = ["archive","isspam","ishighspam","issaspam","isrblspam","spamwhitelisted","spamblacklisted","virusinfected","nameinfected","otherinfected","ismcp","ishighmcp","issamcp","mcpwhitelisted","mcpblacklisted","quarantined"]
NUM_FIELDS = ["size","sascore","mcpscore"]
TEXT_FIELDS = ["id","from_address","from_domain","to_address","to_domain","subject","clientip","spamreport","mcpreport","headers"]
TIME_FIELDS = ["date","time"]

BOOL_FILTER = [11,12]
NUM_FILTER = [1,2,3,4]
TEXT_FILTER = [1,2,5,6,7,89,10]
TIME_FILTER = [1,2,3,4]

def to_dict(tuple_list):
    d = {}
    for i in tuple_list:
        d[i[0]] = i[1]
    return d

class FilterForm(forms.Form):
    filtered_field = forms.ChoiceField(choices=FILTER_ITEMS)
    filtered_by = forms.ChoiceField(choices=FILTER_BY)
    filtered_value = forms.CharField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        submited_field = cleaned_data.get('filtered_field')
        submited_by = int(cleaned_data.get('filtered_by'))
        submited_value = cleaned_data.get('filtered_value')
        if submited_by != 0:
            sbi = (submited_by - 1)
        else:
            sbi = submited_by

        if submited_field in BOOL_FIELDS:
            if not submited_by in BOOL_FILTER:
                filter_items = to_dict(list(FILTER_ITEMS))
                e = "%s does not support the %s filter" % (filter_items[submited_field],FILTER_BY[sbi][1])
                raise forms.ValidationError(e)
        if submited_field in NUM_FIELDS:
            if not submited_by in NUM_FILTER:
                filter_items = to_dict(list(FILTER_ITEMS))
                e = "%s does not support the %s filter" % (filter_items[submited_field],FILTER_BY[sbi][1])
                raise forms.ValidationError(e)
            if submited_value in EMPTY_VALUES:
                raise forms.ValidationError("Please supply a value to query")
        if submited_field in TEXT_FIELDS:
            if not submited_by in TEXT_FILTER:
                filter_items = to_dict(list(FILTER_ITEMS))
                e = "%s does not support the %s filter" % (filter_items[submited_field],FILTER_BY[sbi][1])
                raise forms.ValidationError(e)
            if submited_value in EMPTY_VALUES:
                raise forms.ValidationError("Please supply a value to query")
        if submited_field in TIME_FIELDS:
            if not submited_by in TIME_FILTER:
                filter_items = to_dict(list(FILTER_ITEMS))
                e = "%s does not support the %s filter" % (filter_items[submited_field],FILTER_BY[sbi][1])
                raise forms.ValidationError(e)
            if submited_value in EMPTY_VALUES:
                raise forms.ValidationError("Please supply a value to query")

        return cleaned_data