from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.utils.translation import gettext_lazy as _
import gpxpy


class GpxFile(models.Model):
    '''
    Let users upload gpx files.
    Ideally, parse the content when file is uploaded, for now manual parsing works.
    '''
    name = models.CharField(max_length=100)
    gpx_file = models.FileField(upload_to='gpx/')
    track = models.LineStringField(
        _("Track of gpx file"), blank=True, null=True)
    elevation = models.JSONField(
        _("Elevation of track"), default=list, blank=True, null=True)

    def parse_gpx(self):
        with open(self.gpx_file.path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            track_points = []
            elevation = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        track_points.append((point.longitude, point.latitude))
                    if segment.has_elevations:
                        for point in segment.points:
                            elevation.append(point.elevation)
            linestring = LineString(track_points)
            self.track = linestring
            self.elevation = elevation
            print(
                f"Finished parsing gpx file, call {self.name}.save() to save to database")

    def __str__(self):
        return self.name
