#!/bin/bash
# Clean the Wikipedia Presidents data.
cat data/presidents-wikipedia.txt | grep -A3 sortname | sed s/'{{ayd|.*}}<br>'/''/ | sed s/'}}.*'// | sed s/'{{sortname|'// | sed s/'{{nowrap|'// | sed s/'|abbr=on'// | sed s/'{{dts|'// | sed s/'<span .*'/""/ | sed s/'^| '// | sed s/'nowrap | '//  > data/presidents-wikipedia-clean.txt

