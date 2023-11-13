#!/bin/bash
docker run --rm -it -v $(pwd):/data ylked/pandoc bash -c "/root/build.sh /data/report.md /data/report.pdf"
