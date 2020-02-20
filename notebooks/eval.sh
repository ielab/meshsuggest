#!/usr/bin/env bash

# ATM
trec_eval -m recall.5,10,20 ../data/clef_tar_processed/2017/testing/data.qrels ../data/clef_tar_processed/2017/testing/meta_all.res >atm_2017.run
trec_eval -m recall.5,10,20 ../data/clef_tar_processed/2018/testing/data.qrels ../data/clef_tar_processed/2018/testing/meta_all.res >atm_2018.run
trec_eval -m recall.5,10,20 ../data/clef_tar_processed/2019/DTA/testing/data.qrels ../data/clef_tar_processed/2019/DTA/testing/meta_all.res >atm_2019_d.run
trec_eval -m recall.5,10,20 ../data/clef_tar_processed/2019/Intervention/testing/data.qrels ../data/clef_tar_processed/2019/Intervention/testing/meta_all.res >atm_2019_i.run
