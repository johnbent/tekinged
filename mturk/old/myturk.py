# https://chromium.googlesource.com/external/boto/+/master/bin/mturk

import datetime,calendar


def display_datetime(dt):
  return dt.strftime('%e %b %Y, %l:%M %P')


mturk_website="mturk.com"
def preview_url(hit):
    return 'https://{}/mturk/preview?groupId={}'.format(
        mturk_website, hit.HITTypeId)



time_units = dict(
    s = 1,
    min = 60,
    h = 60 * 60,
    d = 24 * 60 * 60)

def display_duration(n):
    for unit, m in sorted(time_units.items(), key = lambda x: -x[1]):
      if n % m == 0:
        return '{} {}'.format(n / m, unit)

nicknames = {}
def get_nickname(hitid):
    for k, v in nicknames.items():
      if v == hitid:
        return k
    return "No nickname"



def parse_timestamp(s):
    '''Takes a timestamp like "2012-11-24T16:34:41Z".  Returns a datetime object in the local time zone.'''
    return datetime.datetime.fromtimestamp(
        calendar.timegm(
        datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').timetuple()))


def display_hit(hit, verbose = False):
    et = parse_timestamp(hit.Expiration)
    return '\n'.join([
        '{} - {} ({}, {}, {})'.format(
            get_nickname(hit.HITId),
            hit.Title,
            hit.FormattedPrice,
            display_duration(int(hit.AssignmentDurationInSeconds)),
            hit.HITStatus),
        'HIT ID: ' + hit.HITId,
        'Type ID: ' + hit.HITTypeId,
        'Group ID: ' + hit.HITGroupId,
        'Preview: ' + preview_url(hit),
        'Created {}   {}'.format(
            display_datetime(parse_timestamp(hit.CreationTime)),
            'Expired' if et <= datetime.datetime.now() else
                'Expires ' + display_datetime(et)),
        'Assignments: {} -- {} avail, {} pending, {} reviewable, {} reviewed'.format(
            hit.MaxAssignments,
            hit.NumberOfAssignmentsAvailable,
            hit.NumberOfAssignmentsPending,
            int(hit.MaxAssignments) - (int(hit.NumberOfAssignmentsAvailable) + int(hit.NumberOfAssignmentsPending) + int(hit.NumberOfAssignmentsCompleted)),
            hit.NumberOfAssignmentsCompleted)
            if hasattr(hit, 'NumberOfAssignmentsAvailable')
            else 'Assignments: {} total'.format(hit.MaxAssignments),
            # For some reason, SearchHITs includes the
            # NumberOfAssignmentsFoobar fields but GetHIT doesn't.
        ] + ([] if not verbose else [
            '\nDescription: ' + hit.Description,
            '\nKeywords: ' + hit.Keywords
        ])) + '\n'
