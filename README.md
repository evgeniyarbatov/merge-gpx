# Merge GPX Files

GPS location recorded with a watch has lower accuracy than the one recorded with a phone. The phone does not record heart rate / power / cadence. Solution? Combine GPX files created with the phone and watch based on timestamps.

## Tools

- [OSMTracker](https://wiki.openstreetmap.org/wiki/OSMTracker_(Android)) app to record GPX
- smartwatch to create GPX file

## Run

Download GPX from your watch.

Download phone GPX traces from Google Drive:

```
make
```

Merge:

```
python3 merge.py \
traces/osm-upload5693156463216149905.gpx \
~/Downloads/Night_Run\ \(1\).gpx \
~/Downloads/Fixed_Night_Run.gpx
```

where

- `traces/osm-upload5693156463216149905.gpx`: GPX file from the phone
- `~/Downloads/Night_Run\ \(1\).gpx`: GPX file from watch
- `~/Downloads/Fixed_Night_Run.gpx`: merged GPX file