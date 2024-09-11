# Merge GPX Files

GPS location recorded with a watch tends to be lower accuracy than the one recorded with a phone. 

The phone does not record heart rate and cadence while the watch does. 

Solution? Combine GPX files created with phone and watch based on common timestamp.

## Tools

- [OSMTracker](https://wiki.openstreetmap.org/wiki/OSMTracker_(Android)) app to record GPX
- smartwatch to create GPX file

## Run

```
python3 merge.py \
traces/osm-upload5693156463216149905.gpx # GPX file from the phone
~/Downloads/Night_Run\ \(1\).gpx # GPX file from watch
~/Downloads/Fixed_Night_Run.gpx # Merged GPX file
```
