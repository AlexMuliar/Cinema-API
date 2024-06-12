#!/bin/sh
set -e

if [ "$APP_ENV" = "prod" ]; then
    uvicorn src.app:app --host=0.0.0.0 --port=8000 --log-level=debug
else
    uvicorn src.app:app --host=0.0.0.0 --port=8000 --log-level=debug --reload
fi

exec "$@"
