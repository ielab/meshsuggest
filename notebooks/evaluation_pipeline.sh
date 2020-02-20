#!/usr/bin/env bash

RUNS=$(ls queries)

for query in ${RUNS}; do
  for collection in "2017/testing" "2018/testing" "2019/testing/DTA" "2019/testing/Intervention"; do
    echo queries/${query}/${collection}
    mkdir -p results/${collection}
    if [ -e results/${collection}/${query}.res ]; then
      echo "results file already exists... skipping!"
      continue
    fi
    boogie --pipeline notebooks/pipelines/evaluate-pipeline.json queries/${query}/${collection} results/${collection}/${query}.res notebooks/combined_pubdates
  done
done
