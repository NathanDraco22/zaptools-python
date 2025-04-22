## 0.5.1
- Added `None` validation to Headers
- Updated Changelog file


## 0.5.0
- Added `ConnectionRouter` class
- Refactor: Change project structure
- __BREAKING CHANGE:__ Empty header is not includes into json data.
```json
{
    "eventName": "empty-event",
    "payload": null
}
```

## 0.4.6
- Added github action

## 0.4.4
- Added py.typed file
- Fixed: event stream gets blocked

## 0.3.0
- Added support to python Client