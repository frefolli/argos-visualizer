#!/bin/bash

rm -rf output ~/Desktop/output/
mkdir ~/Desktop/output
make executor SUPPLEMENT="-i archive-task-executor"
mv output ~/Desktop/output/TaskExecutor/
make allocator SUPPLEMENT="-i archive-task-allocator"
mv output ~/Desktop/output/TaskAllocator/
make allocator SUPPLEMENT="-i archive-task-allocator-shortened"
mv output ~/Desktop/output/TaskAllocatorShortened/
