import re

import boto3
from botocore import exceptions
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pytube import YouTube
from pytube.helpers import safe_filename
from zappa.async import task


def get_video_stream(video_id):
    yt = YouTube('https://www.youtube.com/watch?v=%s' % video_id)
    return yt.streams.filter(progressive=True, subtype=settings.VIDEO_FORMAT).order_by('resolution').asc().first()


def get_filename(stream):
    title = stream.player_config_args['title']
    return '{filename}.{subtype}'.format(filename=safe_filename(title), subtype=stream.subtype)


@task
def download(video_id):
    stream = get_video_stream(video_id)
    default_storage.save(get_filename(stream), stream.stream_to_buffer())


def index(request):
    video_url = request.GET.get('url')

    if not video_url:
        return HttpResponseBadRequest('missing url parameter')

    m = re.match(r'^http(s)?://(www\.)?youtube\.com.*v=([^&]*)$', video_url)

    if m is None or len(m.groups()) < 3:
        return HttpResponseBadRequest('Video ID not found')

    video_id = m.group(3)

    download(video_id)  # call lambda function

    return render(request, 'index.html', {'videoId': video_id, 'apiStage': settings.LAMBDA_STAGE})


def check_video(request):
    video_id = request.GET.get('video_id')

    if not video_id:
        return HttpResponseBadRequest('missing video id')

    stream = get_video_stream(video_id)
    filename = get_filename(stream)

    downloaded = 0

    s3 = boto3.resource('s3')

    try:
        s3.Object(settings.AWS_S3_BUCKET_NAME, filename).load()
    except exceptions.ClientError as e:
        # if e.response['Error']['Code'] == "404":
        #     # The object does not exist.
        #     return JsonResponse({'url': None})
        # else:
        #     # Something else has gone wrong.
        #     raise
        pass
    else:
        # The object does exist.
        downloaded = 1

    return JsonResponse({'downloaded': downloaded})
